#!/usr/bin/env python3
"""Static privacy, dependency, and HTML-contract checks for the Pages surface."""

from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
CSS = ROOT / "assets" / "styles.css"
APP_JS = ROOT / "assets" / "app.js"
ESTIMATOR_JS = ROOT / "assets" / "estimator.js"
ALLOWED_SOURCE_HOSTS = {
    "pages.nist.gov",
    "csrc.nist.gov",
    "www.nist.gov",
    "www.nccoe.nist.gov",
}
BANNED_RUNTIME_TOKENS = {
    "localStorage": "browser persistence",
    "sessionStorage": "browser persistence",
    "sendBeacon": "telemetry",
    "XMLHttpRequest": "network API",
    "WebSocket": "network API",
    "document.cookie": "cookies",
    "console.log": "console disclosure",
}


class ContractParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.forms = 0
        self.scripts: list[dict[str, str | None]] = []
        self.links: list[dict[str, str | None]] = []
        self.anchors: list[str] = []
        self.inputs: list[dict[str, str | None]] = []
        self.metas: list[dict[str, str | None]] = []
        self.ids: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "form":
            self.forms += 1
        elif tag == "script":
            self.scripts.append(values)
        elif tag == "link":
            self.links.append(values)
        elif tag == "a" and values.get("href"):
            self.anchors.append(values["href"] or "")
        elif tag == "input":
            self.inputs.append(values)
        elif tag == "meta":
            self.metas.append(values)
        if values.get("id"):
            self.ids.add(values["id"] or "")


def fail(message: str) -> None:
    raise SystemExit(f"static site: {message}")


def local_path(value: str) -> bool:
    parsed = urlparse(value)
    return not parsed.scheme and not parsed.netloc and not value.startswith("//")


def main() -> int:
    html = INDEX.read_text(encoding="utf-8")
    css = CSS.read_text(encoding="utf-8")
    app_js = APP_JS.read_text(encoding="utf-8")
    estimator_js = ESTIMATOR_JS.read_text(encoding="utf-8")

    parser = ContractParser()
    parser.feed(html)

    if parser.forms:
        fail("form submission surfaces are forbidden")

    csp = next(
        (
            item.get("content")
            for item in parser.metas
            if (item.get("http-equiv") or "").lower() == "content-security-policy"
        ),
        None,
    )
    if not csp:
        fail("Content-Security-Policy meta is required")
    for forbidden in ("'unsafe-inline'", "'unsafe-eval'", "http:", "https:", "data:*"):
        if forbidden in csp:
            fail(f"CSP contains forbidden token {forbidden}")
    for required in ("default-src 'self'", "script-src 'self'", "connect-src 'self'", "form-action 'none'"):
        if required not in csp:
            fail(f"CSP missing {required}")

    script_sources = [item.get("src") for item in parser.scripts if item.get("src")]
    if script_sources != ["assets/estimator.js", "assets/app.js"]:
        fail(f"unexpected script sources: {script_sources}")
    if any(not local_path(source or "") for source in script_sources):
        fail("all scripts must be local")
    if any("src" not in item and (item.get("type") or "").lower() != "application/ld+json" for item in parser.scripts):
        fail("inline executable scripts are forbidden")

    stylesheet_links = [
        item.get("href")
        for item in parser.links
        if (item.get("rel") or "").lower() == "stylesheet"
    ]
    if stylesheet_links != ["assets/styles.css"]:
        fail(f"unexpected stylesheet links: {stylesheet_links}")

    password_inputs = [item for item in parser.inputs if item.get("id") == "passwordInput"]
    if len(password_inputs) != 1:
        fail("exactly one passwordInput is required")
    password_input = password_inputs[0]
    expected_input = {
        "type": "password",
        "autocomplete": "new-password",
        "maxlength": "256",
        "spellcheck": "false",
    }
    for key, expected in expected_input.items():
        if password_input.get(key) != expected:
            fail(f"passwordInput {key} must equal {expected!r}")

    for href in parser.anchors:
        parsed = urlparse(href)
        if parsed.scheme in {"http", "https"} and parsed.hostname not in ALLOWED_SOURCE_HOSTS:
            fail(f"external source host is not allowlisted: {parsed.hostname}")

    if re.search(r"@import\s", css, flags=re.IGNORECASE):
        fail("CSS @import is forbidden")
    if re.search(r"url\(\s*['\"]?https?://", css, flags=re.IGNORECASE):
        fail("external CSS URLs are forbidden")

    runtime = app_js + "\n" + estimator_js
    for token, description in BANNED_RUNTIME_TOKENS.items():
        if token in runtime:
            fail(f"{description} token found: {token}")
    if 'fetch("data/attack-profiles.json"' not in app_js:
        fail("local attack-profile JSON fetch is required")
    if 'addEventListener("pagehide"' not in app_js:
        fail("pagehide memory clear is required")
    if ".value = \"\"" not in app_js:
        fail("explicit transient value clear is required")
    if "innerHTML" in app_js or "outerHTML" in app_js:
        fail("unsafe dynamic HTML assignment is forbidden")
    if "textContent" not in app_js:
        fail("safe text rendering is required")

    required_ids = {
        "passwordInput", "attackProfile", "resultState", "patternMethod",
        "patternTime", "randomTime", "groverQueries", "clearInput",
    }
    missing = required_ids - parser.ids
    if missing:
        fail(f"missing required DOM IDs: {sorted(missing)}")

    print("static site: pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
