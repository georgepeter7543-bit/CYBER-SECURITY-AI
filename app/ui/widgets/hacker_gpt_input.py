"""
Custom-Painted Cyberpunk Input Console Widget (HackerGPT Style)
PETER CYBER SECURITY PROGRAM
"""

from PyQt6.QtCore import Qt, pyqtSignal, QPointF, QRectF
from PyQt6.QtGui import (
    QPainter, QColor, QPen, QBrush, QPainterPath, QFont,
    QKeyEvent
)
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
    QPushButton, QFileDialog, QGraphicsDropShadowEffect
)

from app.core.config import CyberTheme


class CyberPromptTextEdit(QTextEdit):
    """
    Subclassed QTextEdit that emits submit on Return (Enter)
    and allows newline on Shift+Return.
    """
    return_pressed = pyqtSignal()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            if not (event.modifiers() & Qt.KeyboardModifier.ShiftModifier):
                self.return_pressed.emit()
                event.accept()
                return
        super().keyPressEvent(event)


class HackerGPTInputConsole(QWidget):
    """
    Native hardware-accelerated cyberpunk input console featuring
    the custom stepped/chamfered polygon outline, upload button, and send action.
    """
    message_sent = pyqtSignal(str)
    file_attached = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(130)
        self.setMaximumHeight(170)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(18, 18, 18, 14)
        main_layout.setSpacing(6)

        # 1. Multi-line prompt editor
        self.text_editor = CyberPromptTextEdit()
        self.text_editor.setPlaceholderText("Message HackerGPT")
        self.text_editor.setFont(QFont("Segoe UI", 13))
        self.text_editor.setStyleSheet("""
            QTextEdit {
                background: transparent;
                border: none;
                color: #F1F5F9;
                selection-background-color: #06B6D4;
                selection-color: #000000;
            }
        """)
        self.text_editor.return_pressed.connect(self._on_submit)
        main_layout.addWidget(self.text_editor, stretch=1)

        # 2. Bottom Action Row: [Upload] ........... [Send ▶]
        bottom_bar = QHBoxLayout()
        bottom_bar.setContentsMargins(4, 0, 4, 0)

        # Upload Button
        self.btn_upload = QPushButton("📁 Upload")
        self.btn_upload.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_upload.setStyleSheet("""
            QPushButton {
                background-color: #171A23;
                color: #7A8699;
                border: 1px solid #2B3142;
                border-radius: 6px;
                padding: 5px 12px;
                font-size: 12px;
                font-weight: 500;
            }
            QPushButton:hover {
                color: #FFFFFF;
                border-color: #3F475F;
                background-color: #1D212D;
            }
        """)
        self.btn_upload.clicked.connect(self._on_upload_clicked)
        bottom_bar.addWidget(self.btn_upload)

        bottom_bar.addStretch()

        # Send Button with Cyber Arrow
        self.btn_send = QPushButton("▶")
        self.btn_send.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_send.setFixedSize(36, 34)
        self.btn_send.setStyleSheet("""
            QPushButton {
                background-color: #1A1E29;
                color: #C2CBD8;
                border: 1px solid #353D52;
                border-radius: 6px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #242B3B;
                color: #FFFFFF;
                border-color: #4D5875;
            }
            QPushButton:pressed {
                background-color: #12151D;
            }
        """)
        self.btn_send.clicked.connect(self._on_submit)
        bottom_bar.addWidget(self.btn_send)

        main_layout.addLayout(bottom_bar)

    def _on_submit(self):
        text = self.text_editor.toPlainText().strip()
        if not text:
            return
        self.text_editor.clear()
        self.message_sent.emit(text)

    def _on_upload_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Attach Security Artifact / Binary / PCAP / Script",
            "",
            "All Files (*.*);;Binaries (*.exe *.dll *.bin);;PCAP / Logs (*.pcap *.pcapng *.log);;Scripts (*.py *.sh *.ps1)"
        )
        if file_path:
            self.file_attached.emit(file_path)

    # -----------------------------------------------------------------
    # Native QPainter Vector Rendering for the Cyber Chamfered Outline
    # -----------------------------------------------------------------
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect().adjusted(4, 4, -4, -4)
        w = rect.width()
        h = rect.height()
        x0 = rect.left()
        y0 = rect.top()
        x1 = rect.right()
        y1 = rect.bottom()

        # Fill background container
        bg_brush = QBrush(QColor("#111319"))
        border_pen = QPen(QColor("#384054"), 1.4)

        # Construct the exact HackerGPT polygon with the stepped cutout
        # Top edge step geometry:
        # Step starts around x1 - 160, angles down to y0 + 14, runs flat to x1 - 32, then angles up
        step_x1 = max(x0 + 80, x1 - 150)
        step_x2 = max(x0 + 100, x1 - 132)
        step_x3 = x1 - 32
        step_x4 = x1 - 18
        step_depth = y0 + 13

        c_size = 12.0  # Chamfer corner size

        path = QPainterPath()
        # Top-left start after chamfer
        path.moveTo(x0 + c_size, y0)

        # Line to step start
        path.lineTo(step_x1, y0)
        # Angle down into step
        path.lineTo(step_x2, step_depth)
        # Flat bottom of step
        path.lineTo(step_x3, step_depth)
        # Angle back up
        path.lineTo(step_x4, y0)
        # Flat to top-right corner
        path.lineTo(x1 - c_size, y0)

        # Top-right chamfer
        path.lineTo(x1, y0 + c_size)

        # Right edge
        path.lineTo(x1, y1 - c_size)

        # Bottom-right chamfer
        path.lineTo(x1 - c_size, y1)

        # Bottom edge
        path.lineTo(x0 + c_size, y1)

        # Bottom-left chamfer
        path.lineTo(x0, y1 - c_size)

        # Left edge
        path.lineTo(x0, y0 + c_size)

        # Close with top-left chamfer
        path.closeSubpath()

        # Draw filled background
        painter.setBrush(bg_brush)
        painter.setPen(border_pen)
        painter.drawPath(path)

        # Draw the distinctive dashed line accent on the top-left edge
        dashed_pen = QPen(QColor("#525D78"), 1.5, Qt.PenStyle.CustomDashLine)
        dashed_pen.setDashPattern([5, 4])
        painter.setPen(dashed_pen)
        painter.drawLine(int(x0 + c_size + 4), int(y0), int(x0 + c_size + 65), int(y0))

        # Draw subtle dashed line accent at bottom right
        painter.drawLine(int(x1 - c_size - 40), int(y1), int(x1 - c_size - 6), int(y1))
