"""
Native Chat Message Bubble and Monospace Code Box Widgets
PETER CYBER SECURITY PROGRAM
"""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit,
    QPushButton, QFrame, QApplication
)

from app.core.config import CyberTheme


class CodeBoxWidget(QFrame):
    """
    Dedicated native monospace code container with syntax styling and copy action.
    """
    def __init__(self, code_text: str, language: str = "bash", parent=None):
        super().__init__(parent)
        self.code_text = code_text.strip()
        self.language = language

        self.setStyleSheet(f"""
            QFrame {{
                background-color: {CyberTheme.BG_CODE};
                border: 1px solid {CyberTheme.BORDER_MID};
                border-left: 3px solid {CyberTheme.COLOR_AI_CYAN};
                border-radius: 6px;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(6)

        # Header bar with language badge and Copy button
        header = QHBoxLayout()
        lang_label = QLabel(f"TERMINAL / {language.upper()}")
        lang_label.setStyleSheet(f"color: {CyberTheme.COLOR_AI_CYAN}; font-family: 'Consolas', monospace; font-size: 11px; font-weight: bold;")
        header.addWidget(lang_label)
        header.addStretch()

        self.copy_btn = QPushButton("📋 Copy Snippet")
        self.copy_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {CyberTheme.BG_CARD};
                color: {CyberTheme.TEXT_MUTED};
                border: 1px solid {CyberTheme.BORDER_DARK};
                border-radius: 4px;
                padding: 3px 8px;
                font-size: 10px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                color: #FFFFFF;
                border-color: {CyberTheme.COLOR_AI_CYAN};
            }}
        """)
        self.copy_btn.clicked.connect(self._copy_to_clipboard)
        header.addWidget(self.copy_btn)
        layout.addLayout(header)

        # Monospace code content
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setPlainText(self.code_text)
        self.text_area.setFont(QFont("Consolas", 10))
        self.text_area.setStyleSheet(f"""
            QTextEdit {{
                background-color: transparent;
                border: none;
                color: #38BDF8;
                padding: 0px;
            }}
        """)
        # Auto-adjust height based on lines
        lines_count = len(self.code_text.splitlines())
        height = min(max(lines_count * 20 + 20, 60), 240)
        self.text_area.setFixedHeight(height)
        layout.addWidget(self.text_area)

    def _copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        if clipboard:
            clipboard.setText(self.code_text)
            self.copy_btn.setText("✓ Copied!")
            self.copy_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: rgba(0, 255, 102, 0.2);
                    color: {CyberTheme.COLOR_SCANNER};
                    border: 1px solid {CyberTheme.COLOR_SCANNER};
                    border-radius: 4px;
                    padding: 3px 8px;
                    font-size: 10px;
                    font-weight: 600;
                }}
            """)


class ChatMessageWidget(QFrame):
    """
    Renders user queries and cybersecurity assistant responses with code boxes.
    """
    def __init__(self, sender: str, text: str, code_snippet: str = None, code_lang: str = "bash", parent=None):
        super().__init__(parent)
        is_user = (sender.lower() == "user")

        border_color = CyberTheme.COLOR_AI_CYAN if is_user else CyberTheme.COLOR_AI_PURPLE
        header_color = CyberTheme.COLOR_AI_CYAN if is_user else "#C084FC"

        self.setStyleSheet(f"""
            ChatMessageWidget {{
                background-color: {CyberTheme.BG_CARD if not is_user else "#121824"};
                border: 1px solid {CyberTheme.BORDER_MID};
                border-left: 3px solid {border_color};
                border-radius: 8px;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(8)

        # Header
        header = QHBoxLayout()
        badge_text = "OPERATOR [SEC-ADMIN]" if is_user else "PETER CYBER DEFENSE AI [v4.2]"
        header_lbl = QLabel(badge_text)
        header_lbl.setStyleSheet(f"color: {header_color}; font-size: 11px; font-weight: 700; letter-spacing: 0.5px;")
        header.addWidget(header_lbl)
        header.addStretch()

        import time
        time_lbl = QLabel(time.strftime("%H:%M:%S"))
        time_lbl.setStyleSheet(f"color: {CyberTheme.TEXT_DARK}; font-size: 10px; font-family: monospace;")
        header.addWidget(time_lbl)
        layout.addLayout(header)

        # Message Text
        msg_lbl = QLabel(text)
        msg_lbl.setWordWrap(True)
        msg_lbl.setStyleSheet(f"color: {CyberTheme.TEXT_MAIN}; font-size: 13px; line-height: 1.5;")
        layout.addWidget(msg_lbl)

        # Optional Code Snippet Block
        if code_snippet:
            code_box = CodeBoxWidget(code_snippet, language=code_lang)
            layout.addWidget(code_box)
