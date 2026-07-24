"""Validate the scoped app.surface.json contract."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def check() -> list[str]:
    errors: list[str] = []
    try:
        manifest = json.loads((ROOT / "app.manifest.json").read_text(encoding="utf-8"))
        surface = json.loads((ROOT / "app.surface.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"manifest unreadable: {exc}"]

    if surface.get("schema") != "n.surface.v1":
        errors.append("surface schema must be n.surface.v1")
    if surface.get("app_id") != manifest.get("app_id"):
        errors.append("surface app_id must match app manifest")
    manifest_ids = {item["id"] for item in manifest.get("commands", []) if isinstance(item, dict) and item.get("id")}
    surface_commands = surface.get("commands", [])
    surface_ids = {item.get("id") for item in surface_commands if isinstance(item, dict)}
    if surface_ids != manifest_ids:
        errors.append(f"surface command ids differ: manifest={sorted(manifest_ids)} surface={sorted(surface_ids)}")
    for item in surface_commands:
        if not isinstance(item, dict):
            errors.append("surface commands must be objects")
            continue
        if not item.get("surfaces"):
            errors.append(f"surface command {item.get('id', '<unknown>')} has no visible surface")
    return errors


def main() -> int:
    errors = check()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("N-App surface contract: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
