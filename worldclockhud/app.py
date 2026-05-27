"""Application entry point with single-instance guard."""

from __future__ import annotations

import logging
import sys

import psutil
from PyQt6 import QtWidgets

from worldclockhud.hud import HUDClock
from worldclockhud.tray import SystemTray

logger = logging.getLogger("worldclockhud")

PROCESS_NAME = "WorldClockHud.exe"
MAX_INSTANCES = 2  # pyinstaller spawns a child process


def _is_already_running() -> bool:
    """Return True if another instance of the app is already running."""
    count = 0
    for proc in psutil.process_iter(["name"]):
        if proc.info["name"] == PROCESS_NAME:
            count += 1
    return count > MAX_INSTANCES


def main() -> None:
    """Launch WorldClockHud."""
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    )

    if _is_already_running():
        logger.info("Another instance is already running. Exiting.")
        sys.exit(0)

    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    hud = HUDClock()
    tray = SystemTray(hud)  # noqa: F841 — prevent garbage collection

    sys.exit(app.exec())
