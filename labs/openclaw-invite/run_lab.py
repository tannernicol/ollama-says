#!/usr/bin/env python3
import json
import os
import socket
import threading
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

BASE_DIR = Path(__file__).resolve().parent
CONTROL_HTML = ""
DEFENDED_HTML = ""

CONTROL_PORT = None
GATEWAY_PORT = None
ATTACKER_PORT = None

GATEWAY_TOKEN = "gateway-token-123"

gateway_state = {
    "payload_executed": False,
    "last_action": "",
}

attacker_state = {
    "last_token": "",
    "last_gateway": "",
    "last_result": "",
}

lab_state = {
    "last_report": "",
    "last_event": "",
}


def _send_json(handler, status, payload):
    data = json.dumps(payload).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(data)))
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.end_headers()
    handler.wfile.write(data)


def _send_text(handler, status, payload, content_type="text/plain; charset=utf-8"):
    data = payload.encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", content_type)
    handler.send_header("Content-Length", str(len(data)))
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.end_headers()
    handler.wfile.write(data)


class ControlHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        if path in ("/", "/control.html"):
            _send_text(self, 200, CONTROL_HTML, "text/html; charset=utf-8")
            return
        if path == "/control_defended.html":
            _send_text(self, 200, DEFENDED_HTML, "text/html; charset=utf-8")
            return
        _send_text(self, 404, "Not Found")

    def log_message(self, format, *args):
        return


class GatewayHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-Gateway-Token")
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/status":
            _send_json(self, 200, gateway_state)
            return
        _send_text(self, 200, "Gateway lab running")

    def do_POST(self):
        path = urlparse(self.path).path
        if path == "/reset":
            gateway_state["payload_executed"] = False
            gateway_state["last_action"] = "reset"
            _write_report("gateway_reset")
            _send_json(self, 200, {"ok": True})
            return
        if path == "/run":
            token = self.headers.get("X-Gateway-Token", "")
            if token != GATEWAY_TOKEN:
                _send_json(self, 403, {"ok": False, "error": "invalid token"})
                return
            gateway_state["payload_executed"] = True
            gateway_state["last_action"] = "payload executed"
            _write_report("payload_executed")
            _send_json(self, 200, {"ok": True, "message": "payload executed"})
            return
        _send_json(self, 404, {"ok": False, "error": "not found"})

    def log_message(self, format, *args):
        return


class AttackerHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/status":
            _send_json(self, 200, attacker_state)
            return
        if path == "/report":
            _send_json(self, 200, lab_state)
            return
        _send_text(self, 200, "Attacker lab running")

    def do_POST(self):
        path = urlparse(self.path).path
        if path != "/connect":
            _send_json(self, 404, {"ok": False, "error": "not found"})
            return

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8")
        try:
            payload = json.loads(body) if body else {}
        except json.JSONDecodeError:
            payload = {}

        token = payload.get("token", "")
        gateway_url = payload.get("gateway", f"http://localhost:{GATEWAY_PORT}")

        attacker_state["last_token"] = token
        attacker_state["last_gateway"] = gateway_url

        result = ""
        try:
            req = Request(
                f"{gateway_url}/run",
                method="POST",
                headers={"X-Gateway-Token": token},
                data=b"",
            )
            with urlopen(req, timeout=2) as resp:
                result = resp.read().decode("utf-8")
        except Exception as exc:
            result = f"error: {exc}"

        attacker_state["last_result"] = result
        _write_report("attacker_connect")
        _send_json(self, 200, {"ok": True, "result": result})

    def log_message(self, format, *args):
        return


def _serve(server):
    server.serve_forever()

def _redact_token(token):
    if not token:
        return ""
    if len(token) <= 4:
        return "***"
    return f"{token[:2]}***{token[-2:]}"

def _write_report(action):
    report_dir = Path(os.environ.get("LAB_REPORT_DIR", BASE_DIR.parent.parent / "reports" / "labs"))
    report_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    report = {
        "lab_id": "openclaw-invite",
        "timestamp": timestamp,
        "action": action,
        "requested_url": "",
        "status": "",
        "blocked_reason": "",
        "ports": {
            "control": CONTROL_PORT,
            "gateway": GATEWAY_PORT,
            "attacker": ATTACKER_PORT,
        },
        "gateway_state": dict(gateway_state),
        "attacker_state": {
            "last_token": _redact_token(attacker_state.get("last_token", "")),
            "last_gateway": attacker_state.get("last_gateway", ""),
            "last_result": attacker_state.get("last_result", ""),
        },
        "note": "Local-only lab report. Payload is a benign state flip.",
    }
    report_path = report_dir / f"openclaw_invite_{timestamp}.json"
    report_path.write_text(json.dumps(report, indent=2))
    latest_path = report_dir / "openclaw_invite_latest.json"
    latest_path.write_text(json.dumps(report, indent=2))
    lab_state["last_report"] = str(report_path)
    lab_state["last_event"] = action
    return report_path

def _ports_available(base_port, span=3):
    sockets = []
    try:
        for offset in range(span):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(("", base_port + offset))
            sockets.append(sock)
        return True
    except OSError:
        return False
    finally:
        for sock in sockets:
            sock.close()

def _pick_base_port(preferred):
    if _ports_available(preferred):
        return preferred
    for step in range(1, 21):
        candidate = preferred + step * 10
        if _ports_available(candidate):
            return candidate
    raise RuntimeError("No available port range found.")

def main():
    global CONTROL_PORT, GATEWAY_PORT, ATTACKER_PORT, CONTROL_HTML, DEFENDED_HTML

    preferred_base = int(os.environ.get("LAB_PORT_BASE", "8000"))
    base_port = _pick_base_port(preferred_base)
    CONTROL_PORT = base_port
    GATEWAY_PORT = base_port + 1
    ATTACKER_PORT = base_port + 2

    CONTROL_HTML = (BASE_DIR / "control.html").read_text(encoding="utf-8")
    DEFENDED_HTML = (BASE_DIR / "control_defended.html").read_text(encoding="utf-8")
    CONTROL_HTML = CONTROL_HTML.replace("__GATEWAY_PORT__", str(GATEWAY_PORT))
    CONTROL_HTML = CONTROL_HTML.replace("__ATTACKER_PORT__", str(ATTACKER_PORT))
    DEFENDED_HTML = DEFENDED_HTML.replace("__GATEWAY_PORT__", str(GATEWAY_PORT))
    DEFENDED_HTML = DEFENDED_HTML.replace("__ATTACKER_PORT__", str(ATTACKER_PORT))

    servers = [
        (CONTROL_PORT, ControlHandler),
        (GATEWAY_PORT, GatewayHandler),
        (ATTACKER_PORT, AttackerHandler),
    ]

    threads = []
    for port, handler in servers:
        httpd = ThreadingHTTPServer(("", port), handler)
        thread = threading.Thread(target=_serve, args=(httpd,), daemon=True)
        thread.start()
        threads.append((thread, httpd))

    print("OpenClaw invite lab running:")
    print(f"- Control (vulnerable): http://localhost:{CONTROL_PORT}/control.html?gatewayUrl=http://localhost:{ATTACKER_PORT}")
    print(f"- Control (defended):   http://localhost:{CONTROL_PORT}/control_defended.html?gatewayUrl=http://localhost:{ATTACKER_PORT}")
    print(f"- Gateway status:       http://localhost:{GATEWAY_PORT}/status")
    print(f"- Attacker status:      http://localhost:{ATTACKER_PORT}/status")
    print(f"- Report info:          http://localhost:{ATTACKER_PORT}/report")
    print(f"- Reports directory:    {Path(os.environ.get('LAB_REPORT_DIR', BASE_DIR.parent.parent / 'reports' / 'labs')).resolve()}")
    if base_port != preferred_base:
        print(f"Note: default ports were busy; using base {base_port}.")
    print("Press Ctrl+C to stop.")

    try:
        for thread, _httpd in threads:
            thread.join()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
