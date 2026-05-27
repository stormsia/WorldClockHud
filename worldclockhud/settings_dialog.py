"""Settings dialog for managing timezones."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytz
from PyQt6 import QtCore, QtWidgets

if TYPE_CHECKING:
    from worldclockhud.hud import HUDClock


class SettingsDialog(QtWidgets.QDialog):
    """Dialog for adding/removing timezone tiles."""

    def __init__(self, hud: HUDClock) -> None:
        super().__init__()
        self.hud = hud
        self.setWindowTitle("Settings")
        self.setFixedSize(300, 320)
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.bg = QtWidgets.QFrame(self)
        self.bg.setGeometry(0, 0, 300, 320)
        self.bg.setStyleSheet(
            """
            QFrame {
                background: rgba(40, 40, 40, 200);
                border-radius: 15px;
            }
            """
        )

        self.main_layout = QtWidgets.QVBoxLayout(self.bg)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)

        # Header
        header_layout = QtWidgets.QHBoxLayout()
        title = QtWidgets.QLabel("TZ Settings")
        title.setStyleSheet("color:white; font-size:16px; font-weight:bold;")
        header_layout.addWidget(title)
        header_layout.addStretch()

        close_btn = QtWidgets.QPushButton("×")
        close_btn.setFixedSize(20, 20)
        close_btn.setStyleSheet(
            """
            QPushButton {
                background: rgba(200,50,50,0.8);
                color:white;
                border:none;
                border-radius:10px;
                font-weight:bold;
            }
            QPushButton:hover { background: rgba(255,50,50,1); }
            """
        )
        close_btn.clicked.connect(self.close)
        header_layout.addWidget(close_btn)
        self.main_layout.addLayout(header_layout)

        # Timezone cards container
        self.cards_container = QtWidgets.QWidget()
        self.cards_layout = QtWidgets.QVBoxLayout(self.cards_container)
        self.cards_layout.setSpacing(5)
        self.main_layout.addWidget(self.cards_container)
        self._refresh_cards()

        # Add timezone row
        add_layout = QtWidgets.QHBoxLayout()
        self.combo_tz = QtWidgets.QComboBox()
        self.combo_tz.setStyleSheet(
            """
            QComboBox {
                border: 1px solid rgba(255,255,255,0.3);
                border-radius: 5px;
                padding: 3px;
                color: white;
                background: rgba(255,255,255,0.05);
            }
            QComboBox QAbstractItemView {
                background: rgba(50,50,50,220);
                selection-background-color: #00aaff;
                color: white;
            }
            """
        )
        self._populate_combobox()

        add_btn = QtWidgets.QPushButton("Add")
        add_btn.setStyleSheet(
            """
            QPushButton {
                background-color: rgba(0,170,255,0.7);
                color: white;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover { background-color: rgba(0,170,255,1); }
            """
        )
        add_btn.clicked.connect(self._add_timezone)
        add_layout.addWidget(self.combo_tz)
        add_layout.addWidget(add_btn)
        self.main_layout.addLayout(add_layout)

    def _populate_combobox(self) -> None:
        self.combo_tz.clear()
        for tz in sorted(pytz.all_timezones):
            self.combo_tz.addItem(tz)
            if tz in self.hud.tiles:
                index = self.combo_tz.findText(tz)
                self.combo_tz.model().item(index).setEnabled(False)

    def _refresh_cards(self) -> None:
        for i in reversed(range(self.cards_layout.count())):
            w = self.cards_layout.itemAt(i).widget()
            if w:
                w.setParent(None)
        for tz in self.hud.tiles:
            card = QtWidgets.QFrame()
            card.setStyleSheet(
                """
                QFrame {
                    background: rgba(60,60,60,180);
                    border-radius: 8px;
                }
                QFrame:hover { background: rgba(80,80,80,200); }
                """
            )
            card_layout = QtWidgets.QHBoxLayout(card)
            label = QtWidgets.QLabel(tz)
            label.setStyleSheet("color:white; font-weight:bold;")
            remove_btn = QtWidgets.QPushButton("×")
            remove_btn.setStyleSheet(
                """
                QPushButton {
                    background: rgba(255,50,50,0.8);
                    border-radius: 6px;
                    color:white;
                    font-weight:bold;
                    padding:2px 5px;
                }
                QPushButton:hover { background: rgba(255,50,50,1); }
                """
            )
            remove_btn.clicked.connect(
                lambda _, t=tz: self._remove_timezone(t)
            )
            card_layout.addWidget(label)
            card_layout.addStretch()
            card_layout.addWidget(remove_btn)
            self.cards_layout.addWidget(card)

    def _add_timezone(self) -> None:
        tz = self.combo_tz.currentText()
        if tz and tz not in self.hud.tiles:
            self.hud.add_tile(tz)
            self.hud.adjust_height()
            self.hud.save_state()
            self._refresh_cards()
            self._populate_combobox()

    def _remove_timezone(self, tz: str) -> None:
        self.hud.remove_tile(tz)
        self.hud.adjust_height()
        self.hud.save_state()
        self._refresh_cards()
        self._populate_combobox()
