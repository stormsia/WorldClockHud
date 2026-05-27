"""System tray icon with Always-on-Top toggle."""

from __future__ import annotations

import os
import sys
from typing import TYPE_CHECKING

from PyQt6 import QtGui, QtWidgets

if TYPE_CHECKING:
    from worldclockhud.hud import HUDClock


def resource_path(relative: str) -> str:
    """Return absolute path to a resource, works for PyInstaller bundles."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(os.path.abspath("."), relative)


class SystemTray(QtWidgets.QSystemTrayIcon):
    """Tray icon with show/hide, always-on-top toggle, settings, and exit."""

    def __init__(self, hud: HUDClock) -> None:
        icon = QtGui.QIcon(resource_path("icon.ico"))
        super().__init__(icon)
        self.hud = hud

        menu = QtWidgets.QMenu()

        # Show / Hide
        show_action = menu.addAction("Show/Hide HUD")
        show_action.triggered.connect(self.hud.toggle_visibility)

        # Window Modes
        mode_group = QtGui.QActionGroup(menu)
        mode_group.setExclusive(True)

        self.aot_action = QtGui.QAction("Always on Top", menu)
        self.aot_action.setCheckable(True)
        self.aot_action.setChecked(self.hud.always_on_top)
        self.aot_action.triggered.connect(lambda: self.hud.set_window_mode("top"))
        mode_group.addAction(self.aot_action)
        menu.addAction(self.aot_action)

        self.pin_action = QtGui.QAction("Pin to Desktop", menu)
        self.pin_action.setCheckable(True)
        self.pin_action.setChecked(self.hud.pin_to_desktop)
        self.pin_action.triggered.connect(lambda: self.hud.set_window_mode("desktop"))
        mode_group.addAction(self.pin_action)
        menu.addAction(self.pin_action)

        self.normal_action = QtGui.QAction("Normal Window", menu)
        self.normal_action.setCheckable(True)
        self.normal_action.setChecked(not self.hud.always_on_top and not self.hud.pin_to_desktop)
        self.normal_action.triggered.connect(lambda: self.hud.set_window_mode("normal"))
        mode_group.addAction(self.normal_action)
        menu.addAction(self.normal_action)

        menu.addSeparator()

        # Settings
        settings_action = menu.addAction("Settings")
        settings_action.triggered.connect(self.hud.open_settings)

        menu.addSeparator()

        # Exit
        quit_action = menu.addAction("Exit")
        quit_action.triggered.connect(QtWidgets.QApplication.quit)

        self.setContextMenu(menu)
        self.setToolTip("WorldClockHud")
        self.activated.connect(self._icon_clicked)
        self.show()

    def _icon_clicked(self, reason: QtWidgets.QSystemTrayIcon.ActivationReason) -> None:
        if reason == QtWidgets.QSystemTrayIcon.ActivationReason.Trigger:
            self.hud.toggle_visibility()
