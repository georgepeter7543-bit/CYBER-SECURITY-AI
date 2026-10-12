"""
PETER CYBER SECURITY PROGRAM - Unified Backend Entry Point
Supports both Flask REST API Backend (for Vite/React Frontend) and PyQt6 Desktop GUI.
"""

import sys
import os
import time
import json
import random

# Ensure both current directory and parent directory are on sys.path
current_dir = os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
for path in [parent_dir, current_dir]:
    if path not in sys.path:
        sys.path.insert(0, path)

try:
    from app.core.config import APP_TITLE, APP_VERSION, GLOBAL_NODES
    from app.core.security_engine import calculate_file_hashes
    from app.core.system_monitor import HAS_PSUTIL
    if HAS_PSUTIL:
        import psutil
except ImportError:
    HAS_PSUTIL = False


# =====================================================================
# 1. FLASK REST API SERVER (For Vite/React Frontend: npm run dev)
# =====================================================================
def run_api_server(host=None, port=None):
    """Launches the Flask backend API server for the React frontend."""
    from flask import Flask, jsonify, request, send_from_directory
    from flask_cors import CORS

    # Cloud hosting support (Render, Railway, Fly.io provide PORT in environment)
    if port is None:
        port = int(os.environ.get("PORT", 5000))
    if host is None:
        host = os.environ.get("HOST", "0.0.0.0" if "PORT" in os.environ else "127.0.0.1")

    dist_folder = os.path.abspath(os.path.join(current_dir, "ui", "dist"))

    # Initialize Flask with static_folder=None so catch-all route handles both static assets and SPA fallback
    app = Flask(__name__, static_folder=None)
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

    print("\n" + "="*65)
    print(" 🛡️  PETER CYBER SECURITY PROGRAM - BACKEND API SERVER")
    print("="*65)
    print(f" [*] Status:   Active and Listening")
    print(f" [*] Host/Port: {host}:{port}")
    print(f" [*] Endpoint: http://{host}:{port}/api/status")
    print(f" [*] Frontend: Connect via Vercel or http://localhost:5173")
    print("="*65 + "\n")

    @app.route("/api/status", methods=["GET"])
    def get_status():
        return jsonify({
            "status": "ONLINE",
            "version": "4.8.2-ENTERPRISE",
            "model": "NEURAL-DEFENSE v4.2",
            "hq": "Arusha HQ, Tanzania",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        })

    @app.route("/api/telemetry", methods=["GET"])
    def get_telemetry():
        cpu = 18.5
        ram_used = 7.8
        ram_total = 16.0
        if HAS_PSUTIL:
            try:
                cpu = psutil.cpu_percent(interval=None)
                mem = psutil.virtual_memory()
                ram_used = round(mem.used / (1024**3), 1)
                ram_total = round(mem.total / (1024**3), 1)
            except Exception:
                pass
        else:
            cpu = round(15 + random.uniform(-3, 8), 1)

        return jsonify({
            "cpu_percent": cpu,
            "ram_used_gb": ram_used,
            "ram_total_gb": ram_total,
            "net_tx_mb": round(20 + random.uniform(2, 14), 1),
            "net_rx_mb": round(90 + random.uniform(10, 30), 1),
            "model_status": "ONLINE"
        })

    @app.route("/api/scan", methods=["POST"])
    def post_scan():
        data = request.json or {}
        filename = data.get("filename", "sample_payload.bin")
        return jsonify({
            "target": filename,
            "md5": "4a2b9f1092e01bca7f8842ad910c2e41",
            "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "entropy": "7.914 / 8.000",
            "status": "THREAT DETECTED",
            "verdicts": [
                {"engine": "PETER Neural Core v4.2", "status": "THREAT DETECTED", "vector": "Trojan.Win64.AgentTesla.Generic", "score": "9.8 / 10", "action": "QUARANTINE"},
                {"engine": "CrowdStrike Falcon Heuristic", "status": "SUSPICIOUS BEHAVIOR", "vector": "Process Injection / Memory Hollowing", "score": "8.4 / 10", "action": "FLAGGED"},
                {"engine": "ClamAV Signature Engine", "status": "THREAT DETECTED", "vector": "Win.Trojan.Agent-9921", "score": "9.5 / 10", "action": "QUARANTINE"},
                {"engine": "Kernel Sandboxing Sandbox-01", "status": "ANOMALOUS ACTIVITY", "vector": "C2 Beaconing via port 4444", "score": "9.1 / 10", "action": "TERMINATED"},
            ]
        })

    @app.route("/api/recon", methods=["POST"])
    def post_recon():
        data = request.json or {}
        query = data.get("query", "cybergym.hackergpt.app")
        target = query.replace("Check ", "").replace("check ", "").replace("scan ", "").strip().rstrip("/")
        is_arusha = any(k in target.lower() for k in ["arusha", "tz", "tanzania"])

        ip = "102.214.32.14" if is_arusha else "34.231.169.117"
        whois = "tzNIC - Peter Defense Grid Arusha" if is_arusha else "No publicly-available WHOIS record was returned for the sub-domain."

        return jsonify({
            "target": target,
            "ip": ip,
            "whois": whois,
            "fingerprint": {
                "target": f"http://{target}",
                "http_status": 200,
                "request_config": {
                    "headers": {
                        "User-Agent": "HackerGPT/4.2 (Zero-Trust Recon Engine; x64)"
                    }
                },
                "plugins": {
                    "Country": {"string": ["TANZANIA" if is_arusha else "UNITED STATES"], "module": ["TZ" if is_arusha else "US"]},
                    "HTML5": {},
                    "IP": {"string": [ip]},
                    "JQuery": {"version": ["2.2.4"]},
                    "WAF": {"string": ["Cloudflare / Peter Shield Active"]},
                    "Title": {"string": ["CyberGym"]},
                    "UncommonHeaders": {"string": ["access-control-allow-origin,x-content-type-options,feature-policy,x-re..."]}
                }
            }
        })

    @app.route("/api/threats", methods=["GET"])
    def get_threats():
        return jsonify({
            "active_arcs": 4,
            "region": "GLOBAL",
            "feed": [
                {"time": time.strftime("%H:%M:%S"), "origin": "Frankfurt IXP", "target": "Arusha HQ (Tanzania)", "vector": "DDoS SYN-Flood Incursion", "severity": "CRITICAL", "action": "BLOCKED (Peter Core)"},
                {"time": time.strftime("%H:%M:%S"), "origin": "Silicon Valley Cloud", "target": "Nairobi Gateway", "vector": "Zero-Day Kerberos Exploit", "severity": "HIGH", "action": "BLOCKED"},
                {"time": time.strftime("%H:%M:%S"), "origin": "London Cyber Command", "target": "Johannesburg Sentinel", "vector": "Credential Stuffing Wave", "severity": "MEDIUM", "action": "RATE-LIMITED"},
            ]
        })

    @app.route("/api/vulnerabilities", methods=["GET"])
    def get_vulnerabilities():
        return jsonify({
            "posture_score": 94.8,
            "active_cves": 3,
            "zero_trust_compliance": "98.7%",
            "monitored_daemons": 4
        })

    # =================================================================
    # Unified SPA Static Route & Fallback Handler
    # =================================================================
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_frontend(path):
        # Do not catch unresolved API endpoints
        if path.startswith("api/"):
            return jsonify({"error": "API route not found", "path": f"/{path}"}), 404

        # Serve existing static assets (e.g., /assets/index-xxx.js, /assets/index-xxx.css, icons)
        if path:
            candidate_path = os.path.join(dist_folder, path)
            if os.path.isfile(candidate_path):
                return send_from_directory(dist_folder, path)

        # Serve index.html for all client-side SPA routes (e.g., /, /dashboard, /scanner, /threat-map)
        index_file = os.path.join(dist_folder, "index.html")
        if os.path.isfile(index_file):
            return send_from_directory(dist_folder, "index.html")

        # Fallback if frontend dist/ has not been built yet
        return jsonify({
            "status": "ONLINE",
            "message": "PETER CYBER SECURITY PROGRAM Unified Backend is active.",
            "note": "Frontend static bundle not found at app/ui/dist/. Run 'npm run build' inside app/ui/ to build the frontend.",
            "api_endpoints": [
                "/api/status",
                "/api/telemetry",
                "/api/scan",
                "/api/recon",
                "/api/threats",
                "/api/vulnerabilities"
            ]
        }), 200

    app.run(host=host, port=port, debug=False)


# =====================================================================
# 2. DESKTOP GUI RUNNER (PyQt6 Native Mode)
# =====================================================================
def run_desktop_gui():
    """Launches the PyQt6 Native Desktop Application."""
    from PyQt6.QtCore import Qt
    from PyQt6.QtGui import QFont, QPalette, QColor, QIcon
    from PyQt6.QtWidgets import QApplication
    from app.core.config import CyberTheme
    from app.ui.main_window import MainWindow
    from app.ui.style import get_application_stylesheet

    if hasattr(Qt.ApplicationAttribute, "AA_UseHighDpiPixmaps"):
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setApplicationName("PETER CYBER SECURITY PROGRAM")

    icon_path = os.path.join(parent_dir, "IMAGES", "the ai .png")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    font = QFont("Segoe UI", 10)
    app.setFont(font)
    app.setStyleSheet(get_application_stylesheet())

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


# =====================================================================
# MAIN ENTRY POINT
# =====================================================================
if __name__ == "__main__":
    # If explicitly passed --desktop, run PyQt6 native desktop window
    if "--desktop" in sys.argv or "-d" in sys.argv:
        run_desktop_gui()
    else:
        # Default mode: Run Flask API backend (supports npm run dev on port 5173)
        run_api_server()
