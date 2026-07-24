"""Static privacy, dependency, and asset checks for the Pages surface."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]


class SurfaceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.scripts: list[dict[str, str]] = []
        self.stylesheets: list[dict[str, str]] = []
        self.links: list[str] = []
        self.inputs: list[dict[str, str]] = []
        self.csp = ""
        self.forms = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value or "" for key, value in attrs}
        if tag == "script":
            self.scripts.append(values)
        elif tag == "link" and values.get("rel") == "stylesheet":
            self.stylesheets.append(values)
        elif tag == "a" and values.get("href"):
            self.links.append(values["href"])
        elif tag == "input":
            self.inputs.append(values)
        elif tag == "meta" and values.get("http-equiv", "").lower() == "content-security-policy":
            self.csp = values.get("content", "")
        elif tag == "form":
            self.forms += 1


def is_external(value: str) -> bool:
    return urlparse(value).scheme in {"http", "https", "//"}


def check() -> list[str]:
    errors: list[str] = []
    index_path = ROOT / "index.html"
    html = index_path.read_text(encoding="utf-8")
    parser = SurfaceParser()
    parser.feed(html)

    if parser.forms:
        errors.append("the analyzer must not use a submitting form")
    if not parser.csp:
        errors.append("Content Security Policy meta tag is missing")
    else:
        for token in ("default-src 'self'", "script-src 'self'", "object-src 'none'", "form-action 'none'"):
            if token not in parser.csp:
                errors.append(f"CSP missing {token}")
        if "unsafe-inline" in parser.csp or "unsafe-eval" in parser.csp:
            errors.append("CSP must not permit unsafe-inline or unsafe-eval")

    for script in parser.scripts:
        source = script.get("src")
        if not source:
            errors.append("inline script detected")
        elif is_external(source):
            errors.append(f"external script detected: {source}")
        elif not (ROOT / source).is_file():
            errors.append(f"script asset missing: {source}")

    for stylesheet in parser.stylesheets:
        href = stylesheet.get("href")
        if not href:
            errors.append("stylesheet href missing")
        elif is_external(href):
            errors.append(f"external stylesheet detected: {href}")
        elif not (ROOT / href).is_file():
            errors.append(f"stylesheet asset missing: {href}")

    password_inputs = [item for item in parser.inputs if item.get("id") == "passwordInput"]
    if len(password_inputs) != 1:
        errors.append("exactly one passwordInput is required")
    else:
        item = password_inputs[0]
        if item.get("type") != "password":
            errors.append("passwordInput must default to type=password")
        if item.get("autocomplete") != "new-password":
            errors.append("passwordInput must use autocomplete=new-password")
        if item.get("maxlength") != "256":
            errors.append("passwordInput maxlength contract changed")

    allowed_external_hosts = {"pages.nist.gov", "csrc.nist.gov", "www.nist.gov", "www.nccoe.nist.gov"}
    for link in parser.links:
        if is_external(link):
            parsed = urlparse(link)
            if parsed.scheme != "https":
                errors.append(f"non-HTTPS source link: {link}")
            if parsed.hostname not in allowed_external_hosts:
                errors.append(f"unapproved external host: {parsed.hostname}")

    if re.search(r"<style\b", html, flags=re.IGNORECASE):
        errors.append("inline style block detected")
    css = "\n".join(
        (ROOT / stylesheet["href"]).read_text(encoding="utf-8")
        for stylesheet in parser.stylesheets
        if stylesheet.get("href") and not is_external(stylesheet["href"])
    )
    if re.search(r"@import\s", css, flags=re.IGNORECASE):
        errors.append("CSS @import is not allowed")
    if re.search(r"url\([\"']?https?://", css, flags=re.IGNORECASE):
        errors.append("external CSS URL detected")

    javascript = "\n".join(
        (ROOT / "assets" / name).read_text(encoding="utf-8")
        for name in ("estimator.js", "app.js")
    )
    banned = {
        "localStorage": "persistent local storage",
        "sessionStorage": "session storage",
        "sendBeacon": "beacon transmission",
        "XMLHttpRequest": "XMLHttpRequest",
        "WebSocket": "WebSocket",
        "document.cookie": "cookies",
        "console.log": "console logging",
    }
    for token, label in banned.items():
        if token in javascript:
            errors.append(f"{label} detected in browser code")
    if 'fetch("data/attack-profiles.json"' not in javascript:
        errors.append("same-origin attack-profile load contract missing")
    if "pagehide" not in javascript:
        errors.append("pagehide memory-clearing hook missing")
    return errors


def main() -> int:
    errors = check()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Static privacy and dependency contract: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
