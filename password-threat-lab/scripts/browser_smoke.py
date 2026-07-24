#!/usr/bin/env python3
"""Render the actual site assets in Chromium and exercise a synthetic sample.

The managed execution environment may block browser navigation to loopback or
file URLs. This smoke check therefore renders the real HTML/CSS/JS in memory.
CSP and same-origin asset behavior are validated separately by static and HTTP
checks in the quality gate.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--screenshots", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise SystemExit(f"browser smoke unavailable: {exc}") from exc

    html = (ROOT / "index.html").read_text(encoding="utf-8")
    css = (ROOT / "assets" / "styles.css").read_text(encoding="utf-8")
    estimator = (ROOT / "assets" / "estimator.js").read_text(encoding="utf-8")
    app = (ROOT / "assets" / "app.js").read_text(encoding="utf-8")

    # Remove CSP and external local asset tags for the in-memory harness only.
    html = re.sub(
        r'<meta\s+http-equiv="Content-Security-Policy"[^>]*>',
        "",
        html,
        flags=re.IGNORECASE,
    )
    html = re.sub(r'<link\s+rel="stylesheet"\s+href="assets/styles\.css"\s*>', "", html)
    html = re.sub(r'<script\s+src="assets/(?:estimator|app)\.js"\s+defer></script>', "", html)

    errors: list[str] = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            executable_path="/usr/bin/chromium",
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"],
        )
        try:
            page = browser.new_page(viewport={"width": 1440, "height": 1000}, device_scale_factor=1)
            page.on("console", lambda message: errors.append(f"console:{message.type}:{message.text}") if message.type == "error" else None)
            page.on("pageerror", lambda error: errors.append(f"pageerror:{error}"))
            page.set_content(html, wait_until="domcontentloaded")
            page.add_style_tag(content=css)
            page.add_script_tag(content=estimator)
            page.add_script_tag(content=app)
            page.wait_for_function("document.documentElement.dataset.ready === 'true'", timeout=15_000)

            assert page.title() == "Password Threat Lab — Classical and Quantum Context"
            assert page.locator("#emptyState").is_visible()
            page.locator("#passwordInput").fill("Password1!")
            page.wait_for_function("document.querySelector('#patternMethod').textContent.includes('word with predictable suffix')")
            assert page.locator("#strengthLabel").inner_text() == "Very weak"
            assert page.locator("#resultState").is_visible()
            assert "word with predictable suffix" in page.locator("#patternMethod").inner_text().lower()
            assert page.locator("#patternTime").inner_text().strip() not in {"", "—"}
            assert page.locator("#groverQueries").inner_text().strip() not in {"", "—"}

            page.locator("#toggleVisibility").click()
            assert page.locator("#passwordInput").get_attribute("type") == "text"
            page.locator("#clearInput").click()
            assert page.locator("#passwordInput").input_value() == ""
            assert page.locator("#emptyState").is_visible()

            if args.screenshots:
                assets = ROOT / "docs" / "assets"
                assets.mkdir(parents=True, exist_ok=True)
                page.screenshot(path=str(assets / "desktop-proof.png"), full_page=True)
                mobile = browser.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=1)
                try:
                    mobile.set_content(html, wait_until="domcontentloaded")
                    mobile.add_style_tag(content=css)
                    mobile.add_script_tag(content=estimator)
                    mobile.add_script_tag(content=app)
                    mobile.wait_for_function("document.documentElement.dataset.ready === 'true'", timeout=15_000)
                    mobile.locator("#passwordInput").fill("Password1!")
                    mobile.screenshot(path=str(assets / "mobile-proof.png"), full_page=True)
                finally:
                    mobile.close()
        finally:
            browser.close()

    if errors:
        raise SystemExit("browser smoke errors: " + " | ".join(errors))
    print(json.dumps({"status": "pass", "sample": "synthetic", "method": "word with predictable suffix"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
