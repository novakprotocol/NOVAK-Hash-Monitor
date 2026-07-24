#!/usr/bin/env python3
"""Validate the scoped N-App manifest without external dependencies."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "app.manifest.json"


def fail(message: str) -> None:
    raise SystemExit(f"N-App contract: {message}")


def main() -> int:
    try:
        payload = json.loads(PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(str(exc))

    if payload.get("schema_version") != "n.app.manifest.v1":
        fail("schema_version must be n.app.manifest.v1")
    if payload.get("app_id") != "com.novak.password_threat_lab":
        fail("unexpected app_id")
    if payload.get("tier") != "tier3-reference-candidate":
        fail("tier must preserve candidate status")

    runtime = payload.get("runtime")
    if not isinstance(runtime, dict):
        fail("runtime object missing")
    if runtime.get("entrypoint") != "python serve.py":
        fail("runtime entrypoint must be python serve.py")
    if runtime.get("third_party_runtime_dependencies") not in ([], "none"):
        fail("third-party runtime dependencies are not allowed")

    security = payload.get("security")
    if not isinstance(security, dict):
        fail("security object missing")
    required_security = {
        "local_first": True,
        "secrets": "none",
        "browser_storage": "none",
        "submitted_value_transmission": "none",
    }
    for key, expected in required_security.items():
        if security.get(key) != expected:
            fail(f"security.{key} must equal {expected!r}")

    commands = payload.get("commands")
    if not isinstance(commands, list) or not commands:
        fail("commands must be a non-empty list")
    command_ids = {item.get("id") for item in commands if isinstance(item, dict)}
    expected_ids = {"lab.estimate", "lab.select_profile", "lab.clear", "app.about"}
    if command_ids != expected_ids:
        fail(f"command IDs must equal {sorted(expected_ids)}")
    for command in commands:
        for field in ("id", "title", "description", "risk", "authority_scope"):
            if not command.get(field):
                fail(f"command missing {field}")
        if command.get("risk") != "low":
            fail("all scoped commands must remain low risk")

    claims = payload.get("claim_boundaries")
    if not isinstance(claims, list) or len(claims) < 3:
        fail("claim_boundaries must be explicit")

    print("N-App contract: pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
