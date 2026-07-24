"""Run local proof for the Password Threat Lab candidate."""

from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import threading
import urllib.request

ROOT = Path(__file__).resolve().parents[1]


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        return


@contextmanager
def local_server():
    handler = partial(QuietHandler, directory=str(ROOT))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}/"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def run_command(name: str, command: list[str], *, timeout: int = 60) -> dict[str, object]:
    result = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
    )
    return {
        "name": name,
        "status": "pass" if result.returncode == 0 else "fail",
        "returncode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
        "command": [Path(command[0]).name, *command[1:]],
    }


def check_required_files() -> dict[str, object]:
    required = [
        "index.html",
        "assets/styles.css",
        "assets/sections.css",
        "assets/estimator.js",
        "assets/app.js",
        "data/attack-profiles.json",
        "README.md",
        "AGENTS.md",
        "NEXT_RUN.md",
        "COMMANDS.md",
        ".repo-standard.yml",
        "app.manifest.json",
        "app.surface.json",
        "docs/PRODUCT_RECONNAISSANCE.md",
        "docs/MENU_SURFACE_PILOT.md",
        "docs/product/CURRENT_FEATURES.md",
        "docs/product/CURRENT_VS_PLANNED.md",
        "docs/product/FEATURE_LEDGER.md",
        "docs/n-sdt/current-truth.md",
        "docs/n-sdt/handoff.md",
        "docs/nvibe/SCAN_EVIDENCE.md",
        "docs/project_management/MISSED_OPPORTUNITIES.md",
        "reports/tier3-scorecard.json",
        "tests/test_reference_estimator.py",
        "tests/test_browser_contract.mjs",
        "tools/reference_estimator.py",
        "serve.py",
    ]
    missing = [value for value in required if not (ROOT / value).is_file()]
    return {
        "name": "required repository floor",
        "status": "pass" if not missing else "fail",
        "missing": missing,
    }


def check_json_files() -> dict[str, object]:
    paths = sorted(ROOT.rglob("*.json"))
    errors: list[str] = []
    for path in paths:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")
    return {
        "name": "JSON parse",
        "status": "pass" if not errors else "fail",
        "files": [str(path.relative_to(ROOT)) for path in paths],
        "errors": errors,
    }


def check_whitespace() -> dict[str, object]:
    errors: list[str] = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.parts[-2:] == ("reports", "local-proof.json"):
            continue
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pyc", ".pyo"}:
            continue
        text = path.read_text(encoding="utf-8")
        for line_number, line in enumerate(text.splitlines(), start=1):
            if line.rstrip() != line:
                errors.append(f"{path.relative_to(ROOT)}:{line_number}: trailing whitespace")
        if text and not text.endswith("\n"):
            errors.append(f"{path.relative_to(ROOT)}: missing final newline")
    return {
        "name": "whitespace",
        "status": "pass" if not errors else "fail",
        "errors": errors,
    }


def http_smoke() -> dict[str, object]:
    requested = [
        "index.html",
        "assets/styles.css",
        "assets/sections.css",
        "assets/estimator.js",
        "assets/app.js",
        "data/attack-profiles.json",
    ]
    errors: list[str] = []
    with local_server() as base_url:
        for path in requested:
            try:
                with urllib.request.urlopen(base_url + path, timeout=10) as response:
                    if response.status != 200:
                        errors.append(f"{path}: HTTP {response.status}")
                    if not response.read(32):
                        errors.append(f"{path}: empty response")
            except Exception as exc:  # pragma: no cover - reported as evidence
                errors.append(f"{path}: {exc}")
    return {
        "name": "loopback HTTP smoke",
        "status": "pass" if not errors else "fail",
        "requested": requested,
        "errors": errors,
    }


def chromium_smoke() -> dict[str, object]:
    chromium = shutil.which("chromium") or shutil.which("chromium-browser") or shutil.which("google-chrome")
    if chromium is None:
        return {
            "name": "Chromium interaction smoke",
            "status": "not-run",
            "reason": "Chromium executable not available",
        }
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return {
            "name": "Chromium interaction smoke",
            "status": "not-run",
            "reason": "Optional Playwright test harness not available",
        }

    import re

    html = (ROOT / "index.html").read_text(encoding="utf-8")
    # Direct browser navigation is blocked in some managed tool environments.
    # Static CSP and loopback HTTP are checked separately; this in-memory render
    # exercises the real HTML, CSS, estimator, and UI code without a network URL.
    html = re.sub(r'<meta http-equiv="Content-Security-Policy"[^>]*>\n?', "", html)
    html = html.replace(
        '<link rel="stylesheet" href="assets/styles.css">',
        f'<style>{(ROOT / "assets" / "styles.css").read_text(encoding="utf-8")}</style>',
    )
    html = html.replace(
        '<link rel="stylesheet" href="assets/sections.css">',
        f'<style>{(ROOT / "assets" / "sections.css").read_text(encoding="utf-8")}</style>',
    )
    html = html.replace('<script src="assets/estimator.js" defer></script>', "")
    html = html.replace('<script src="assets/app.js" defer></script>', "")

    errors: list[str] = []
    observations: dict[str, str] = {}
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(
                headless=True,
                executable_path=chromium,
                args=["--no-sandbox", "--disable-dev-shm-usage"],
            )
            page = browser.new_page(viewport={"width": 1440, "height": 1000})
            page.on("console", lambda message: errors.append(f"console:{message.type}:{message.text}") if message.type == "error" else None)
            page.on("pageerror", lambda exception: errors.append(f"pageerror:{exception}"))
            page.set_content(html, wait_until="load", timeout=30_000)
            page.add_script_tag(content=(ROOT / "assets" / "estimator.js").read_text(encoding="utf-8"))
            page.add_script_tag(content=(ROOT / "assets" / "app.js").read_text(encoding="utf-8"))
            page.wait_for_function("document.documentElement.dataset.ready === 'true'", timeout=10_000)
            observations["title"] = page.title()
            observations["empty_state"] = page.locator("#emptyState").inner_text().strip()
            page.locator("#passwordInput").fill("Password1!")
            page.wait_for_timeout(100)
            observations["method"] = page.locator("#patternMethod").inner_text().strip()
            observations["label"] = page.locator("#strengthLabel").inner_text().strip()
            observations["result_hidden"] = str(page.locator("#resultState").get_attribute("hidden"))
            page.locator("#clearInput").click()
            observations["cleared_length"] = str(page.locator("#passwordInput").input_value().__len__())
            browser.close()
    except Exception as exc:  # pragma: no cover - environment evidence
        errors.append(f"browser harness: {exc}")

    if observations.get("title") != "Password Threat Lab — Classical and Quantum Context":
        errors.append("unexpected page title")
    if "No sample in memory" not in observations.get("empty_state", ""):
        errors.append("empty state not rendered")
    if observations.get("method") != "Word With Predictable Suffix":
        errors.append("interactive pattern result did not render")
    if observations.get("label") != "Very weak":
        errors.append("interactive strength label did not render")
    if observations.get("result_hidden") not in {"None", "null"}:
        errors.append("result surface remained hidden")
    if observations.get("cleared_length") != "0":
        errors.append("clear action did not remove the sample")
    return {
        "name": "Chromium interaction smoke",
        "status": "pass" if not errors else "fail",
        "errors": errors,
        "observations": observations,
        "mode": "in-memory real-asset render; CSP and HTTP checked separately",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Password Threat Lab local quality gate.")
    parser.add_argument("--write-report", type=Path, help="Write the machine-readable receipt to this path.")
    args = parser.parse_args()

    checks: list[dict[str, object]] = [
        check_required_files(),
        check_json_files(),
        check_whitespace(),
        run_command("N-App manifest contract", [sys.executable, "scripts/check_napp_contract.py"]),
        run_command("surface contract", [sys.executable, "scripts/check_surface_contract.py"]),
        run_command("static privacy contract", [sys.executable, "scripts/check_static_site.py"]),
        run_command("Python unit tests", [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py", "-v"]),
    ]

    node = shutil.which("node")
    if node:
        checks.append(run_command("JavaScript estimator contract", [node, "tests/test_browser_contract.mjs"]))
    else:
        checks.append({"name": "JavaScript estimator contract", "status": "not-run", "reason": "Node.js not available"})

    checks.extend([http_smoke(), chromium_smoke()])
    failed = [check for check in checks if check.get("status") == "fail"]
    receipt = {
        "schema_version": "n.local-proof.password-threat-lab.v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "pass" if not failed else "fail",
        "root": ".",
        "python": sys.version.split()[0],
        "checks": checks,
        "claim_boundary": [
            "Local proof only.",
            "No hosted CI claim.",
            "No production-ready, production-grade, security-audit, or quantum feasibility claim.",
            "No real credential was required for the checks.",
        ],
    }

    output = json.dumps(receipt, indent=2, ensure_ascii=False)
    print(output)
    if args.write_report:
        report_path = args.write_report
        if not report_path.is_absolute():
            report_path = ROOT / report_path
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(output + "\n", encoding="utf-8")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
