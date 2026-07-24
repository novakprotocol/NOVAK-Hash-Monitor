"""Validate the scoped N-App manifest."""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


def check() -> list[str]:
    errors: list[str] = []
    path = ROOT / "app.manifest.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"app.manifest.json unreadable: {exc}"]

    required = {"schema_version", "app_id", "app_name", "description", "tier", "runtime", "security", "commands"}
    missing = required - data.keys()
    if missing:
        errors.append(f"missing top-level fields: {sorted(missing)}")
    if data.get("schema_version") != "n.app.manifest.v1":
        errors.append("schema_version must be n.app.manifest.v1")
    commands = data.get("commands")
    if not isinstance(commands, list) or not commands:
        errors.append("commands must be a non-empty list")
    else:
        ids = [item.get("id") for item in commands if isinstance(item, dict)]
        if any(not value for value in ids):
            errors.append("every command needs an id")
        if len(ids) != len(set(ids)):
            errors.append("command ids must be unique")
        for item in commands:
            if not isinstance(item, dict):
                errors.append("command entries must be objects")
                continue
            for field in ("title", "description", "risk", "mutates_state", "requires_approval", "authority_scope"):
                if field not in item:
                    errors.append(f"command {item.get('id', '<unknown>')} missing {field}")
    runtime = data.get("runtime", {})
    language = str(runtime.get("language", "")).strip().lower()
    if language == "java" or language.startswith("java "):
        errors.append("Java runtime is outside the project boundary")
    security = data.get("security", {})
    for field in ("local_first", "network", "secrets", "storage", "privacy"):
        if field not in security:
            errors.append(f"security missing {field}")
    if security.get("local_first") is not True:
        errors.append("security.local_first must be true")
    return errors


def main() -> int:
    errors = check()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("N-App manifest contract: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
