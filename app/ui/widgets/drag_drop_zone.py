"""
Native File Drag-and-Drop Dropzone Widget
PETER CYBER SECURITY PROGRAM
"""

import os
from PyQt6.QtCore import Qt, pyqtSignal, QRectF, QPointF
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QPainterPath
from PyQt6.QtWidgets import QWidget, QFileDialog

from app.core.config import CyberTheme


class NativeDropZoneWidget(QWidget):
    """
    Hardware-rendered native Drag-and-Drop zone with cyber borders,
    hover highlights, and file picker fallback.
    """
    file_selected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setMinimumHeight(180)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self._is_drag_active = False
        self._current_file_path: str = ""
        self._pulse_alpha = 180

    def set_file_path(self, path: str):
        self._current_file_path = path
        self.update()

    def clear(self):
        self._current_file_path = ""
        self.update()

    # ----------------------------------------------------
    # Native Drag & Drop Handlers
    # ----------------------------------------------------
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self._is_drag_active = True
            self.update()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self._is_drag_active = False
        self.update()

    def dropEvent(self, event):
        self._is_drag_active = False
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            if os.path.exists(file_path):
                self._current_file_path = file_path
                self.file_selected.emit(file_path)
                event.acceptProposedAction()
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._open_file_dialog()

    def _open_file_dialog(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Binary / File for Deep Heuristic Inspection",
            "",
            "Executable / Binary Files (*.exe *.dll *.elf *.bin *.sys *.ps1 *.bat *.vbs *.apk *.zip);;All Files (*.*)"
        )
        if path:
            self._current_file_path = path
            self.file_selected.emit(path)
            self.update()

    # ----------------------------------------------------
    # Native QPainter Vector Rendering
    # ----------------------------------------------------
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect().adjusted(6, 6, -6, -6)
        width = rect.width()
        height = rect.height()

        # Background fill
        if self._is_drag_active:
            bg_color = QColor(0, 255, 102, 28)
            border_color = QColor(CyberTheme.COLOR_SCANNER)
            pen_style = Qt.PenStyle.SolidLine
        else:
            bg_color = QColor(16, 18, 24)
            border_color = QColor(36, 42, 58)
            pen_style = Qt.PenStyle.DashLine

        # Draw main rounded container
        painter.setBrush(QBrush(bg_color))
        pen = QPen(border_color, 1.5, pen_style)
        pen.setDashPattern([6, 5])
        painter.setPen(pen)
        painter.drawRoundedRect(QRectF(rect), 8, 8)

        # Draw High-Tech Cyber Corner Brackets
        corner_len = 16
        bracket_pen = QPen(QColor(CyberTheme.COLOR_SCANNER), 2)
        painter.setPen(bracket_pen)
        # Top-left
        painter.drawLine(int(rect.left()), int(rect.top() + corner_len), int(rect.left()), int(rect.top()))
        painter.drawLine(int(rect.left()), int(rect.top()), int(rect.left() + corner_len), int(rect.top()))
        # Top-right
        painter.drawLine(int(rect.right() - corner_len), int(rect.top()), int(rect.right()), int(rect.top()))
        painter.drawLine(int(rect.right()), int(rect.top()), int(rect.right()), int(rect.top() + corner_len))
        # Bottom-left
        painter.drawLine(int(rect.left()), int(rect.bottom() - corner_len), int(rect.left()), int(rect.bottom()))
        painter.drawLine(int(rect.left()), int(rect.bottom()), int(rect.left() + corner_len), int(rect.bottom()))
        # Bottom-right
        painter.drawLine(int(rect.right() - corner_len), int(rect.bottom()), int(rect.right()), int(rect.bottom()))
        painter.drawLine(int(rect.right()), int(rect.bottom()), int(rect.right()), int(rect.bottom() - corner_len))

        # Center vector icon: Cyber Shield
        center_x = rect.center().x()
        shield_top = rect.top() + 25

        self._draw_cyber_shield(painter, center_x, shield_top)

        # Instructions Text
        painter.setPen(QColor(CyberTheme.TEXT_MAIN if not self._is_drag_active else CyberTheme.COLOR_SCANNER))
        font_main = QFont("Segoe UI", 12, QFont.Weight.Bold)
        painter.setFont(font_main)

        if self._current_file_path:
            display_name = os.path.basename(self._current_file_path)
            painter.drawText(
                int(rect.left()), int(shield_top + 65), int(width), 24,
                Qt.AlignmentFlag.AlignHCenter,
                f"LOADED TARGET: {display_name}"
            )
            painter.setPen(QColor(CyberTheme.TEXT_MUTED))
            font_sub = QFont("Consolas", 10)
            painter.setFont(font_sub)
            painter.drawText(
                int(rect.left()), int(shield_top + 92), int(width), 20,
                Qt.AlignmentFlag.AlignHCenter,
                f"Path: {self._current_file_path}"
            )
        else:
            painter.drawText(
                int(rect.left()), int(shield_top + 65), int(width), 24,
                Qt.AlignmentFlag.AlignHCenter,
                "DRAG & DROP SUSPICIOUS BINARY / SAMPLE FILE HERE"
            )

            painter.setPen(QColor(CyberTheme.TEXT_MUTED))
            font_sub = QFont("Segoe UI", 10)
            painter.setFont(font_sub)
            painter.drawText(
                int(rect.left()), int(shield_top + 92), int(width), 20,
                Qt.AlignmentFlag.AlignHCenter,
                "Supported: .exe, .dll, .bin, .ps1, .vbs, .elf, .apk, .sys, archives | Click to Browse Filesystem"
            )

    def _draw_cyber_shield(self, painter: QPainter, cx: float, cy: float):
        """Draws a native geometric vector cybersecurity shield."""
        path = QPainterPath()
        # Shield geometry
        w = 18
        h = 24
        path.moveTo(cx, cy)
        path.lineTo(cx + w, cy + 6)
        path.lineTo(cx + w, cy + h - 6)
        path.quadTo(cx, cy + h + 10, cx, cy + h + 14)
        path.quadTo(cx, cy + h + 10, cx - w, cy + h - 6)
        path.lineTo(cx - w, cy + 6)
        path.closeSubpath()

        glow_color = QColor(CyberTheme.COLOR_SCANNER if self._is_drag_active else "#2A3344")
        painter.setBrush(QBrush(QColor(0, 255, 102, 35) if self._is_drag_active else QColor(25, 30, 42)))
        painter.setPen(QPen(glow_color, 2))
        painter.drawPath(path)

        # Inner crosshair tick
        painter.setPen(QPen(QColor(CyberTheme.COLOR_SCANNER), 1.5))
        painter.drawLine(int(cx - 6), int(cy + 13), int(cx + 6), int(cy + 13))
        painter.drawLine(int(cx), int(cy + 7), int(cx), int(cy + 19))
