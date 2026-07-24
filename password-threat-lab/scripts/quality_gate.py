#!/usr/bin/env python3
"""Run the scoped Password Threat Lab local evidence gate."""

from __future__ import annotations

import argparse
import functools
import http.server
import json
import platform
import shutil
import subprocess
import sys
import threading
import time
import urllib.request
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = (
    "README.md",
    "AGENTS.md",
    "NEXT_RUN.md",
    "COMMANDS.md",
    ".repo-standard.yml",
    ".gitignore",
    "index.html",
    "serve.py",
    "assets/styles.css",
    "assets/estimator.js",
    "assets/app.js",
    "data/attack-profiles.json",
    "app.manifest.json",
    "app.surface.json",
    "tools/reference_estimator.py",
    "tests/test_reference_estimator.py",
    "tests/test_browser_contract.mjs",
    "scripts/check_napp_contract.py",
    "scripts/check_surface_contract.py",
    "scripts/check_static_site.py",
    "scripts/browser_smoke.py",
    "scripts/quality_gate.py",
    "docs/PRODUCT_RECONNAISSANCE.md",
    "docs/STACK_EVIDENCE_PACKET.md",
    "docs/MENU_SURFACE_PILOT.md",
    "docs/product/CURRENT_FEATURES.md",
    "docs/product/CURRENT_VS_PLANNED.md",
    "docs/product/FEATURE_LEDGER.md",
    "docs/n-sdt/current-truth.md",
    "docs/n-sdt/handoff.md",
    "docs/nvibe/SCAN_EVIDENCE.md",
    "docs/project_management/MISSED_OPPORTUNITIES.md",
    "reports/tier3-scorecard.json",
)
TEXT_SUFFIXES = {".html", ".css", ".js", ".mjs", ".py", ".md", ".json", ".yml", ".yaml", ".txt"}


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store, max-age=0")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        super().end_headers()

    def log_message(self, format: str, *args: object) -> None:  # noqa: A002
        return


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run local Password Threat Lab checks.")
    parser.add_argument("--write-report", type=Path, help="Write the JSON evidence receipt")
    parser.add_argument("--screenshots", action="store_true", help="Regenerate synthetic Chromium screenshots")
    return parser.parse_args()


def run_command(name: str, command: list[str], records: list[dict[str, Any]]) -> None:
    started = time.perf_counter()
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    duration = round(time.perf_counter() - started, 3)
    output = (result.stdout + result.stderr).strip()
    records.append(
        {
            "name": name,
            "status": "pass" if result.returncode == 0 else "fail",
            "command": command,
            "duration_seconds": duration,
            "output": output[-8000:],
        }
    )
    if result.returncode != 0:
        raise RuntimeError(f"{name} failed\n{output}")
    print(f"[pass] {name} ({duration:.3f}s)")


def check_required_files(records: list[dict[str, Any]]) -> None:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).is_file()]
    if missing:
        records.append({"name": "required file floor", "status": "fail", "missing": missing})
        raise RuntimeError(f"missing required files: {missing}")
    records.append({"name": "required file floor", "status": "pass", "count": len(REQUIRED_FILES)})
    print(f"[pass] required file floor ({len(REQUIRED_FILES)} files)")


def check_json(records: list[dict[str, Any]]) -> None:
    parsed: list[str] = []
    for path in sorted(ROOT.rglob("*.json")):
        json.loads(path.read_text(encoding="utf-8"))
        parsed.append(str(path.relative_to(ROOT)))
    records.append({"name": "JSON parse", "status": "pass", "files": parsed})
    print(f"[pass] JSON parse ({len(parsed)} files)")


def check_text_hygiene(records: list[dict[str, Any]]) -> None:
    checked = 0
    failures: list[str] = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if path.name == "local-proof.json":
            continue
        text = path.read_text(encoding="utf-8")
        checked += 1
        if "\x00" in text:
            failures.append(f"{path.relative_to(ROOT)}: NUL byte")
        if text and not text.endswith("\n"):
            failures.append(f"{path.relative_to(ROOT)}: no final newline")
        for line_number, line in enumerate(text.splitlines(), 1):
            if line.rstrip(" \t") != line:
                failures.append(f"{path.relative_to(ROOT)}:{line_number}: trailing whitespace")
                break
    if failures:
        records.append({"name": "text hygiene", "status": "fail", "failures": failures})
        raise RuntimeError("text hygiene failed: " + "; ".join(failures))
    records.append({"name": "text hygiene", "status": "pass", "files": checked})
    print(f"[pass] text hygiene ({checked} files)")


def check_http(records: list[dict[str, Any]]) -> None:
    handler = functools.partial(QuietHandler, directory=str(ROOT))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    host, port = server.server_address[:2]
    results: list[dict[str, Any]] = []
    try:
        for relative, expected in (
            ("index.html", "text/html"),
            ("assets/styles.css", "text/css"),
            ("assets/estimator.js", "javascript"),
            ("assets/app.js", "javascript"),
            ("data/attack-profiles.json", "application/json"),
        ):
            request = urllib.request.Request(f"http://{host}:{port}/{relative}", headers={"User-Agent": "PasswordThreatLab-LocalProof/1"})
            with urllib.request.urlopen(request, timeout=5) as response:
                body = response.read()
                content_type = response.headers.get_content_type()
                cache_control = response.headers.get("Cache-Control", "")
                if not body:
                    raise RuntimeError(f"empty HTTP response for {relative}")
                if expected not in content_type:
                    raise RuntimeError(f"unexpected content type for {relative}: {content_type}")
                if "no-store" not in cache_control:
                    raise RuntimeError(f"missing no-store for {relative}")
                results.append({"path": relative, "status": response.status, "content_type": content_type, "bytes": len(body)})
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=3)
    records.append({"name": "loopback HTTP smoke", "status": "pass", "assets": results})
    print(f"[pass] loopback HTTP smoke ({len(results)} assets)")


def browser_command(screenshots: bool) -> list[str]:
    command = [sys.executable, "scripts/browser_smoke.py"]
    if screenshots:
        command.append("--screenshots")
    return command


def environment_snapshot() -> dict[str, Any]:
    node = shutil.which("node")
    chromium = shutil.which("chromium") or shutil.which("chromium-browser") or shutil.which("google-chrome")
    node_version = None
    if node:
        node_version = subprocess.run([node, "--version"], text=True, capture_output=True, check=False).stdout.strip()
    return {
        "python": sys.version.split()[0],
        "python_implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "node": node_version,
        "chromium": chromium,
        "execution": "local isolated workspace",
    }


def write_report(path: Path, receipt: dict[str, Any]) -> None:
    target = path if path.is_absolute() else ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"receipt: {target}")


def main() -> int:
    args = parse_args()
    started_at = datetime.now(UTC)
    records: list[dict[str, Any]] = []
    status = "pass"
    error: str | None = None

    try:
        check_required_files(records)
        check_json(records)
        check_text_hygiene(records)
        run_command("N-App manifest contract", [sys.executable, "scripts/check_napp_contract.py"], records)
        run_command("surface contract", [sys.executable, "scripts/check_surface_contract.py"], records)
        run_command("static privacy and dependency contract", [sys.executable, "scripts/check_static_site.py"], records)
        run_command("Python reference tests", [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], records)
        if not shutil.which("node"):
            raise RuntimeError("Node.js is required for the browser-estimator contract test")
        run_command("JavaScript estimator tests", ["node", "tests/test_browser_contract.mjs"], records)
        check_http(records)
        run_command("Chromium synthetic interaction smoke", browser_command(args.screenshots), records)
    except Exception as exc:  # noqa: BLE001 - gate must persist a bounded failure receipt
        status = "fail"
        error = str(exc)
        print(f"[fail] {error}", file=sys.stderr)

    finished_at = datetime.now(UTC)
    receipt = {
        "schema_version": "n.local-proof.password-threat-lab.v1",
        "status": status,
        "started_at_utc": started_at.isoformat(),
        "finished_at_utc": finished_at.isoformat(),
        "duration_seconds": round((finished_at - started_at).total_seconds(), 3),
        "scope": "password-threat-lab/**",
        "synthetic_input_only": True,
        "checks": records,
        "environment": environment_snapshot(),
        "error": error,
        "claim_boundaries": [
            "Local proof only; hosted CI was not asserted.",
            "No production-ready, production-grade, MVP-ready, secure, or audited claim.",
            "No GitHub Pages deployment claim.",
            "No quantum hardware feasibility or wall-clock cracking claim.",
            "No real credential was required or recorded.",
        ],
    }
    if args.write_report:
        write_report(args.write_report, receipt)
    if status != "pass":
        return 1
    print(f"quality gate: pass ({receipt['duration_seconds']:.3f}s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
