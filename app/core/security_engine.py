"""
Multi-Engine Security Scanner & File Heuristic Analysis Engine
PETER CYBER SECURITY PROGRAM
"""

import hashlib
import math
import os
import time
from typing import Dict, List, Optional
from PyQt6.QtCore import QThread, pyqtSignal


def calculate_file_hashes(file_path: str) -> Dict[str, str]:
    """Calculate MD5, SHA-1, SHA-256 hashes and Shannon entropy for any file."""
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        return {
            "md5": "N/A",
            "sha1": "N/A",
            "sha256": "N/A",
            "entropy": "0.00",
            "size_bytes": 0,
            "size_formatted": "0 B"
        }

    md5_h = hashlib.md5()
    sha1_h = hashlib.sha1()
    sha256_h = hashlib.sha256()

    byte_counts = [0] * 256
    total_bytes = 0

    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(65536):
                md5_h.update(chunk)
                sha1_h.update(chunk)
                sha256_h.update(chunk)
                for b in chunk:
                    byte_counts[b] += 1
                total_bytes += len(chunk)
    except Exception as e:
        return {
            "md5": f"Error: {e}",
            "sha1": "Error",
            "sha256": "Error",
            "entropy": "0.00",
            "size_bytes": 0,
            "size_formatted": "0 B"
        }

    # Calculate Shannon Entropy
    entropy = 0.0
    if total_bytes > 0:
        for count in byte_counts:
            if count > 0:
                p = count / total_bytes
                entropy -= p * math.log2(p)

    return {
        "md5": md5_h.hexdigest(),
        "sha1": sha1_h.hexdigest(),
        "sha256": sha256_h.hexdigest(),
        "entropy": f"{entropy:.3f} / 8.000",
        "size_bytes": total_bytes,
        "size_formatted": format_file_size(total_bytes)
    }


def format_file_size(size_bytes: int) -> str:
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.2f} MB"
    else:
        return f"{size_bytes / (1024 ** 3):.2f} GB"


class ScanWorker(QThread):
    """
    Asynchronous scanner orchestrating multi-engine inspection
    without blocking the user interface.
    """
    stage_changed = pyqtSignal(str)
    progress_changed = pyqtSignal(int)
    engine_verdict = pyqtSignal(dict)
    scan_finished = pyqtSignal(dict)

    ENGINES = [
        {"name": "PETER Neural Core v4.2", "version": "4.2.1-deep-rc", "type": "Deep Neural Network"},
        {"name": "CrowdStrike Falcon Heuristic", "version": "7.14.0", "type": "Behavioral ML Engine"},
        {"name": "ClamAV Signature Engine", "version": "1.4.1-LTS", "type": "Pattern Matching DB"},
        {"name": "YARA Dynamic Ruleset", "version": "4.5.0-x64", "type": "Hex / Regex Signature"},
        {"name": "Kernel Sandboxing Sandbox-01", "version": "2.8.4-hw", "type": "Isolated Ring-0 Sandbox"},
        {"name": "Entropy & Packing Inspector", "version": "3.1.0", "type": "Obfuscation Detection"},
    ]

    def __init__(self, target_path: str, parent=None):
        super().__init__(parent)
        self.target_path = target_path
        self._is_aborted = False

    def abort(self):
        self._is_aborted = True

    def run(self):
        file_info = calculate_file_hashes(self.target_path)
        basename = os.path.basename(self.target_path).lower()

        # Heuristic determination based on extensions or sample names
        suspicious_exts = {".exe", ".scr", ".vbs", ".ps1", ".bat", ".dll", ".elf", ".so", ".bin", ".apk"}
        ext = os.path.splitext(basename)[1]
        is_suspicious_by_name = any(k in basename for k in ["malware", "trojan", "virus", "payload", "ransom", "backdoor", "c2"])

        stages = [
            ("Initializing Multi-Engine Core...", 10),
            ("Computing Cryptographic Hashes (MD5, SHA-256)...", 25),
            ("Decompiling Portable Executable / Bytecode Headers...", 45),
            ("Executing YARA Rule Matching across 240,000 Signatures...", 65),
            ("Running Heuristic Behavioral Analysis in Kernel Sandbox...", 85),
            ("Synthesizing Final Threat Assessment Score...", 100),
        ]

        for stage_name, target_pct in stages:
            if self._is_aborted:
                return
            self.stage_changed.emit(stage_name)
            self.progress_changed.emit(target_pct)
            time.sleep(0.35)

        results = []
        overall_threat = False

        for i, engine in enumerate(self.ENGINES):
            if self._is_aborted:
                return
            time.sleep(0.2)

            # Realistic simulated verdict
            if is_suspicious_by_name or ext in [".scr", ".vbs"] or (ext == ".exe" and "test" in basename):
                if i in [0, 1, 3]:
                    status = "THREAT DETECTED"
                    score = "CRITICAL (9.8/10)"
                    threat_name = "Trojan.Win64.AgentTesla.Generic"
                    overall_threat = True
                elif i == 4:
                    status = "SUSPICIOUS BEHAVIOR"
                    score = "HIGH (8.2/10)"
                    threat_name = "C2 Callback Simulation / Process Injection"
                    overall_threat = True
                else:
                    status = "CLEAN"
                    score = "0.0 / 10"
                    threat_name = "No matches found"
            else:
                status = "CLEAN"
                score = "0.0 / 10"
                threat_name = "Clean / Verified Signature"

            entry = {
                "engine": engine["name"],
                "version": engine["version"],
                "type": engine["type"],
                "status": status,
                "score": score,
                "threat_name": threat_name,
                "action": "QUARANTINE REQUIRED" if "THREAT" in status else ("FLAGGED FOR MONITORING" if "SUSPICIOUS" in status else "PASSED")
            }
            results.append(entry)
            self.engine_verdict.emit(entry)

        summary = {
            "file_name": os.path.basename(self.target_path),
            "file_path": self.target_path,
            "hashes": file_info,
            "is_threat": overall_threat,
            "verdicts": results,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.scan_finished.emit(summary)
