"""
HackerGPT Recon Snapshot & Monospace Code Box Widgets
PETER CYBER SECURITY PROGRAM
"""

import json
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QPainter, QPen, QBrush
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit,
    QPushButton, QFrame, QApplication, QTableWidget,
    QTableWidgetItem, QHeaderView
)

from app.core.config import CyberTheme


class HackerGPTCodeBox(QFrame):
    """
    Code box matching HackerGPT style:
    - Top bar with language badge on left ('text' or 'json') and '📋 Copy' button on right.
    - Dark navy/charcoal background (#181B24).
    - Monospace formatted code text.
    """
    def __init__(self, code_text: str, lang_label: str = "text", parent=None):
        super().__init__(parent)
        self.code_text = code_text.strip()
        self.lang_label = lang_label

        self.setStyleSheet("""
            QFrame {
                background-color: #171A23;
                border: 1px solid #282E3D;
                border-radius: 8px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 10, 14, 12)
        layout.setSpacing(6)

        # Header Row: "text" / "json" on left, "Copy" on right
        header = QHBoxLayout()
        header.setContentsMargins(2, 0, 2, 0)

        lbl_lang = QLabel(self.lang_label)
        lbl_lang.setStyleSheet("color: #8C96A5; font-size: 13px; font-weight: 500; font-family: 'Segoe UI', sans-serif;")
        header.addWidget(lbl_lang)
        header.addStretch()

        self.btn_copy = QPushButton("📄 Copy")
        self.btn_copy.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_copy.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #A0AAB8;
                border: none;
                font-size: 13px;
                font-weight: 500;
                padding: 4px 8px;
            }
            QPushButton:hover {
                color: #FFFFFF;
            }
        """)
        self.btn_copy.clicked.connect(self._copy_to_clipboard)
        header.addWidget(self.btn_copy)
        layout.addLayout(header)

        # Monospace Code Area
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setPlainText(self.code_text)
        self.text_edit.setFont(QFont("Consolas", 10))
        self.text_edit.setStyleSheet("""
            QTextEdit {
                background-color: transparent;
                border: none;
                color: #E2E8F0;
                line-height: 1.45;
                padding: 0px;
            }
        """)

        # Calculate height based on lines
        lines_count = len(self.code_text.splitlines())
        calc_height = min(max(lines_count * 21 + 15, 80), 380)
        self.text_edit.setFixedHeight(calc_height)
        layout.addWidget(self.text_edit)

    def _copy_to_clipboard(self):
        cb = QApplication.clipboard()
        if cb:
            cb.setText(self.code_text)
            self.btn_copy.setText("✓ Copied")
            self.btn_copy.setStyleSheet("color: #00FF66; font-size: 13px; font-weight: bold; border: none; background: transparent;")


class DottedReconTable(QWidget):
    """
    Table rendering Item | Details with dashed/dotted borders matching HackerGPT style.
    """
    def __init__(self, rows_data: list, parent=None):
        super().__init__(parent)
        self.rows_data = rows_data
        self.is_expanded = False

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Frame with dashed styling
        self.table_frame = QFrame()
        self.table_frame.setStyleSheet("""
            QFrame {
                background-color: transparent;
                border: 1px dashed #3D4454;
            }
        """)
        t_layout = QVBoxLayout(self.table_frame)
        t_layout.setContentsMargins(0, 0, 0, 0)
        t_layout.setSpacing(0)

        # Header: Item | Details
        hdr_widget = self._create_row("Item", "Details", is_header=True)
        t_layout.addWidget(hdr_widget)

        for item_key, item_val, is_expandable in self.rows_data:
            row_widget = self._create_row(item_key, item_val, is_expandable=is_expandable)
            t_layout.addWidget(row_widget)

        layout.addWidget(self.table_frame)

    def _create_row(self, col1: str, col2: str, is_header: bool = False, is_expandable: bool = False) -> QWidget:
        row = QFrame()
        border_top = "border-top: 1px dashed #3D4454;" if not is_header else ""
        row.setStyleSheet(f"""
            QFrame {{
                background-color: transparent;
                {border_top}
            }}
        """)
        r_layout = QHBoxLayout(row)
        r_layout.setContentsMargins(14, 10, 14, 10)
        r_layout.setSpacing(12)

        lbl1 = QLabel(col1)
        lbl1.setFixedWidth(160)
        font_weight = "bold" if is_header else "bold"
        font_color = "#FFFFFF" if is_header else "#E2E8F0"
        lbl1.setStyleSheet(f"color: {font_color}; font-size: 13px; font-weight: {font_weight}; border: none;")
        r_layout.addWidget(lbl1)

        # Vertical dotted divider
        div = QLabel("|")
        div.setStyleSheet("color: #3D4454; border: none; font-weight: bold;")
        r_layout.addWidget(div)

        if is_expandable:
            self.btn_expand = QPushButton(f"▶ {col2}")
            self.btn_expand.setCursor(Qt.CursorShape.PointingHandCursor)
            self.btn_expand.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    color: #A0AAB8;
                    border: none;
                    text-align: left;
                    font-size: 13px;
                }
                QPushButton:hover {
                    color: #FFFFFF;
                }
            """)
            r_layout.addWidget(self.btn_expand, stretch=1)
        else:
            lbl2 = QLabel(col2)
            lbl2.setWordWrap(True)
            lbl2.setStyleSheet(f"color: {font_color}; font-size: 13px; border: none;")
            r_layout.addWidget(lbl2, stretch=1)

        return row


class HackerGPTReconSnapshotWidget(QWidget):
    """
    Renders the complete HackerGPT Reconnaissance snapshot:
    - Target heading: '<target> - Quick Recon Snapshot'
    - Dotted table with IP, WHOIS, HTTP Fingerprint
    - Collapsible JSON Code Box
    """
    def __init__(self, target: str, ip: str, whois: str, json_fingerprint: str, parent=None):
        super().__init__(parent)
        self.target = target
        self.ip = ip
        self.whois = whois
        self.json_fingerprint = json_fingerprint

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 4, 0, 10)
        layout.setSpacing(12)

        # Title: target - Quick Recon Snapshot
        self.title_lbl = QLabel(f"{target} - Quick Recon Snapshot")
        self.title_lbl.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        self.title_lbl.setStyleSheet("color: #FFFFFF; letter-spacing: 0.3px;")
        layout.addWidget(self.title_lbl)

        # Dotted Table
        rows = [
            ("IP Address", ip, False),
            ("WHOIS", whois, False),
            ("HTTP Fingerprint", "Click to expand", True)
        ]
        self.table = DottedReconTable(rows)
        self.table.btn_expand.clicked.connect(self._toggle_expand)
        layout.addWidget(self.table)

        # Code Box containing HTTP Fingerprint JSON
        self.code_box = HackerGPTCodeBox(json_fingerprint, lang_label="text")
        layout.addWidget(self.code_box)

    def _toggle_expand(self):
        is_visible = self.code_box.isVisible()
        self.code_box.setVisible(not is_visible)
        if not is_visible:
            self.table.btn_expand.setText("▼ Hide fingerprint")
        else:
            self.table.btn_expand.setText("▶ Click to expand")
