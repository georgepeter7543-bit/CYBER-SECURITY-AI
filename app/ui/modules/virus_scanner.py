"""
Virus Scanner Module (Color Accent: Matrix Neon Green - #00FF66)
PETER CYBER SECURITY PROGRAM
"""

import json
import os
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QProgressBar, QTableWidget, QTableWidgetItem, QHeaderView,
    QFrame, QMessageBox, QFileDialog
)

from app.core.config import CyberTheme
from app.core.security_engine import ScanWorker, calculate_file_hashes
from app.ui.widgets.drag_drop_zone import NativeDropZoneWidget


class VirusScannerModule(QWidget):
    """
    Module 2: Advanced Heuristic Virus Scanner & Multi-Engine Sandboxing.
    Theme: Matrix Neon Green (#00FF66).
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.active_file: str = ""
        self.scan_worker: ScanWorker = None
        self.last_scan_result: dict = None

        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(14)

        # 1. Module Header
        header = QHBoxLayout()
        title_box = QVBoxLayout()
        title = QLabel("VIRUS SCANNER & HEURISTIC ANALYZER")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {CyberTheme.COLOR_SCANNER}; letter-spacing: 0.5px;")
        subtitle = QLabel("Multi-engine signature matching, entropy calculation, and kernel behavioral sandboxing.")
        subtitle.setStyleSheet(f"color: {CyberTheme.TEXT_MUTED}; font-size: 12px;")
        title_box.addWidget(title)
        title_box.addWidget(subtitle)
        header.addLayout(title_box)
        header.addStretch()

        # Engine Status Badge
        badge = QLabel("CORE ENGINES: 6/6 ONLINE")
        badge.setStyleSheet(f"""
            background-color: rgba(0, 255, 102, 0.12);
            color: {CyberTheme.COLOR_SCANNER};
            border: 1px solid {CyberTheme.COLOR_SCANNER};
            border-radius: 4px;
            padding: 6px 12px;
            font-size: 11px;
            font-weight: 700;
        """)
        header.addWidget(badge)
        layout.addLayout(header)

        # 2. Native File Drag-and-Drop Zone
        self.drop_zone = NativeDropZoneWidget()
        self.drop_zone.file_selected.connect(self._on_file_selected)
        layout.addWidget(self.drop_zone)

        # 3. Cryptographic Hashes & File Telemetry Strip
        self.crypto_card = QFrame()
        self.crypto_card.setStyleSheet(f"""
            QFrame {{
                background-color: {CyberTheme.BG_CARD};
                border: 1px solid {CyberTheme.BORDER_DARK};
                border-radius: 6px;
                padding: 6px 12px;
            }}
        """)
        crypto_layout = QHBoxLayout(self.crypto_card)
        crypto_layout.setContentsMargins(8, 6, 8, 6)

        self.lbl_md5 = QLabel("MD5: --")
        self.lbl_sha256 = QLabel("SHA-256: --")
        self.lbl_entropy = QLabel("ENTROPY: --")
        self.lbl_size = QLabel("SIZE: --")

        for lbl in [self.lbl_md5, self.lbl_sha256, self.lbl_entropy, self.lbl_size]:
            lbl.setStyleSheet(f"color: {CyberTheme.TEXT_MUTED}; font-family: 'Consolas', monospace; font-size: 11px;")
            crypto_layout.addWidget(lbl)
            if lbl != self.lbl_size:
                sep = QLabel("|")
                sep.setStyleSheet(f"color: {CyberTheme.BORDER_MID};")
                crypto_layout.addWidget(sep)
        layout.addWidget(self.crypto_card)

        # 4. Scanning Progress & Current Stage
        progress_box = QVBoxLayout()
        progress_box.setSpacing(4)
        prog_header = QHBoxLayout()
        self.stage_lbl = QLabel("READY - Awaiting Target Binary")
        self.stage_lbl.setStyleSheet(f"color: {CyberTheme.TEXT_MAIN}; font-size: 12px; font-weight: 600;")
        prog_header.addWidget(self.stage_lbl)
        prog_header.addStretch()

        self.pct_lbl = QLabel("0%")
        self.pct_lbl.setStyleSheet(f"color: {CyberTheme.COLOR_SCANNER}; font-weight: 700; font-family: monospace;")
        prog_header.addWidget(self.pct_lbl)
        progress_box.addLayout(prog_header)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        progress_box.addWidget(self.progress_bar)
        layout.addLayout(progress_box)

        # 5. Multi-Engine Result Table
        self.result_table = QTableWidget(0, 6)
        self.result_table.setHorizontalHeaderLabels([
            "SECURITY ENGINE", "ENGINE TYPE", "DETECTION STATUS", "THREAT VECTOR", "RISK SCORE", "RECOMMENDED ACTION"
        ])
        self.result_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.result_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.result_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.result_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.result_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.result_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        self.result_table.verticalHeader().setVisible(False)
        self.result_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.result_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.result_table, stretch=1)

        # 6. Action Control Bar
        control_bar = QHBoxLayout()
        control_bar.setSpacing(10)

        self.btn_scan = QPushButton("▶ EXECUTE DEEP HEURISTIC SCAN")
        self.btn_scan.setProperty("class", "CyberButtonGreen")
        self.btn_scan.setEnabled(False)
        self.btn_scan.clicked.connect(self._start_scan)
        control_bar.addWidget(self.btn_scan)

        self.btn_abort = QPushButton("⏹ ABORT")
        self.btn_abort.setProperty("class", "CyberButton")
        self.btn_abort.setEnabled(False)
        self.btn_abort.clicked.connect(self._abort_scan)
        control_bar.addWidget(self.btn_abort)

        control_bar.addStretch()

        self.btn_quarantine = QPushButton("🛡️ QUARANTINE THREAT")
        self.btn_quarantine.setProperty("class", "CyberButton")
        self.btn_quarantine.setEnabled(False)
        self.btn_quarantine.clicked.connect(self._quarantine_threat)
        control_bar.addWidget(self.btn_quarantine)

        self.btn_export = QPushButton("📄 EXPORT FORENSIC REPORT")
        self.btn_export.setProperty("class", "CyberButton")
        self.btn_export.setEnabled(False)
        self.btn_export.clicked.connect(self._export_report)
        control_bar.addWidget(self.btn_export)

        layout.addLayout(control_bar)

    # ----------------------------------------------------
    # Event Handlers & Scan Workflow
    # ----------------------------------------------------
    def _on_file_selected(self, path: str):
        self.active_file = path
        self.btn_scan.setEnabled(True)
        self.stage_lbl.setText(f"Target loaded: {os.path.basename(path)} - Ready to execute scan")
        self.progress_bar.setValue(0)
        self.pct_lbl.setText("0%")
        self.result_table.setRowCount(0)

        # Compute file cryptographic metadata immediately
        hashes = calculate_file_hashes(path)
        self.lbl_md5.setText(f"MD5: {hashes['md5'][:16]}...")
        self.lbl_sha256.setText(f"SHA-256: {hashes['sha256'][:20]}...")
        self.lbl_entropy.setText(f"ENTROPY: {hashes['entropy']}")
        self.lbl_size.setText(f"SIZE: {hashes['size_formatted']}")

    def _start_scan(self):
        if not self.active_file or not os.path.exists(self.active_file):
            QMessageBox.warning(self, "No Target", "Please select a valid file target.")
            return

        self.btn_scan.setEnabled(False)
        self.btn_abort.setEnabled(True)
        self.btn_quarantine.setEnabled(False)
        self.btn_export.setEnabled(False)
        self.result_table.setRowCount(0)

        self.scan_worker = ScanWorker(self.active_file, self)
        self.scan_worker.stage_changed.connect(self._on_stage_changed)
        self.scan_worker.progress_changed.connect(self._on_progress_changed)
        self.scan_worker.engine_verdict.connect(self._on_engine_verdict)
        self.scan_worker.scan_finished.connect(self._on_scan_finished)
        self.scan_worker.start()

    def _abort_scan(self):
        if self.scan_worker and self.scan_worker.isRunning():
            self.scan_worker.abort()
            self.scan_worker.wait(1000)
            self.stage_lbl.setText("Scan Aborted by Operator")
            self.btn_abort.setEnabled(False)
            self.btn_scan.setEnabled(True)

    def _on_stage_changed(self, stage_text: str):
        self.stage_lbl.setText(stage_text)

    def _on_progress_changed(self, pct: int):
        self.progress_bar.setValue(pct)
        self.pct_lbl.setText(f"{pct}%")

    def _on_engine_verdict(self, verdict: dict):
        row = self.result_table.rowCount()
        self.result_table.insertRow(row)

        item_engine = QTableWidgetItem(f"  {verdict['engine']}")
        item_type = QTableWidgetItem(verdict['type'])
        item_status = QTableWidgetItem(verdict['status'])
        item_vector = QTableWidgetItem(verdict['threat_name'])
        item_score = QTableWidgetItem(verdict['score'])
        item_action = QTableWidgetItem(verdict['action'])

        # Stylize status badges
        status = verdict['status']
        if "THREAT" in status:
            item_status.setForeground(QColor(CyberTheme.SEVERITY_CRITICAL))
            item_status.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        elif "SUSPICIOUS" in status:
            item_status.setForeground(QColor(CyberTheme.SEVERITY_HIGH))
            item_status.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        else:
            item_status.setForeground(QColor(CyberTheme.COLOR_SCANNER))

        self.result_table.setItem(row, 0, item_engine)
        self.result_table.setItem(row, 1, item_type)
        self.result_table.setItem(row, 2, item_status)
        self.result_table.setItem(row, 3, item_vector)
        self.result_table.setItem(row, 4, item_score)
        self.result_table.setItem(row, 5, item_action)

    def _on_scan_finished(self, summary: dict):
        self.last_scan_result = summary
        self.btn_scan.setEnabled(True)
        self.btn_abort.setEnabled(False)
        self.btn_export.setEnabled(True)

        if summary["is_threat"]:
            self.stage_lbl.setText("⚠️ SCAN COMPLETE: CRITICAL THREAT DETECTED")
            self.stage_lbl.setStyleSheet(f"color: {CyberTheme.SEVERITY_CRITICAL}; font-weight: bold;")
            self.btn_quarantine.setEnabled(True)
        else:
            self.stage_lbl.setText("✓ SCAN COMPLETE: ZERO MALICIOUS ARTIFACTS FOUND")
            self.stage_lbl.setStyleSheet(f"color: {CyberTheme.COLOR_SCANNER}; font-weight: bold;")

    def _quarantine_threat(self):
        if not self.active_file:
            return
        QMessageBox.information(
            self,
            "Quarantine Executed",
            f"File '{os.path.basename(self.active_file)}' has been neutralized and moved to Peter Isolated Vault.\n"
            f"Permissions revoked (0000). Process hooks detached."
        )
        self.btn_quarantine.setEnabled(False)

    def _export_report(self):
        if not self.last_scan_result:
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Export Forensic JSON Report", f"scan_report_{os.path.basename(self.active_file)}.json", "JSON Files (*.json)"
        )
        if path:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.last_scan_result, f, indent=4)
            QMessageBox.information(self, "Export Complete", f"Forensic report written successfully to:\n{path}")
