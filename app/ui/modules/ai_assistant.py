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
from app.ui.widgets.hacker_gpt_input import HackerGPTInputConsole
from app.ui.widgets.hacker_gpt_recon import (
    HackerGPTReconSnapshotWidget, HackerGPTCodeBox
)


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
        """Preloads the exact recon snapshot shown in the user's screenshot."""
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
        q = query.lower()

        # Handle URL / Domain Reconnaissance requests
        if "check " in q or "scan " in q or ".app" in q or ".com" in q or ".org" in q or ".tz" in q or "http" in q:
            target = query.replace("Check ", "").replace("check ", "").replace("scan ", "").replace("Scan ", "").strip()
            if "/" in target:
                target = target.rstrip("/")

            if "arusha" in target or "tz" in target:
                ip = "102.214.32.14"
                whois = "Tanzania Network Information Centre (tzNIC) - Peter Defense Grid Arusha."
                country = "TANZANIA"
                module_code = "TZ"
            elif "cybergym" in target:
                ip = "34.231.169.117"
                whois = "No publicly-available WHOIS record was returned for the sub-domain."
                country = "UNITED STATES"
                module_code = "US"
            else:
                ip = "198.51.100.82"
                whois = "ARIN Registry - Cloudflare / Fastly Edge Proxy."
                country = "GLOBAL ANYCAST"
                module_code = "GL"

            res_json = json.dumps({
                "target": f"http://{target}",
                "http_status": 200,
                "request_config": {
                    "headers": {
                        "User-Agent": "HackerGPT/4.2 (Zero-Trust Recon Engine; x64)"
                    }
                },
                "plugins": {
                    "Country": {"string": [country], "module": [module_code]},
                    "HTML5": {},
                    "IP": {"string": [ip]},
                    "WAF": {"string": ["Cloudflare / Peter Shield Active"]},
                    "SecurityHeaders": {"string": ["Strict-Transport-Security, X-Frame-Options: DENY"]},
                    "OpenPorts": {"string": ["80/TCP, 443/TCP (TLS 1.3)"]},
                    "VulnerabilityWeight": "0.0 - SECURE"
                }
            }, indent=2)

            self._add_recon_snapshot(target, ip, whois, res_json)

        elif "/audit-ports" in q or "port" in q:
            code = (
                "# HackerGPT Netstat Recon Telemetry\n"
                "PORT     STATE SERVICE      REASON          VERSION\n"
                "22/tcp   open  ssh          syn-ack ttl 64  OpenSSH 9.6p1\n"
                "80/tcp   open  http         syn-ack ttl 64  nginx 1.26.0\n"
                "443/tcp  open  ssl/https    syn-ack ttl 64  nginx 1.26.0 (TLS 1.3 only)\n"
                "8080/tcp open  http-proxy   syn-ack ttl 64  [ALERT: Unauthenticated Dev API]\n\n"
                "# Remediation Directive\n"
                "iptables -A INPUT -p tcp --dport 8080 ! -s 127.0.0.1 -j DROP"
            )
            self._add_code_response(code, lang="text")

        elif "/firewall-rules" in q or "firewall" in q:
            code = (
                "#!/bin/bash\n"
                "# HackerGPT Hardened Netfilter Matrix\n"
                "iptables -P INPUT DROP\n"
                "iptables -P FORWARD DROP\n"
                "iptables -P OUTPUT ACCEPT\n"
                "iptables -A INPUT -i lo -j ACCEPT\n"
                "iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT\n"
                "iptables -A INPUT -p tcp -m multiport --dports 22,443 -j ACCEPT\n"
                "echo '[+] Zero-Trust Perimeter Rules Enforced'"
            )
            self._add_code_response(code, lang="text")

        elif "/zero-day-check" in q or "cve" in q or "zero" in q:
            code = (
                "TARGET ADVISORY DATABASE QUERY:\n"
                "CVE-2026-31902 | OpenSSL 3.0.x Handshake Memory Leak | STATUS: PATCHED\n"
                "CVE-2026-28114 | Linux eBPF Ring Buffer Overflow     | STATUS: MITIGATED\n"
                "CVE-2026-44019 | Win32k GDI Handle Privilege Escalation| STATUS: SECURE"
            )
            self._add_code_response(code, lang="text")

        else:
            resp = json.dumps({
                "query": query,
                "status": "ANALYSIS_COMPLETE",
                "hacker_gpt_assessment": "Host defenses stable. Zero unauthorized ingress vectors detected.",
                "recommendation": "Use 'Check <url>' to run a live reconnaissance snapshot or '/audit-ports' for listening socket inspection."
            }, indent=2)
            self._add_code_response(resp, lang="json")

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
        self._add_code_response(resp, lang="json")

    def _start_new_chat(self):
        # Clear chat container
        while self.chat_layout.count() > 1:
            child = self.chat_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self._add_user_prompt("New session initialized. Ready for target reconnaissance.")

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
