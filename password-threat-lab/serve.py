"""Serve Password Threat Lab locally with the Python standard library."""

from __future__ import annotations

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent


class NoStoreHandler(SimpleHTTPRequestHandler):
    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        super().end_headers()

    def log_message(self, format: str, *args: object) -> None:
        # Request paths are logged by the standard server. The application never
        # places the analyzed value in a URL, so the sample is not part of logs.
        super().log_message(format, *args)


def main() -> int:
    parser = argparse.ArgumentParser(description="Serve Password Threat Lab on loopback.")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    handler = partial(NoStoreHandler, directory=str(ROOT))
    server = ThreadingHTTPServer(("127.0.0.1", args.port), handler)
    print(f"Password Threat Lab: http://127.0.0.1:{args.port}/")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
