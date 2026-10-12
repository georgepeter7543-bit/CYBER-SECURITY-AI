"""
Executive Stat Card Widget for Telemetry and Vulnerability Metrics
PETER CYBER SECURITY PROGRAM
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtGui import QFont

from app.core.config import CyberTheme


class CyberStatCard(QFrame):
    """
    Sleek dark metric card displaying executive telemetry or vulnerability counters.
    """
    def __init__(self, title: str, initial_value: str, subtext: str, accent_color: str = CyberTheme.COLOR_SCANNER, parent=None):
        super().__init__(parent)
        self.setProperty("class", "CyberCard")
        self.accent_color = accent_color
        self.setStyleSheet(f"""
            QFrame.CyberCard {{
                background-color: {CyberTheme.BG_CARD};
                border: 1px solid {CyberTheme.BORDER_DARK};
                border-top: 3px solid {self.accent_color};
                border-radius: 8px;
                padding: 10px;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(4)

        # Header row with title and indicator
        header_layout = QHBoxLayout()
        self.title_label = QLabel(title.upper())
        self.title_label.setStyleSheet(f"color: {CyberTheme.TEXT_MUTED}; font-size: 11px; font-weight: 700; letter-spacing: 0.8px;")
        header_layout.addWidget(self.title_label)

        self.dot_indicator = QLabel("●")
        self.dot_indicator.setStyleSheet(f"color: {self.accent_color}; font-size: 10px;")
        header_layout.addStretch()
        header_layout.addWidget(self.dot_indicator)
        layout.addLayout(header_layout)

        # Big Value Display
        self.value_label = QLabel(initial_value)
        self.value_label.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        self.value_label.setStyleSheet("color: #FFFFFF;")
        layout.addWidget(self.value_label)

        # Subtext / Metadata
        self.subtext_label = QLabel(subtext)
        self.subtext_label.setStyleSheet(f"color: {CyberTheme.TEXT_DARK}; font-size: 11px; font-weight: 500;")
        layout.addWidget(self.subtext_label)

    def set_value(self, value: str, subtext: str = None):
        self.value_label.setText(value)
        if subtext is not None:
            self.subtext_label.setText(subtext)

    def set_accent_color(self, color: str):
        self.accent_color = color
        self.dot_indicator.setStyleSheet(f"color: {color}; font-size: 10px;")
        self.setStyleSheet(f"""
            QFrame.CyberCard {{
                background-color: {CyberTheme.BG_CARD};
                border: 1px solid {CyberTheme.BORDER_DARK};
                border-top: 3px solid {color};
                border-radius: 8px;
                padding: 10px;
            }}
        """)
