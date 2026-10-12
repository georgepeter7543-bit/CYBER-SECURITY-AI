"""
Main Desktop Application Window & Navigation Hub
PETER CYBER SECURITY PROGRAM
"""

import time
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon, QFont, QColor
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QStackedWidget, QFrame, QStatusBar, QProgressBar
)

from app.core.config import APP_TITLE, APP_SUBTITLE, APP_VERSION, CyberTheme
from app.core.system_monitor import SystemMonitorWorker
from app.ui.modules.virus_scanner import VirusScannerModule
from app.ui.modules.threat_map import ThreatMapModule
from app.ui.modules.ai_assistant import AIAssistantModule
from app.ui.modules.vulnerability_view import VulnerabilityOverviewModule


class MainWindow(QMainWindow):
    """
    Main application shell implementing top navigation, live telemetry strip,
    and modular tab switching across cybersecurity domains.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_TITLE} - {APP_VERSION}")
        self.resize(1340, 880)
        self.setMinimumSize(1100, 720)

        # Launch non-blocking telemetry worker thread
        self.monitor_worker = SystemMonitorWorker(interval_ms=1000, parent=self)
        self.monitor_worker.telemetry_updated.connect(self._on_telemetry_updated)
        self.monitor_worker.start()

        self._start_time = time.time()
        self._init_ui()

        # Uptime ticker timer
        self.uptime_timer = QTimer(self)
        self.uptime_timer.timeout.connect(self._update_uptime)
        self.uptime_timer.start(1000)

    def _init_ui(self):
        # Central Root Container
        self.central_widget = QWidget()
        self.central_widget.setObjectName("CentralWidget")
        self.setCentralWidget(self.central_widget)

        root_layout = QVBoxLayout(self.central_widget)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # 1. TOP NAVIGATION BAR
        self.top_nav = self._create_top_navigation_bar()
        root_layout.addWidget(self.top_nav)

        # 2. MODULAR STACKED CONTAINER
        self.stacked_widget = QStackedWidget()

        # Instantiate the 4 Core Modules
        self.mod_virus_scanner = VirusScannerModule()
        self.mod_threat_map = ThreatMapModule()
        self.mod_ai_assistant = AIAssistantModule()
        self.mod_vulnerability = VulnerabilityOverviewModule()

        self.stacked_widget.addWidget(self.mod_virus_scanner)    # Index 0
        self.stacked_widget.addWidget(self.mod_threat_map)       # Index 1
        self.stacked_widget.addWidget(self.mod_ai_assistant)      # Index 2
        self.stacked_widget.addWidget(self.mod_vulnerability)     # Index 3

        root_layout.addWidget(self.stacked_widget, stretch=1)

        # 3. NATIVE STATUS BAR
        self._setup_status_bar()

        # Set default active module (Virus Scanner)
        self._switch_tab(0)

    def _create_top_navigation_bar(self) -> QFrame:
        nav_frame = QFrame()
        nav_frame.setObjectName("TopNavBar")
        nav_layout = QVBoxLayout(nav_frame)
        nav_layout.setContentsMargins(16, 8, 16, 6)
        nav_layout.setSpacing(8)

        # Upper Row: Title Branding + Live Telemetry Indicators
        upper_row = QHBoxLayout()
        upper_row.setSpacing(14)

        # Branding
        title_box = QVBoxLayout()
        title_box.setSpacing(1)

        prog_title = QLabel("PETER CYBER SECURITY PROGRAM")
        prog_title.setFont(QFont("Segoe UI", 15, QFont.Weight.Bold))
        prog_title.setStyleSheet("color: #FFFFFF; letter-spacing: 1px;")

        sub_title = QLabel("SEC-OPS ENTERPRISE ZERO-TRUST ARCHITECTURE // ARUSHA HQ")
        sub_title.setFont(QFont("Consolas", 9, QFont.Weight.Bold))
        sub_title.setStyleSheet(f"color: {CyberTheme.COLOR_SCANNER}; letter-spacing: 0.5px;")

        title_box.addWidget(prog_title)
        title_box.addWidget(sub_title)
        upper_row.addLayout(title_box)

        upper_row.addStretch()

        # Live Indicator 1: CPU Usage
        self.pill_cpu = self._create_telemetry_pill("CPU", "0.0%", CyberTheme.COLOR_THREAT_MAP)
        upper_row.addWidget(self.pill_cpu)

        # Live Indicator 2: RAM Usage
        self.pill_ram = self._create_telemetry_pill("RAM", "0.0 GB", CyberTheme.COLOR_VULN_GOLD)
        upper_row.addWidget(self.pill_ram)

        # Live Indicator 3: AI Model Status
        self.pill_ai = self._create_telemetry_pill("AI CORE", "NEURAL v4.2 [ONLINE]", CyberTheme.COLOR_AI_PURPLE)
        upper_row.addWidget(self.pill_ai)

        # Live Indicator 4: Network Stream
        self.pill_net = self._create_telemetry_pill("NETWORK", "TX 0.0 MB/s | RX 0.0 MB/s", CyberTheme.COLOR_SCANNER)
        upper_row.addWidget(self.pill_net)

        nav_layout.addLayout(upper_row)

        # Lower Row: Module Switching Tab Buttons
        tab_row = QHBoxLayout()
        tab_row.setSpacing(4)

        self.tab_buttons = []
        modules = [
            ("VIRUS SCANNER", "green", CyberTheme.COLOR_SCANNER, 0),
            ("GLOBAL THREAT MAP", "blue", CyberTheme.COLOR_THREAT_MAP, 1),
            ("AI SECURITY CHAT", "cyan", CyberTheme.COLOR_AI_CYAN, 2),
            ("SYSTEM VULNERABILITY", "gold", CyberTheme.COLOR_VULN_GOLD, 3),
        ]

        for title, theme_key, accent_col, idx in modules:
            btn = QPushButton(title)
            btn.setProperty("class", "NavTabButton")
            btn.setProperty("theme", theme_key)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked, i=idx: self._switch_tab(i))
            tab_row.addWidget(btn)
            self.tab_buttons.append((btn, accent_col))

        tab_row.addStretch()
        nav_layout.addLayout(tab_row)

        return nav_frame

    def _create_telemetry_pill(self, label: str, value: str, accent_color: str) -> QFrame:
        pill = QFrame()
        pill.setProperty("class", "TelemetryPill")
        pill.setStyleSheet(f"""
            QFrame.TelemetryPill {{
                background-color: {CyberTheme.BG_CARD};
                border: 1px solid {CyberTheme.BORDER_DARK};
                border-left: 2px solid {accent_color};
                border-radius: 4px;
                padding: 3px 8px;
            }}
        """)
        p_layout = QHBoxLayout(pill)
        p_layout.setContentsMargins(6, 4, 6, 4)
        p_layout.setSpacing(6)

        lbl = QLabel(label)
        lbl.setStyleSheet(f"color: {CyberTheme.TEXT_MUTED}; font-size: 10px; font-weight: bold;")
        p_layout.addWidget(lbl)

        val = QLabel(value)
        val.setStyleSheet("color: #FFFFFF; font-family: 'Consolas', monospace; font-size: 11px; font-weight: 600;")
        p_layout.addWidget(val)
        pill.value_label = val

        return pill

    def _switch_tab(self, index: int):
        self.stacked_widget.setCurrentIndex(index)
        for i, (btn, accent_col) in enumerate(self.tab_buttons):
            if i == index:
                btn.setProperty("active", "true")
                btn.setStyleSheet(f"""
                    color: #FFFFFF;
                    border-bottom: 3px solid {accent_col};
                    background-color: rgba(255, 255, 255, 0.04);
                """)
            else:
                btn.setProperty("active", "false")
                btn.setStyleSheet("")

    def _setup_status_bar(self):
        sb = QStatusBar(self)
        sb.setStyleSheet(f"""
            QStatusBar {{
                background-color: {CyberTheme.BG_SURFACE};
                border-top: 1px solid {CyberTheme.BORDER_DARK};
                color: {CyberTheme.TEXT_MUTED};
                font-family: 'Consolas', monospace;
                font-size: 11px;
                padding: 4px 12px;
            }}
        """)
        self.setStatusBar(sb)

        self.status_left = QLabel("GRID STATUS: ZERO-TRUST SHIELD ENFORCED // ENCLAVE INTEGRITY: VERIFIED")
        self.status_left.setStyleSheet(f"color: {CyberTheme.COLOR_SCANNER}; font-weight: bold;")
        sb.addWidget(self.status_left)

        self.status_right = QLabel("UPTIME: 00:00:00 | ENCRYPTION: AES-256-GCM | HARDWARE ACCEL: OPENGL ACTIVE")
        self.status_right.setStyleSheet(f"color: {CyberTheme.TEXT_MUTED};")
        sb.addPermanentWidget(self.status_right)

    def _on_telemetry_updated(self, data: dict):
        # Update CPU meter
        cpu = data["cpu_percent"]
        self.pill_cpu.value_label.setText(f"{cpu:.1f}%")

        # Update RAM meter
        ram = data["ram_used_gb"]
        tot = data["ram_total_gb"]
        self.pill_ram.value_label.setText(f"{ram:.1f}/{tot:.0f} GB ({data['ram_percent']:.0f}%)")

        # Update Network meter
        self.pill_net.value_label.setText(f"TX {data['tx_speed']} | RX {data['rx_speed']}")

    def _update_uptime(self):
        elapsed = int(time.time() - self._start_time)
        hrs = elapsed // 3600
        mins = (elapsed % 3600) // 60
        secs = elapsed % 60
        uptime_str = f"{hrs:02d}:{mins:02d}:{secs:02d}"
        self.status_right.setText(f"UPTIME: {uptime_str} | ENCRYPTION: AES-256-GCM | HARDWARE ACCEL: ACTIVE")

    def closeEvent(self, event):
        # Safely shut down background telemetry thread
        if hasattr(self, "monitor_worker"):
            self.monitor_worker.stop()
        event.accept()
