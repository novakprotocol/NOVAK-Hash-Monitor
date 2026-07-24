#!/usr/bin/env python3
"""Serve the static Password Threat Lab on a loopback-only development server."""

from __future__ import annotations

import argparse
import contextlib
import http.server
import os
import socketserver
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent


class NoStoreHandler(http.server.SimpleHTTPRequestHandler):
    """Static handler with conservative local-development response headers."""

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Cross-Origin-Resource-Policy", "same-origin")
        super().end_headers()

    def log_message(self, format: str, *args: object) -> None:  # noqa: A002
        # Log method/path/status only. Request bodies are impossible for this GET-only surface.
        super().log_message(format, *args)


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Serve Password Threat Lab locally.")
    parser.add_argument("--host", default="127.0.0.1", help="Bind address (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8000, help="TCP port (default: 8000)")
    parser.add_argument("--open", action="store_true", help="Open the page in the default browser")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.port < 0 or args.port > 65535:
        raise SystemExit("--port must be between 0 and 65535")

    os.chdir(ROOT)
    with ReusableTCPServer((args.host, args.port), NoStoreHandler) as server:
        host, port = server.server_address[:2]
        url = f"http://{host}:{port}/"
        print(f"Password Threat Lab: {url}")
        print("Press Ctrl+C to stop.")
        if args.open:
            with contextlib.suppress(Exception):
                webbrowser.open(url)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
