"""
Global Threat Map Module (Color Accent: Tech Neon Blue - #00D2FF)
PETER CYBER SECURITY PROGRAM
"""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QSplitter,
    QFrame, QComboBox
)

from app.core.config import CyberTheme, REGIONS
from app.ui.widgets.threat_canvas import ThreatCanvasWidget


class ThreatMapModule(QWidget):
    """
    Module 3: Global Threat Map & Geospatial Attack Arc Telemetry.
    Theme: Tech Neon Blue (#00D2FF).
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_stream_paused = False
        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(18, 14, 18, 14)
        main_layout.setSpacing(10)

        # 1. Header & Region Filter Controls
        header = QHBoxLayout()
        title_box = QVBoxLayout()
        title = QLabel("GLOBAL THREAT INTELLIGENCE & ATTACK MAP")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {CyberTheme.COLOR_THREAT_MAP}; letter-spacing: 0.5px;")

        subtitle = QLabel("Real-time distributed telemetry, orbital vector arcs, and East Africa defense node monitoring.")
        subtitle.setStyleSheet(f"color: {CyberTheme.TEXT_MUTED}; font-size: 12px;")
        title_box.addWidget(title)
        title_box.addWidget(subtitle)
        header.addLayout(title_box)
        header.addStretch()

        # Region Filter Buttons
        filter_box = QHBoxLayout()
        filter_box.setSpacing(6)
        filter_lbl = QLabel("SECTOR VIEW:")
        filter_lbl.setStyleSheet(f"color: {CyberTheme.TEXT_MUTED}; font-size: 11px; font-weight: bold;")
        filter_box.addWidget(filter_lbl)

        self.region_buttons = {}
        for reg in REGIONS:
            btn = QPushButton(reg)
            btn.setProperty("class", "CyberButton")
            btn.setCheckable(True)
            if reg == "WORLD":
                btn.setChecked(True)
                btn.setStyleSheet(f"background-color: rgba(0, 210, 255, 0.2); color: #FFFFFF; border-color: {CyberTheme.COLOR_THREAT_MAP};")

            btn.clicked.connect(lambda checked, r=reg: self._on_region_selected(r))
            filter_box.addWidget(btn)
            self.region_buttons[reg] = btn

        header.addLayout(filter_box)
        main_layout.addLayout(header)

        # 2. Main Content Splitter: Canvas on Top, Streaming Feed on Bottom
        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.setStyleSheet(f"""
            QSplitter::handle {{
                background-color: {CyberTheme.BORDER_MID};
                height: 3px;
            }}
        """)

        # Custom 2D Vector Threat Canvas
        self.canvas = ThreatCanvasWidget()
        self.canvas.threat_intercepted.connect(self._on_threat_intercepted)
        splitter.addWidget(self.canvas)

        # Bottom Panel: Live Streaming Feed
        feed_panel = QFrame()
        feed_panel.setStyleSheet(f"""
            QFrame {{
                background-color: {CyberTheme.BG_SURFACE};
                border: 1px solid {CyberTheme.BORDER_DARK};
                border-radius: 6px;
            }}
        """)
        feed_layout = QVBoxLayout(feed_panel)
        feed_layout.setContentsMargins(12, 10, 12, 10)
        feed_layout.setSpacing(8)

        # Feed Controls Header
        feed_header = QHBoxLayout()
        feed_title = QLabel("LIVE INCOMING THREAT FEED (GLOBAL SENSORS)")
        feed_title.setStyleSheet(f"color: {CyberTheme.COLOR_THREAT_MAP}; font-size: 12px; font-weight: 700; letter-spacing: 0.5px;")
        feed_header.addWidget(feed_title)

        feed_status = QLabel("● STREAM ACTIVE [42.6 EPS]")
        feed_status.setStyleSheet("color: #00FF66; font-size: 11px; font-weight: bold; font-family: monospace;")
        feed_header.addWidget(feed_status)
        feed_header.addStretch()

        self.btn_pause = QPushButton("⏸ Pause Feed")
        self.btn_pause.setProperty("class", "CyberButton")
        self.btn_pause.clicked.connect(self._toggle_pause)
        feed_header.addWidget(self.btn_pause)

        self.btn_clear = QPushButton("🗑 Clear Feed")
        self.btn_clear.setProperty("class", "CyberButton")
        self.btn_clear.clicked.connect(self._clear_feed)
        feed_header.addWidget(self.btn_clear)

        feed_layout.addLayout(feed_header)

        # Live Threat Table
        self.feed_table = QTableWidget(0, 6)
        self.feed_table.setHorizontalHeaderLabels([
            "TIMESTAMP", "ORIGIN NODE", "TARGET NODE", "THREAT VECTOR", "SEVERITY", "DEFENSE ACTION"
        ])
        self.feed_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.feed_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.feed_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.feed_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.feed_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.feed_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        self.feed_table.verticalHeader().setVisible(False)
        self.feed_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.feed_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        feed_layout.addWidget(self.feed_table)

        splitter.addWidget(feed_panel)
        splitter.setSizes([380, 240])

        main_layout.addWidget(splitter)

    def _on_region_selected(self, region: str):
        for reg, btn in self.region_buttons.items():
            if reg == region:
                btn.setChecked(True)
                btn.setStyleSheet(f"background-color: rgba(0, 210, 255, 0.2); color: #FFFFFF; border-color: {CyberTheme.COLOR_THREAT_MAP};")
            else:
                btn.setChecked(False)
                btn.setStyleSheet("")

        self.canvas.set_region_filter(region)

    def _on_threat_intercepted(self, data: dict):
        if self.is_stream_paused:
            return

        # Insert at top of table (descending order)
        self.feed_table.insertRow(0)

        t_item = QTableWidgetItem(f"  {data['timestamp']}")
        t_item.setFont(QFont("Consolas", 10))
        t_item.setForeground(QColor(CyberTheme.TEXT_MUTED))

        o_item = QTableWidgetItem(data['origin'])
        tg_item = QTableWidgetItem(data['target'])
        v_item = QTableWidgetItem(data['vector'])

        # Highlight Arusha specifically in table
        if "ARUSHA" in data['target'].upper() or "ARUSHA" in data['origin'].upper():
            tg_item.setForeground(QColor(CyberTheme.COLOR_SCANNER))
            o_item.setForeground(QColor(CyberTheme.COLOR_SCANNER))

        sev_item = QTableWidgetItem(f" {data['severity']} ")
        sev_item.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        if data['severity'] == "CRITICAL":
            sev_item.setForeground(QColor(CyberTheme.SEVERITY_CRITICAL))
        elif data['severity'] == "HIGH":
            sev_item.setForeground(QColor(CyberTheme.SEVERITY_HIGH))
        elif data['severity'] == "MEDIUM":
            sev_item.setForeground(QColor(CyberTheme.SEVERITY_MEDIUM))
        else:
            sev_item.setForeground(QColor(CyberTheme.SEVERITY_LOW))

        act_item = QTableWidgetItem(data['mitigation'])
        act_item.setForeground(QColor("#A7F3D0" if "BLOCKED" in data['mitigation'] else CyberTheme.TEXT_MUTED))

        self.feed_table.setItem(0, 0, t_item)
        self.feed_table.setItem(0, 1, o_item)
        self.feed_table.setItem(0, 2, tg_item)
        self.feed_table.setItem(0, 3, v_item)
        self.feed_table.setItem(0, 4, sev_item)
        self.feed_table.setItem(0, 5, act_item)

        # Cap table rows at 100 for memory efficiency
        if self.feed_table.rowCount() > 100:
            self.feed_table.removeRow(100)

    def _toggle_pause(self):
        self.is_stream_paused = not self.is_stream_paused
        if self.is_stream_paused:
            self.btn_pause.setText("▶ Resume Feed")
        else:
            self.btn_pause.setText("⏸ Pause Feed")

    def _clear_feed(self):
        self.feed_table.setRowCount(0)
