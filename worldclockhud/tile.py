"""TileClock widget — a single timezone card."""

from __future__ import annotations

from datetime import datetime

import pytz
from PyQt6 import QtGui, QtWidgets

from worldclockhud.constants import TILE_HEIGHT


class TileClock(QtWidgets.QFrame):
    """A single timezone tile showing the timezone name and current time."""

    def __init__(self, tz_name: str) -> None:
        super().__init__()
        self.tz_name = tz_name
        self.setStyleSheet(
            """
            QFrame {
                background: rgba(50, 50, 50, 180);
                border-radius: 12px;
            }
            QFrame:hover {
                background: rgba(70, 70, 70, 220);
            }
            """
        )
        self.setFixedHeight(TILE_HEIGHT)
        self.setMinimumWidth(220)

        main_layout = QtWidgets.QHBoxLayout()
        main_layout.setContentsMargins(10, 5, 10, 5)

        # Timezone name
        self.label_name = QtWidgets.QLabel(tz_name)
        self.label_name.setStyleSheet(
            "color: white; font-weight: 600; font-size: 14px;"
        )
        self.label_name.setFont(
            QtGui.QFont("Segoe UI", 10, QtGui.QFont.Weight.Bold)
        )
        main_layout.addWidget(self.label_name)
        main_layout.addStretch()

        # Current time
        self.label_time = QtWidgets.QLabel("00:00:00")
        self.label_time.setStyleSheet("color: white; font-size: 14px;")
        self.label_time.setFont(QtGui.QFont("Segoe UI", 11))
        main_layout.addWidget(self.label_time)

        self.setLayout(main_layout)

    def update_time(self) -> None:
        """Refresh the displayed time for this timezone."""
        tz = pytz.timezone(self.tz_name)
        now = datetime.now(tz)
        self.label_time.setText(now.strftime("%H:%M:%S"))
