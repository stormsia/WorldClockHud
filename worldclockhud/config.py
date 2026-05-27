"""Config load/save for WorldClockHud."""

from __future__ import annotations

import json
import logging
import os
from typing import Any

from worldclockhud.constants import DEFAULT_TIMEZONES

logger = logging.getLogger(__name__)

APP_DIR: str = os.path.join(os.getenv("APPDATA", ""), "WorldClockHud")
CONFIG_PATH: str = os.path.join(APP_DIR, "config.json")


def ensure_config_dir() -> None:
    """Create the config directory if it does not exist."""
    os.makedirs(APP_DIR, exist_ok=True)


def load_config() -> dict[str, Any]:
    """Load configuration from disk, returning an empty dict on failure."""
    ensure_config_dir()
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as exc:
            logger.warning("Failed to load config: %s", exc)
    return {}


def save_config(data: dict[str, Any]) -> None:
    """Persist configuration to disk."""
    ensure_config_dir()
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as exc:
        logger.error("Failed to save config: %s", exc)


def default_config() -> dict[str, Any]:
    """Return the default configuration dictionary."""
    return {
        "timezones": DEFAULT_TIMEZONES,
        "position": [50, 50],
        "always_on_top": True,
        "pin_to_desktop": False,
    }
