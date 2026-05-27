"""HUDClock widget — the main transparent clock overlay."""

from __future__ import annotations

import ctypes
import logging
from typing import Optional

from PyQt6 import QtCore, QtWidgets

from worldclockhud.config import load_config, save_config
from worldclockhud.constants import (
    DEFAULT_TIMEZONES,
    DEFAULT_WIDTH,
    DEFAULT_X,
    DEFAULT_Y,
    TILE_HEIGHT,
)
from worldclockhud.tile import TileClock

logger = logging.getLogger(__name__)

# Windows constants for SetWindowPos
_HWND_TOPMOST = -1
_HWND_BOTTOM = 1
_SWP_NOMOVE = 0x0002
_SWP_NOSIZE = 0x0001
_SWP_FLAGS = _SWP_NOMOVE | _SWP_NOSIZE


class HUDClock(QtWidgets.QWidget):
    """Main HUD window displaying timezone tiles."""

    def __init__(self) -> None:
        super().__init__()
        self.config = load_config()
        self.always_on_top: bool = self.config.get("always_on_top", True)
        self.pin_to_desktop: bool = self.config.get("pin_to_desktop", False)

        self.setWindowTitle("WorldClockHud")
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
            | QtCore.Qt.WindowType.Tool
        )
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(DEFAULT_X, DEFAULT_Y, DEFAULT_WIDTH, 200)

        # Restore position from config
        pos = self.config.get("position", [DEFAULT_X, DEFAULT_Y])
        self.move(pos[0], pos[1])

        # Glass/Mica background frame
        self.bg = QtWidgets.QFrame(self)
        self.bg.setStyleSheet(
            """
            QFrame {
                background: rgba(30, 30, 30, 200);
                border-radius: 15px;
            }
            """
        )
        self.bg.setGeometry(0, 0, DEFAULT_WIDTH, 200)

        # Layout for timezone tiles
        self.main_layout = QtWidgets.QVBoxLayout(self.bg)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(8)

        self.tiles: dict[str, TileClock] = {}
        timezones = self.config.get("timezones", DEFAULT_TIMEZONES)
        for tz in timezones:
            self.add_tile(tz)

        # Update timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_tiles)
        self.timer.start(1000)
        self.update_tiles()
        self.adjust_height()

        # Drag support
        self._drag_offset: Optional[QtCore.QPointF] = None
        self.bg.mousePressEvent = self._mouse_press
        self.bg.mouseMoveEvent = self._mouse_move

        # Context menu
        self.bg.setContextMenuPolicy(
            QtCore.Qt.ContextMenuPolicy.CustomContextMenu
        )
        self.bg.customContextMenuRequested.connect(self._open_context_menu)

        # Apply initial window level
        self.apply_window_level()

    # ------------------------------------------------------------------
    # Window level (Always-on-Top / Desktop)
    # ------------------------------------------------------------------

    def apply_window_level(self) -> None:
        """Set window z-order based on always_on_top flag."""
        flags = self.windowFlags()
        if self.always_on_top:
            flags |= QtCore.Qt.WindowType.WindowStaysOnTopHint
        else:
            flags &= ~QtCore.Qt.WindowType.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self.show()

        hwnd = int(self.winId())
        if self.always_on_top:
            target = _HWND_TOPMOST
        elif self.pin_to_desktop:
            target = _HWND_BOTTOM
        else:
            target = -2  # _HWND_NOTOPMOST

        ctypes.windll.user32.SetWindowPos(
            hwnd, target, 0, 0, 0, 0, _SWP_FLAGS
        )
        logger.debug("Window level set, AOT: %s, Pin: %s", self.always_on_top, self.pin_to_desktop)

    def set_window_mode(self, mode: str) -> None:
        """Set the window mode to 'top', 'desktop', or 'normal'."""
        self.always_on_top = (mode == "top")
        self.pin_to_desktop = (mode == "desktop")
        self.apply_window_level()
        self.save_state()

    # ------------------------------------------------------------------
    # Drag
    # ------------------------------------------------------------------

    def _mouse_press(self, event: QtCore.QEvent) -> None:
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self._drag_offset = event.position()

    def _mouse_move(self, event: QtCore.QEvent) -> None:
        if self._drag_offset:
            x = int(event.globalPosition().x() - self._drag_offset.x())
            y = int(event.globalPosition().y() - self._drag_offset.y())
            self.move(x, y)
            self.save_state()

    # ------------------------------------------------------------------
    # Tile management
    # ------------------------------------------------------------------

    def add_tile(self, tz: str) -> None:
        if tz not in self.tiles:
            tile = TileClock(tz)
            self.main_layout.addWidget(tile)
            self.tiles[tz] = tile

    def remove_tile(self, tz: str) -> None:
        if tz in self.tiles:
            tile = self.tiles.pop(tz)
            self.main_layout.removeWidget(tile)
            tile.deleteLater()

    def update_tiles(self) -> None:
        for tile in self.tiles.values():
            tile.update_time()
        self.adjust_height()

    def adjust_height(self) -> None:
        spacing = self.main_layout.spacing()
        margins = self.main_layout.contentsMargins()
        margin = margins.top() + margins.bottom()
        count = len(self.tiles)
        height = count * TILE_HEIGHT + max(0, count - 1) * spacing + margin
        self.setFixedHeight(height)
        self.bg.setFixedHeight(height)

    # ------------------------------------------------------------------
    # Context menu
    # ------------------------------------------------------------------

    def _open_context_menu(self, pos: QtCore.QPoint) -> None:
        from worldclockhud.settings_dialog import SettingsDialog

        menu = QtWidgets.QMenu()
        settings_action = menu.addAction("Settings")
        settings_action.triggered.connect(lambda: SettingsDialog(self).exec())
        toggle_action = menu.addAction("Collapse/Expand")
        toggle_action.triggered.connect(self.toggle_visibility)
        quit_action = menu.addAction("Exit")
        quit_action.triggered.connect(QtWidgets.QApplication.quit)
        menu.exec(self.mapToGlobal(pos))

    def open_settings(self) -> None:
        from worldclockhud.settings_dialog import SettingsDialog
        SettingsDialog(self).exec()

    def toggle_visibility(self) -> None:
        if self.isVisible():
            self.hide()
        else:
            self.show()
            self.raise_()

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def save_state(self) -> None:
        data = {
            "timezones": list(self.tiles.keys()),
            "position": [self.x(), self.y()],
            "always_on_top": self.always_on_top,
            "pin_to_desktop": self.pin_to_desktop,
        }
        save_config(data)
