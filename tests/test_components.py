"""
Automated Component & Architecture Tests
PETER CYBER SECURITY PROGRAM
"""

import os
import sys
import unittest

# Ensure project root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Offscreen platform for headless test execution
os.environ["QT_QPA_PLATFORM"] = "offscreen"

from PyQt6.QtWidgets import QApplication

from app.core.config import GLOBAL_NODES, REGIONS, CyberTheme
from app.core.security_engine import calculate_file_hashes, ScanWorker
from app.core.system_monitor import SystemMonitorWorker
from app.ui.modules.virus_scanner import VirusScannerModule
from app.ui.modules.threat_map import ThreatMapModule
from app.ui.modules.ai_assistant import AIAssistantModule
from app.ui.modules.vulnerability_view import VulnerabilityOverviewModule
from app.ui.main_window import MainWindow


class TestCyberSecurityProgram(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create single QApplication instance for Qt tests
        cls.app = QApplication.instance() or QApplication(sys.argv)

    def test_global_nodes_and_regions(self):
        """Verify presence of East Africa / Arusha Tanzania nodes and regions."""
        self.assertIn("ARUSHA", GLOBAL_NODES)
        arusha = GLOBAL_NODES["ARUSHA"]
        self.assertTrue(arusha.is_hq)
        self.assertEqual(arusha.region, "EAST AFRICA")
        self.assertIn("EAST AFRICA", REGIONS)
        self.assertIn("AFRICA", REGIONS)
        self.assertIn("WORLD", REGIONS)

    def test_file_hash_and_entropy_calculation(self):
        """Verify MD5, SHA-256 and Shannon entropy calculations on a sample file."""
        test_file = os.path.join(os.path.dirname(__file__), "sample_test.bin")
        with open(test_file, "wb") as f:
            f.write(b"PETER_CYBER_SECURITY_ZERO_TRUST_VERIFIED_SIGNATURE_KEY_2026")

        try:
            hashes = calculate_file_hashes(test_file)
            self.assertIn("md5", hashes)
            self.assertIn("sha256", hashes)
            self.assertIn("entropy", hashes)
            self.assertNotEqual(hashes["md5"], "N/A")
            self.assertGreater(hashes["size_bytes"], 0)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_system_monitor_telemetry(self):
        """Verify telemetry monitor produces CPU, RAM and network metrics."""
        worker = SystemMonitorWorker()
        data = worker._gather_telemetry()
        self.assertIn("cpu_percent", data)
        self.assertIn("ram_percent", data)
        self.assertIn("tx_speed", data)
        self.assertIn("rx_speed", data)
        self.assertIn("model_status", data)

    def test_ui_modules_initialization(self):
        """Verify that all 4 required modules initialize cleanly."""
        scanner = VirusScannerModule()
        self.assertIsNotNone(scanner.drop_zone)
        self.assertIsNotNone(scanner.result_table)

        threat_map = ThreatMapModule()
        self.assertIsNotNone(threat_map.canvas)
        self.assertIsNotNone(threat_map.feed_table)

        ai_chat = AIAssistantModule()
        self.assertIsNotNone(ai_chat.input_console)
        self.assertIsNotNone(ai_chat.scroll_area)
        self.assertIsNotNone(ai_chat.btn_hamburger)
        self.assertIsNotNone(ai_chat.btn_new_chat)

        vuln_view = VulnerabilityOverviewModule()
        self.assertIsNotNone(vuln_view.tree_widget)
        self.assertIsNotNone(vuln_view.card_cve)

    def test_main_window_assembly(self):
        """Verify MainWindow integrates top bar, pills, and stacked modules."""
        win = MainWindow()
        self.assertEqual(win.stacked_widget.count(), 4)
        self.assertIsNotNone(win.pill_cpu)
        self.assertIsNotNone(win.pill_ram)
        self.assertIsNotNone(win.pill_ai)
        self.assertIsNotNone(win.pill_net)
        win.close()


    def test_threat_canvas_projection(self):
        """Verify ThreatCanvas projects coordinates and supports East Africa filter."""
        threat_map = ThreatMapModule()
        # Verify region bounds
        self.assertIn("EAST AFRICA", threat_map.canvas.region_bounds)
        threat_map._on_region_selected("EAST AFRICA")
        self.assertEqual(threat_map.canvas.current_region, "EAST AFRICA")

        # Verify Arusha HQ coordinates project to valid points
        arusha = GLOBAL_NODES["ARUSHA"]
        pt = threat_map.canvas._project_latlon(arusha.lat, arusha.lon)
        self.assertGreater(pt.x(), 0)
        self.assertGreater(pt.y(), 0)

    def test_ai_command_generation(self):
        """Verify AI assistant responds to HackerGPT recon queries."""
        ai_module = AIAssistantModule()
        ai_module._on_message_submitted("Check cybergym.hackergpt.app/")
        # Ensure chat container received widgets
        self.assertGreater(ai_module.chat_layout.count(), 1)


if __name__ == "__main__":
    unittest.main()

