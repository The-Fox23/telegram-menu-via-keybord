"""Telegram Menu integration version."""
from __future__ import annotations

import json
from pathlib import Path

_MANIFEST = Path(__file__).with_name("manifest.json")
VERSION = json.loads(_MANIFEST.read_text(encoding="utf-8"))["version"]
