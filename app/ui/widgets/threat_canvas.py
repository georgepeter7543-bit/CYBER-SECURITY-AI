"""
Hardware-Accelerated 2D Vector Threat Map Canvas
PETER CYBER SECURITY PROGRAM
"""

import math
import random
import time
from typing import Dict, List, Optional, Tuple

from PyQt6.QtCore import Qt, QTimer, QPointF, QRectF, pyqtSignal
from PyQt6.QtGui import (
    QPainter, QColor, QPen, QBrush, QFont, QPainterPath,
    QRadialGradient, QLinearGradient, QConicalGradient
)
from PyQt6.QtWidgets import QWidget

from app.core.config import CyberTheme, GLOBAL_NODES, MapNode


class AttackArc:
    """Represents an active animated attack trajectory between two nodes."""
    def __init__(self, origin: MapNode, target: MapNode, threat_type: str, severity: str):
        self.origin = origin
        self.target = target
        self.threat_type = threat_type
        self.severity = severity
        self.progress = 0.0      # 0.0 to 1.0
        self.speed = random.uniform(0.012, 0.024)
        self.impact_active = False
        self.impact_radius = 0.0
        self.impact_max_radius = 28.0
        self.impact_alpha = 255
        self.finished = False

        if severity == "CRITICAL":
            self.color = QColor(CyberTheme.SEVERITY_CRITICAL)
        elif severity == "HIGH":
            self.color = QColor(CyberTheme.SEVERITY_HIGH)
        elif severity == "MEDIUM":
            self.color = QColor(CyberTheme.SEVERITY_MEDIUM)
        else:
            self.color = QColor(CyberTheme.SEVERITY_LOW)


class ThreatCanvasWidget(QWidget):
    """
    2D Custom Canvas rendering global node connections,
    animated Bezier attack arcs, dynamic radar sweeps, and regional focus.
    """
    threat_intercepted = pyqtSignal(dict)

    # Simplified continent polygon definitions for high-tech vector styling
    CONTINENT_PATHS_LATLON = [
        # Africa
        [(37, 10), (32, 32), (12, 51), (-12, 40), (-34, 18), (-34, 26), (-15, 12), (5, 9), (14, -17), (28, -13), (35, -5), (37, 10)],
        # Europe
        [(36, -9), (43, -9), (48, -4), (54, 5), (60, 5), (71, 28), (60, 30), (45, 35), (41, 28), (38, 24), (36, 15), (38, -1), (36, -9)],
        # North America
        [(70, -165), (70, -70), (50, -55), (25, -80), (15, -90), (18, -105), (32, -118), (48, -125), (60, -140), (70, -165)],
        # South America
        [(12, -73), (7, -55), (-5, -35), (-22, -41), (-55, -67), (-52, -75), (-20, -70), (-2, -80), (12, -73)],
        # Asia
        [(75, 40), (75, 180), (60, 160), (40, 140), (22, 120), (10, 105), (20, 85), (25, 60), (40, 50), (60, 45), (75, 40)],
        # Australia
        [(-12, 130), (-15, 145), (-25, 153), (-38, 145), (-35, 115), (-22, 114), (-12, 130)]
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(540, 380)
        self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent, False)
        self.setMouseTracking(True)

        self.current_region = "WORLD"
        self.active_arcs: List[AttackArc] = []
        self.hovered_node: Optional[MapNode] = None

        # Regional Viewports: (min_lat, max_lat, min_lon, max_lon)
        self.region_bounds = {
            "WORLD": (-60.0, 78.0, -160.0, 170.0),
            "AFRICA": (-38.0, 40.0, -22.0, 55.0),
            "EAST AFRICA": (-15.0, 6.0, 26.0, 45.0),  # Tightly focused on Arusha / Tanzania & EA corridor
            "EUROPE": (34.0, 72.0, -15.0, 40.0),
            "AMERICAS": (-58.0, 72.0, -130.0, -32.0),
        }

        # Animated elements
        self._radar_angle = 0.0
        self._pulse_ring_radius = 4.0
        self._pulse_direction = 0.25

        # 40 FPS Animation Timer
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self._on_animation_tick)
        self.anim_timer.start(25)

        # Attack Arc Generation Timer
        self.arc_spawner = QTimer(self)
        self.arc_spawner.timeout.connect(self._spawn_random_attack)
        self.arc_spawner.start(1800)

        # Spawn initial attacks immediately
        for _ in range(3):
            self._spawn_random_attack()

    def set_region_filter(self, region: str):
        if region in self.region_bounds:
            self.current_region = region
            self.update()

    def _on_animation_tick(self):
        # Update radar sweep
        self._radar_angle = (self._radar_angle + 1.8) % 360.0

        # Update pulsing HQ rings
        self._pulse_ring_radius += self._pulse_direction
        if self._pulse_ring_radius > 16.0:
            self._pulse_ring_radius = 4.0

        # Update active attack arcs
        for arc in self.active_arcs:
            if not arc.impact_active:
                arc.progress += arc.speed
                if arc.progress >= 1.0:
                    arc.progress = 1.0
                    arc.impact_active = True
            else:
                arc.impact_radius += 1.4
                arc.impact_alpha = max(0, int(255 * (1.0 - (arc.impact_radius / arc.impact_max_radius))))
                if arc.impact_radius >= arc.impact_max_radius:
                    arc.finished = True

        # Remove finished arcs
        self.active_arcs = [a for a in self.active_arcs if not a.finished]
        self.update()

    def _spawn_random_attack(self):
        nodes_list = list(GLOBAL_NODES.values())
        if len(nodes_list) < 2:
            return

        # Prioritize Arusha or East Africa as target or origin to emphasize regional focus
        if random.random() < 0.5:
            target = GLOBAL_NODES["ARUSHA"]
            candidates = [n for n in nodes_list if n.id != "ARUSHA"]
            origin = random.choice(candidates)
        else:
            origin = random.choice(nodes_list)
            candidates = [n for n in nodes_list if n.id != origin.id]
            target = random.choice(candidates)

        threat_types = [
            ("DDoS SYN-Flood Incursion", "CRITICAL"),
            ("Advanced Persistent Threat (APT-41 Callback)", "CRITICAL"),
            ("Ransomware Lateral Move", "HIGH"),
            ("Zero-Day Kerberos Exploit", "HIGH"),
            ("Credential Stuffing Wave", "MEDIUM"),
            ("Automated Vulnerability Scan", "LOW"),
            ("DNS Tunneling Exfiltration", "HIGH")
        ]
        threat_name, severity = random.choice(threat_types)

        arc = AttackArc(origin, target, threat_name, severity)
        self.active_arcs.append(arc)

        # Notify feed table
        self.threat_intercepted.emit({
            "timestamp": time.strftime("%H:%M:%S"),
            "origin": origin.name,
            "target": target.name,
            "vector": threat_name,
            "severity": severity,
            "mitigation": "BLOCKED (Peter Defense Core)" if severity in ["CRITICAL", "HIGH"] else "MONITORED"
        })

    # -----------------------------------------------------------------
    # Coordinate Projection Engine
    # -----------------------------------------------------------------
    def _project_latlon(self, lat: float, lon: float) -> QPointF:
        """Projects latitude/longitude into canvas (x, y) with regional viewport bounds."""
        min_lat, max_lat, min_lon, max_lon = self.region_bounds[self.current_region]

        w = self.width() - 40
        h = self.height() - 40

        # Normalization with margin
        norm_x = (lon - min_lon) / (max_lon - min_lon)
        norm_y = (max_lat - lat) / (max_lat - min_lat)

        x = 20 + norm_x * w
        y = 20 + norm_y * h
        return QPointF(x, y)

    # -----------------------------------------------------------------
    # Native Painting
    # -----------------------------------------------------------------
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Deep stealth obsidian background
        painter.fillRect(self.rect(), QColor(CyberTheme.BG_OBSIDIAN))

        # 1. High-Tech Tactical Grid
        self._draw_tactical_grid(painter)

        # 2. Continent Landmass Polygons
        self._draw_continents(painter)

        # 3. Static Mesh Connections (Network Backbone)
        self._draw_backbone_mesh(painter)

        # 4. Animated Attack Arcs & Impact Ripples
        self._draw_attack_arcs(painter)

        # 5. Global Defense Nodes
        self._draw_nodes(painter)

        # 6. Rotating Radar HUD Sweep
        self._draw_radar_hud(painter)

        # 7. Hover Node Details Popover
        if self.hovered_node:
            self._draw_node_popover(painter, self.hovered_node)

    def _draw_tactical_grid(self, painter: QPainter):
        pen = QPen(QColor(24, 32, 48, 120), 1, Qt.PenStyle.DotLine)
        painter.setPen(pen)

        step_x = 45
        step_y = 45
        w = self.width()
        h = self.height()

        for x in range(0, w, step_x):
            painter.drawLine(x, 0, x, h)
        for y in range(0, h, step_y):
            painter.drawLine(0, y, w, y)

        # Corner Tactical Crosshairs
        cross_pen = QPen(QColor(CyberTheme.COLOR_THREAT_MAP), 1)
        painter.setPen(cross_pen)
        painter.drawText(12, 22, f"GRID: {self.current_region} SECTOR // LAT-LON MERCATOR 2D")
        painter.drawText(w - 180, 22, f"NODES ACTIVE: {len(GLOBAL_NODES)} ONLINE")

    def _draw_continents(self, painter: QPainter):
        """Draws stylistic vector landmass outlines for geospatial context."""
        painter.setBrush(QBrush(QColor(18, 22, 32, 140)))
        painter.setPen(QPen(QColor(36, 48, 70, 160), 1))

        for polygon in self.CONTINENT_PATHS_LATLON:
            path = QPainterPath()
            first = True
            for lat, lon in polygon:
                pt = self._project_latlon(lat, lon)
                if first:
                    path.moveTo(pt)
                    first = False
                else:
                    path.lineTo(pt)
            path.closeSubpath()
            painter.drawPath(path)

    def _draw_backbone_mesh(self, painter: QPainter):
        """Draws faint security mesh interconnects between trusted nodes."""
        pen = QPen(QColor(0, 210, 255, 25), 1, Qt.PenStyle.SolidLine)
        painter.setPen(pen)

        # Predefined mesh connections
        backbones = [
            ("ARUSHA", "DAR"), ("ARUSHA", "NAIROBI"), ("ARUSHA", "KIGALI"), ("ARUSHA", "KAMPALA"),
            ("DAR", "JOHANNESBURG"), ("NAIROBI", "CAIRO"), ("LAGOS", "JOHANNESBURG"),
            ("CAIRO", "FRANKFURT"), ("FRANKFURT", "LONDON"), ("LONDON", "NEW_YORK"),
            ("NEW_YORK", "SILICON_VALLEY"), ("SILICON_VALLEY", "TOKYO"), ("TOKYO", "SINGAPORE"),
            ("SINGAPORE", "DAR"), ("NEW_YORK", "SAO_PAULO")
        ]

        for n1_id, n2_id in backbones:
            if n1_id in GLOBAL_NODES and n2_id in GLOBAL_NODES:
                p1 = self._project_latlon(GLOBAL_NODES[n1_id].lat, GLOBAL_NODES[n1_id].lon)
                p2 = self._project_latlon(GLOBAL_NODES[n2_id].lat, GLOBAL_NODES[n2_id].lon)
                painter.drawLine(p1, p2)

    def _draw_attack_arcs(self, painter: QPainter):
        """Draws curved Bezier attack vectors with flowing particle head and ripples."""
        for arc in self.active_arcs:
            p0 = self._project_latlon(arc.origin.lat, arc.origin.lon)
            p2 = self._project_latlon(arc.target.lat, arc.target.lon)

            # Control Point for Bezier arc curvature
            mid_x = (p0.x() + p2.x()) / 2.0
            mid_y = (p0.y() + p2.y()) / 2.0
            dx = p2.x() - p0.x()
            dy = p2.y() - p0.y()
            dist = math.hypot(dx, dy)

            # Arc curvature displacement perpendicular to vector
            curvature = min(dist * 0.35, 90.0)
            ctrl_pt = QPointF(mid_x - (dy / (dist + 0.001)) * curvature,
                              mid_y + (dx / (dist + 0.001)) * curvature)

            # Draw trajectory path
            path = QPainterPath()
            path.moveTo(p0)
            path.quadTo(ctrl_pt, p2)

            arc_color_dim = QColor(arc.color)
            arc_color_dim.setAlpha(60)
            painter.setPen(QPen(arc_color_dim, 1.5, Qt.PenStyle.DashLine))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawPath(path)

            # Compute current head point along Quadratic Bezier curve
            t = arc.progress
            inv_t = 1.0 - t
            head_x = inv_t * inv_t * p0.x() + 2 * inv_t * t * ctrl_pt.x() + t * t * p2.x()
            head_y = inv_t * inv_t * p0.y() + 2 * inv_t * t * ctrl_pt.y() + t * t * p2.y()
            head_pt = QPointF(head_x, head_y)

            # Glowing projectile packet
            if not arc.impact_active:
                painter.setBrush(QBrush(arc.color))
                painter.setPen(QPen(Qt.GlobalColor.white, 1))
                painter.drawEllipse(head_pt, 4.0, 4.0)

                # Tail glow
                tail_color = QColor(arc.color)
                tail_color.setAlpha(120)
                painter.setBrush(QBrush(tail_color))
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawEllipse(head_pt, 7.0, 7.0)

            # Destination impact ripple
            if arc.impact_active:
                ripple_color = QColor(arc.color)
                ripple_color.setAlpha(arc.impact_alpha)
                painter.setBrush(Qt.BrushStyle.NoBrush)
                painter.setPen(QPen(ripple_color, 2.0))
                painter.drawEllipse(p2, arc.impact_radius, arc.impact_radius)

    def _draw_nodes(self, painter: QPainter):
        """Draws all defense grid nodes with special prominence for Arusha HQ."""
        font_label = QFont("Segoe UI", 9, QFont.Weight.Bold)
        painter.setFont(font_label)

        for node in GLOBAL_NODES.values():
            pt = self._project_latlon(node.lat, node.lon)

            # Filter visibility check if out of canvas viewport
            if pt.x() < -50 or pt.x() > self.width() + 50 or pt.y() < -50 or pt.y() > self.height() + 50:
                continue

            if node.is_hq:
                # Arusha Tanzania - Primary HQ Node
                # Outer pulsing ring
                pulse_color = QColor(CyberTheme.COLOR_SCANNER)
                pulse_color.setAlpha(int(255 * (1.0 - (self._pulse_ring_radius / 16.0))))
                painter.setPen(QPen(pulse_color, 2))
                painter.setBrush(Qt.BrushStyle.NoBrush)
                painter.drawEllipse(pt, self._pulse_ring_radius + 4, self._pulse_ring_radius + 4)

                # Primary HQ Diamond/Circle
                painter.setBrush(QBrush(QColor(CyberTheme.COLOR_SCANNER)))
                painter.setPen(QPen(Qt.GlobalColor.white, 2))
                painter.drawEllipse(pt, 6.0, 6.0)

                # HQ Badge Label
                painter.setPen(QColor(CyberTheme.COLOR_SCANNER))
                painter.drawText(int(pt.x() + 10), int(pt.y() + 4), "★ ARUSHA HQ [TANZANIA]")
            else:
                # Standard Global Node
                is_ea = (node.region == "EAST AFRICA")
                node_color = QColor(CyberTheme.COLOR_THREAT_MAP if not is_ea else "#38BDF8")

                painter.setBrush(QBrush(node_color))
                painter.setPen(QPen(QColor(10, 15, 25), 1.5))
                painter.drawEllipse(pt, 4.0, 4.0)

                painter.setPen(QColor(CyberTheme.TEXT_MUTED))
                painter.drawText(int(pt.x() + 7), int(pt.y() + 3), node.id)

    def _draw_radar_hud(self, painter: QPainter):
        """Draws subtle tactical radar HUD in the bottom-right corner."""
        w = self.width()
        h = self.height()
        cx = w - 60
        cy = h - 60
        radius = 45

        # Radar rings
        painter.setBrush(QBrush(QColor(10, 14, 20, 180)))
        painter.setPen(QPen(QColor(CyberTheme.COLOR_THREAT_MAP), 1, Qt.PenStyle.SolidLine))
        painter.drawEllipse(QPointF(cx, cy), radius, radius)
        painter.drawEllipse(QPointF(cx, cy), radius * 0.6, radius * 0.6)

        # Crosshairs
        painter.setPen(QPen(QColor(0, 210, 255, 80), 1))
        painter.drawLine(int(cx - radius), int(cy), int(cx + radius), int(cy))
        painter.drawLine(int(cx), int(cy - radius), int(cx), int(cy + radius))

        # Sweep beam
        rad = math.radians(self._radar_angle)
        sx = cx + radius * math.cos(rad)
        sy = cy + radius * math.sin(rad)
        painter.setPen(QPen(QColor(CyberTheme.COLOR_THREAT_MAP), 2))
        painter.drawLine(int(cx), int(cy), int(sx), int(sy))

    def _draw_node_popover(self, painter: QPainter, node: MapNode):
        """Draws tactical telemetry HUD when hovering over a node."""
        pt = self._project_latlon(node.lat, node.lon)
        box_w = 210
        box_h = 74
        box_x = pt.x() + 12
        box_y = pt.y() - 40

        if box_x + box_w > self.width():
            box_x = pt.x() - box_w - 12

        painter.setBrush(QBrush(QColor(16, 20, 28, 240)))
        painter.setPen(QPen(QColor(CyberTheme.COLOR_THREAT_MAP), 1.5))
        painter.drawRoundedRect(QRectF(box_x, box_y, box_w, box_h), 6, 6)

        painter.setPen(QColor(CyberTheme.COLOR_THREAT_MAP))
        painter.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        painter.drawText(int(box_x + 8), int(box_y + 18), node.name)

        painter.setPen(QColor(CyberTheme.TEXT_MUTED))
        painter.setFont(QFont("Consolas", 9))
        painter.drawText(int(box_x + 8), int(box_y + 36), f"IP: {node.ip_range}")
        painter.drawText(int(box_x + 8), int(box_y + 52), f"COORDS: {node.lat:.2f}°, {node.lon:.2f}°")
        painter.drawText(int(box_x + 8), int(box_y + 68), f"STATUS: SECURE // ZERO-TRUST ACTIVE")

    def mouseMoveEvent(self, event):
        pos = event.position()
        found: Optional[MapNode] = None

        for node in GLOBAL_NODES.values():
            pt = self._project_latlon(node.lat, node.lon)
            if math.hypot(pt.x() - pos.x(), pt.y() - pos.y()) < 12:
                found = node
                break

        if found != self.hovered_node:
            self.hovered_node = found
            self.update()
