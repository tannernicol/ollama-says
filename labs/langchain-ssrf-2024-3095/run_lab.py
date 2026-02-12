#!/usr/bin/env python3
import json
import os
import socket
import threading
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from ipaddress import ip_address
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from urllib.request import urlopen

BASE_DIR = Path(__file__).resolve().parent
CONTROL_HTML = ""
DEFENDED_HTML = ""

CONTROL_PORT = None
INTERNAL_PORT = None
PUBLIC_PORT = None

state = {
    "internal_hits": 0,
    "last_request": "",
    "last_blocked": "",
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


def _write_report(action, url, status, blocked_reason=""):
    report_dir = Path(os.environ.get("LAB_REPORT_DIR", BASE_DIR.parent.parent / "reports" / "labs"))
    report_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    report = {
        "lab_id": "langchain-ssrf-2024-3095",
        "timestamp": timestamp,
        "action": action,
        "requested_url": url,
        "status": status,
        "blocked_reason": blocked_reason,
        "ports": {
            "control": CONTROL_PORT,
            "internal": INTERNAL_PORT,
            "public": PUBLIC_PORT,
        },
        "state": dict(state),
    }
    report_path = report_dir / f"langchain_ssrf_2024_3095_{timestamp}.json"
    report_path.write_text(json.dumps(report, indent=2))
    latest_path = report_dir / "langchain_ssrf_2024_3095_latest.json"
    latest_path.write_text(json.dumps(report, indent=2))
    lab_state["last_report"] = str(report_path)
    lab_state["last_event"] = action


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


def _is_blocked(url):
    try:
        parsed = urlparse(url)
    except Exception:
        return True, "invalid_url"
    if parsed.scheme not in ("http", "https"):
        return True, "invalid_scheme"
    host = parsed.hostname
    if not host:
        return True, "missing_host"
    if host in ("localhost", "127.0.0.1", "::1"):
        return True, "localhost_blocked"
    try:
        ips = {ip_address(socket.gethostbyname(host))}
    except Exception:
        return True, "dns_lookup_failed"
    for ip in ips:
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast:
            return True, "private_address"
    return False, ""


def _fetch_url(url):
    with urlopen(url, timeout=2) as resp:
        data = resp.read(512).decode("utf-8", errors="replace")
        return data


class ControlHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        if path in ("/", "/control.html"):
            _send_text(self, 200, CONTROL_HTML, "text/html; charset=utf-8")
            return
        if path == "/control_defended.html":
            _send_text(self, 200, DEFENDED_HTML, "text/html; charset=utf-8")
            return
        if path == "/status":
            _send_json(self, 200, state)
            return
        if path == "/report":
            _send_json(self, 200, lab_state)
            return
        _send_text(self, 404, "Not Found")

    def do_POST(self):
        path = urlparse(self.path).path
        if path == "/fetch":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode("utf-8")
            payload = json.loads(body or "{}")
            url = payload.get("url", "")
            state["last_request"] = url
            try:
                data = _fetch_url(url)
                _write_report("fetch_vulnerable", url, "ok")
                _send_json(self, 200, {"ok": True, "data": data})
            except Exception as exc:
                _write_report("fetch_vulnerable", url, f"error: {exc}")
                _send_json(self, 500, {"ok": False, "error": str(exc)})
            return
        if path == "/fetch_defended":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode("utf-8")
            payload = json.loads(body or "{}")
            url = payload.get("url", "")
            state["last_request"] = url
            blocked, reason = _is_blocked(url)
            if blocked:
                state["last_blocked"] = reason
                _write_report("fetch_defended", url, "blocked", reason)
                _send_json(self, 403, {"ok": False, "error": reason})
                return
            try:
                data = _fetch_url(url)
                _write_report("fetch_defended", url, "ok")
                _send_json(self, 200, {"ok": True, "data": data})
            except Exception as exc:
                _write_report("fetch_defended", url, f"error: {exc}")
                _send_json(self, 500, {"ok": False, "error": str(exc)})
            return
        _send_json(self, 404, {"ok": False, "error": "not found"})

    def log_message(self, format, *args):
        return


class InternalHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/secret":
            state["internal_hits"] += 1
            _send_text(self, 200, "internal-secret=local-only")
            return
        _send_text(self, 200, "internal service")

    def log_message(self, format, *args):
        return


class PublicHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/public":
            _send_text(self, 200, "public-info=ok")
            return
        _send_text(self, 200, "public service")

    def log_message(self, format, *args):
        return


def _serve(server):
    server.serve_forever()


def main():
    global CONTROL_PORT, INTERNAL_PORT, PUBLIC_PORT, CONTROL_HTML, DEFENDED_HTML

    preferred_base = int(os.environ.get("LAB_PORT_BASE", "9300"))
    base_port = _pick_base_port(preferred_base)
    CONTROL_PORT = base_port
    INTERNAL_PORT = base_port + 1
    PUBLIC_PORT = base_port + 2

    CONTROL_HTML = (BASE_DIR / "control.html").read_text(encoding="utf-8")
    DEFENDED_HTML = (BASE_DIR / "control_defended.html").read_text(encoding="utf-8")
    CONTROL_HTML = CONTROL_HTML.replace("__CONTROL_PORT__", str(CONTROL_PORT))
    CONTROL_HTML = CONTROL_HTML.replace("__INTERNAL_PORT__", str(INTERNAL_PORT))
    CONTROL_HTML = CONTROL_HTML.replace("__PUBLIC_PORT__", str(PUBLIC_PORT))
    DEFENDED_HTML = DEFENDED_HTML.replace("__CONTROL_PORT__", str(CONTROL_PORT))
    DEFENDED_HTML = DEFENDED_HTML.replace("__INTERNAL_PORT__", str(INTERNAL_PORT))
    DEFENDED_HTML = DEFENDED_HTML.replace("__PUBLIC_PORT__", str(PUBLIC_PORT))

    servers = [
        (CONTROL_PORT, ControlHandler),
        (INTERNAL_PORT, InternalHandler),
        (PUBLIC_PORT, PublicHandler),
    ]

    threads = []
    for port, handler in servers:
        httpd = ThreadingHTTPServer(("", port), handler)
        thread = threading.Thread(target=_serve, args=(httpd,), daemon=True)
        thread.start()
        threads.append((thread, httpd))

    print("LangChain WebResearchRetriever SSRF lab running:")
    print(f"- Control (vulnerable): http://localhost:{CONTROL_PORT}/control.html")
    print(f"- Control (defended):   http://localhost:{CONTROL_PORT}/control_defended.html")
    print(f"- Internal service:     http://localhost:{INTERNAL_PORT}/secret")
    print(f"- Public service:       http://localhost:{PUBLIC_PORT}/public")
    print(f"- Report info:          http://localhost:{CONTROL_PORT}/report")
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
