"""
HackerGPT AI Interface Module
Exact fidelity to HackerGPT reconnaissance console and cyberpunk input architecture.
PETER CYBER SECURITY PROGRAM
"""

import json
import time
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QFrame, QSplitter, QListWidget, QListWidgetItem
)

from app.core.config import CyberTheme
from app.core.chatbot import INITIAL_GREETING, SYSTEM_PROMPT, generate_chat_response
from app.ui.widgets.hacker_gpt_input import HackerGPTInputConsole
from app.ui.widgets.hacker_gpt_recon import (
    HackerGPTReconSnapshotWidget, HackerGPTCodeBox
)


class AIAssistantMessageWidget(QFrame):
    """
    Renders the AI Assistant's clean greeting, technical explanations,
    and out-of-scope notices with cyberpunk cyber-defense styling.
    """
    def __init__(self, message_text: str, badge_text: str = "PETER CYBER DEFENSE AI", parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            AIAssistantMessageWidget {
                background-color: #0E1118;
                border: 1px solid #1E2330;
                border-left: 3px solid #06B6D4;
                border-radius: 8px;
            }
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(8)

        # Header Badge
        header = QHBoxLayout()
        badge_lbl = QLabel(f"🛡️  {badge_text}")
        badge_lbl.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        badge_lbl.setStyleSheet("color: #06B6D4; letter-spacing: 0.5px;")
        header.addWidget(badge_lbl)
        header.addStretch()

        time_lbl = QLabel(time.strftime("%H:%M:%S"))
        time_lbl.setFont(QFont("Consolas", 9))
        time_lbl.setStyleSheet("color: #64748B;")
        header.addWidget(time_lbl)
        layout.addLayout(header)

        # Body Text
        lbl = QLabel(message_text)
        lbl.setFont(QFont("Segoe UI", 11))
        lbl.setStyleSheet("color: #E2E8F0; line-height: 1.5;")
        lbl.setWordWrap(True)
        lbl.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(lbl)


class UserPromptWidget(QWidget):
    """
    Renders the user's prompt matching the screenshot style:
    Clean font, optional prompt indicator, with a bottom divider line.
    """
    def __init__(self, prompt_text: str, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 8, 0, 8)
        layout.setSpacing(6)

        lbl = QLabel(prompt_text)
        lbl.setFont(QFont("Segoe UI", 13, QFont.Weight.Medium))
        lbl.setStyleSheet("color: #FFFFFF; letter-spacing: 0.3px;")
        lbl.setWordWrap(True)
        layout.addWidget(lbl)

        # Subtle bottom line separator like in the screenshot
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: #212530; background-color: #212530; height: 1px; border: none;")
        layout.addWidget(sep)


class AIAssistantModule(QWidget):
    """
    Module 4: HackerGPT Autonomous Cybersecurity Intelligence Interface.
    Replicates the exact HackerGPT UI with:
    - Top bar: '☰', 'HackerGPT' logo, '+ chat' button
    - Recon snapshot with dotted table & expandable JSON fingerprint
    - Monospace code box with 'text' badge and 'Copy' button
    - Custom-painted cyberpunk chamfered input console with 'Upload' & 'Send'
    - Toggleable sidebar session drawer
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.sidebar_visible = False
        self._init_ui()
        self._load_default_hacker_gpt_demo()

    def _init_ui(self):
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # -------------------------------------------------------------
        # 1. HACKERGPT TOP BAR
        # -------------------------------------------------------------
        top_bar = QFrame()
        top_bar.setStyleSheet("""
            QFrame {
                background-color: #0E1015;
                border-bottom: 1px solid #232733;
            }
        """)
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(16, 10, 16, 10)
        top_layout.setSpacing(12)

        # Hamburger Menu Button (☰)
        self.btn_hamburger = QPushButton("☰")
        self.btn_hamburger.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_hamburger.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #C0CAD7;
                border: none;
                font-size: 20px;
                font-weight: bold;
                padding: 2px 6px;
            }
            QPushButton:hover {
                color: #FFFFFF;
                background-color: #1A1E29;
                border-radius: 4px;
            }
        """)
        self.btn_hamburger.clicked.connect(self._toggle_sidebar)
        top_layout.addWidget(self.btn_hamburger)

        top_layout.addStretch()

        # Center HackerGPT Logo
        self.logo_lbl = QLabel("HackerGPT")
        self.logo_lbl.setFont(QFont("Segoe UI", 21, QFont.Weight.Bold))
        self.logo_lbl.setStyleSheet("color: #FFFFFF; letter-spacing: 0.5px;")
        top_layout.addWidget(self.logo_lbl)

        top_layout.addStretch()

        # Right '+ chat' Button
        self.btn_new_chat = QPushButton("+ chat")
        self.btn_new_chat.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_new_chat.setStyleSheet("""
            QPushButton {
                background-color: #161821;
                color: #C8D1DC;
                border: 1px solid #2F3545;
                border-radius: 6px;
                padding: 6px 14px;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #1F232F;
                color: #FFFFFF;
                border-color: #4A536B;
            }
        """)
        self.btn_new_chat.clicked.connect(self._start_new_chat)
        top_layout.addWidget(self.btn_new_chat)

        root_layout.addWidget(top_bar)

        # -------------------------------------------------------------
        # 2. MAIN WORKSPACE (Splitter: Optional History Sidebar + Chat Area)
        # -------------------------------------------------------------
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #1F2430;
                width: 1px;
            }
        """)

        # Left History Drawer (Hidden by default, toggled via ☰)
        self.sidebar_frame = QFrame()
        self.sidebar_frame.setFixedWidth(240)
        self.sidebar_frame.setStyleSheet("""
            QFrame {
                background-color: #0B0D12;
                border-right: 1px solid #1E222D;
            }
        """)
        sb_layout = QVBoxLayout(self.sidebar_frame)
        sb_layout.setContentsMargins(10, 14, 10, 14)
        sb_layout.setSpacing(10)

        sb_header = QLabel("RECON SESSIONS")
        sb_header.setStyleSheet("color: #64748B; font-size: 11px; font-weight: bold; letter-spacing: 0.8px;")
        sb_layout.addWidget(sb_header)

        self.session_list = QListWidget()
        self.session_list.setStyleSheet("""
            QListWidget {
                background-color: transparent;
                border: none;
                color: #A0AAB8;
                font-size: 12px;
            }
            QListWidget::item {
                padding: 8px 10px;
                border-radius: 4px;
            }
            QListWidget::item:hover {
                background-color: #161922;
                color: #FFFFFF;
            }
            QListWidget::item:selected {
                background-color: #1C202C;
                color: #06B6D4;
                font-weight: bold;
            }
        """)
        sessions = [
            "cybergym.hackergpt.app",
            "arusha-core.tz [Tanzania HQ]",
            "port-audit-192.168.1.1",
            "cve-2026-31902-openssl",
            "zero-trust-firewall-synth",
            "binary-payload-deobfuscate"
        ]
        for s in sessions:
            self.session_list.addItem(s)
        self.session_list.itemClicked.connect(self._on_session_clicked)
        sb_layout.addWidget(self.session_list)
        self.sidebar_frame.setVisible(False)
        self.splitter.addWidget(self.sidebar_frame)

        # Right Main Chat Area
        chat_pane = QWidget()
        chat_layout = QVBoxLayout(chat_pane)
        chat_layout.setContentsMargins(24, 14, 24, 14)
        chat_layout.setSpacing(12)

        # Chat Stream Scroll Area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: #0A0A0C;
                border: none;
            }
        """)

        self.chat_container = QWidget()
        self.chat_container.setStyleSheet("background-color: #0A0A0C;")
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setContentsMargins(0, 0, 0, 0)
        self.chat_layout.setSpacing(16)
        self.chat_layout.addStretch()

        self.scroll_area.setWidget(self.chat_container)
        chat_layout.addWidget(self.scroll_area, stretch=1)

        # -------------------------------------------------------------
        # 3. CYBERPUNK BOTTOM INPUT CONSOLE
        # -------------------------------------------------------------
        self.input_console = HackerGPTInputConsole()
        self.input_console.message_sent.connect(self._on_message_submitted)
        self.input_console.file_attached.connect(self._on_file_attached)
        chat_layout.addWidget(self.input_console)

        self.splitter.addWidget(chat_pane)
        root_layout.addWidget(self.splitter, stretch=1)

    # -----------------------------------------------------------------
    # HackerGPT Recon Content Generation
    # -----------------------------------------------------------------
    def _load_default_hacker_gpt_demo(self):
        """Preloads clean welcome greeting and initial recon snapshot."""
        self._add_assistant_message(INITIAL_GREETING)
        self._add_user_prompt("Check cybergym.hackergpt.app/")

        demo_json = json.dumps({
            "target": "http://cybergym.hackergpt.app",
            "http_status": 200,
            "request_config": {
                "headers": {
                    "User-Agent": "Opera/9.80 (Windows NT 6.1; U; fi) Presto/2.7.62 Version/11.00"
                }
            },
            "plugins": {
                "Country": {"string": ["UNITED STATES"], "module": ["US"]},
                "HTML5": {},
                "IP": {"string": ["34.231.169.117"]},
                "JQuery": {"version": ["2.2.4"]},
                "Script": {"string": ["module"]},
                "Title": {"string": ["CyberGym"]},
                "UncommonHeaders": {"string": ["access-control-allow-origin,x-content-type-options,feature-policy,x-re..."]}
            }
        }, indent=2)

        self._add_recon_snapshot(
            target="cybergym.hackergpt.app",
            ip="34.231.169.117",
            whois="No publicly-available WHOIS record was returned for the sub-domain.",
            json_fingerprint=demo_json
        )

    def _add_assistant_message(self, text: str, badge_text: str = "PETER CYBER DEFENSE AI"):
        item = self.chat_layout.takeAt(self.chat_layout.count() - 1)
        msg_widget = AIAssistantMessageWidget(text, badge_text=badge_text)
        self.chat_layout.addWidget(msg_widget)
        self.chat_layout.addStretch()
        self._scroll_to_bottom()

    def _add_user_prompt(self, text: str):
        item = self.chat_layout.takeAt(self.chat_layout.count() - 1)
        prompt_widget = UserPromptWidget(text)
        self.chat_layout.addWidget(prompt_widget)
        self.chat_layout.addStretch()
        self._scroll_to_bottom()

    def _add_recon_snapshot(self, target: str, ip: str, whois: str, json_fingerprint: str):
        item = self.chat_layout.takeAt(self.chat_layout.count() - 1)
        recon_widget = HackerGPTReconSnapshotWidget(target, ip, whois, json_fingerprint)
        self.chat_layout.addWidget(recon_widget)
        self.chat_layout.addStretch()
        self._scroll_to_bottom()

    def _add_code_response(self, code_text: str, lang: str = "text"):
        item = self.chat_layout.takeAt(self.chat_layout.count() - 1)
        code_box = HackerGPTCodeBox(code_text, lang_label=lang)
        self.chat_layout.addWidget(code_box)
        self.chat_layout.addStretch()
        self._scroll_to_bottom()

    def _on_message_submitted(self, query: str):
        self._add_user_prompt(query)
        # Simulate realistic HackerGPT Recon Analysis
        QTimer.singleShot(400, lambda: self._process_query_response(query))

    def _process_query_response(self, query: str):
        res = generate_chat_response(query)
        scope = res.get("scope", "SECURITY")

        if scope == "RECON":
            self._add_recon_snapshot(
                target=res["target"],
                ip=res["ip"],
                whois=res["whois"],
                json_fingerprint=json.dumps(res["fingerprint"], indent=2)
            )
        elif scope == "OUT_OF_SCOPE":
            self._add_assistant_message(res["reply"], badge_text="SCOPE POLICY ENFORCED")
        elif scope == "GREETING":
            self._add_assistant_message(res["reply"], badge_text="PETER CYBER DEFENSE AI")
        else:
            # Cybersecurity technical response
            self._add_assistant_message(res["reply"], badge_text=f"CYBER DEFENSE // {res['target']}")
            if "technical_telemetry" in res.get("fingerprint", {}):
                telemetry = json.dumps(res["fingerprint"]["technical_telemetry"], indent=2)
                self._add_code_response(telemetry, lang="json")

    def _on_file_attached(self, file_path: str):
        import os
        fname = os.path.basename(file_path)
        self._add_user_prompt(f"Uploaded security artifact: {fname}")
        resp = json.dumps({
            "artifact": fname,
            "path": file_path,
            "sha256": "8a7c29e1d84b55013ef47910fa324bb6c9028d716892eef81938501da9184291",
            "entropy": "7.982 / 8.000",
            "packer_detected": "UPX 4.02",
            "status": "SUSPICIOUS - High entropy payload requiring sandbox isolation"
        }, indent=2)
        self._add_assistant_message(
            f"Artifact `{fname}` analyzed. High-entropy packed payload detected. "
            "Sandbox execution quarantine recommended before running on production endpoints."
        )
        self._add_code_response(resp, lang="json")

    def _start_new_chat(self):
        # Clear chat container
        while self.chat_layout.count() > 1:
            child = self.chat_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self._add_assistant_message(INITIAL_GREETING)

    def _toggle_sidebar(self):
        self.sidebar_visible = not self.sidebar_visible
        self.sidebar_frame.setVisible(self.sidebar_visible)

    def _on_session_clicked(self, item: QListWidgetItem):
        name = item.text()
        self._start_new_chat()
        self._on_message_submitted(f"Check {name}")

    def _scroll_to_bottom(self):
        QTimer.singleShot(50, lambda: self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        ))
