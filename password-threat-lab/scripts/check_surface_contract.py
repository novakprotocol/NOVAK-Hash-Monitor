#!/usr/bin/env python3
"""Validate that visible surface metadata matches the app manifest."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: Path) -> dict[str, object]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"surface contract: {path.name}: {exc}") from exc
    if not isinstance(payload, dict):
        raise SystemExit(f"surface contract: {path.name} must contain an object")
    return payload


def main() -> int:
    manifest = load(ROOT / "app.manifest.json")
    surface = load(ROOT / "app.surface.json")

    if surface.get("schema") != "n.surface.v1":
        raise SystemExit("surface contract: schema must be n.surface.v1")
    if surface.get("app_id") != manifest.get("app_id"):
        raise SystemExit("surface contract: app_id differs from app.manifest.json")

    manifest_ids = {item["id"] for item in manifest["commands"]}
    commands = surface.get("commands")
    if not isinstance(commands, list):
        raise SystemExit("surface contract: commands must be a list")
    surface_ids = {item.get("id") for item in commands if isinstance(item, dict)}
    if surface_ids != manifest_ids:
        raise SystemExit("surface contract: visible command IDs must match manifest")

    for command in commands:
        if command.get("risk") != "low":
            raise SystemExit("surface contract: all commands must remain low risk")
        surfaces = command.get("surfaces")
        if not isinstance(surfaces, list) or not surfaces:
            raise SystemExit(f"surface contract: {command.get('id')} has no visible surface")
        for item in surfaces:
            if item.get("kind") not in {"web", "launcher", "menu", "palette"}:
                raise SystemExit(f"surface contract: unsupported kind {item.get('kind')!r}")

    print("surface contract: pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
