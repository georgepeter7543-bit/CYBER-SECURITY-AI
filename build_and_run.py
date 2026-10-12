#!/usr/bin/env python3
"""
PETER CYBER SECURITY PROGRAM - Unified Build & Launch Script
1. Builds the static React frontend bundle into `app/ui/dist/`
2. Starts the unified Python Flask server in `app/main.py`
"""

import os
import sys
import subprocess
import shutil

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
UI_DIR = os.path.join(ROOT_DIR, "app", "ui")
DIST_DIR = os.path.join(UI_DIR, "dist")
MAIN_PY = os.path.join(ROOT_DIR, "app", "main.py")

def build_frontend():
    print("\n" + "="*65)
    print(" [1/2] 📦 Compiling React Frontend (`npm run build` in app/ui)...")
    print("="*65)
    
    npm_cmd = shutil.which("npm") or shutil.which("npm.cmd")
    if not npm_cmd:
        print(" [!] Warning: npm was not found in PATH.")
        if os.path.exists(DIST_DIR):
            print(" [*] Found existing dist/ bundle. Proceeding with existing build.")
            return True
        else:
            print(" [X] Error: Cannot build frontend without npm.")
            return False

    try:
        subprocess.check_call([npm_cmd, "run", "build"], cwd=UI_DIR)
        print(" [✓] Frontend build completed successfully -> app/ui/dist/")
        return True
    except subprocess.CalledProcessError as e:
        print(f" [!] Build returned code {e.returncode}. Checking for dist/ folder...")
        return os.path.exists(DIST_DIR)

def start_backend():
    print("\n" + "="*65)
    print(" [2/2] 🚀 Launching Unified Full-Stack Application (`python app/main.py`)...")
    print("="*65 + "\n")
    
    # Run app/main.py
    sys.path.insert(0, ROOT_DIR)
    sys.path.insert(0, os.path.join(ROOT_DIR, "app"))
    
    from app.main import run_api_server
    run_api_server()

if __name__ == "__main__":
    skip_build = "--skip-build" in sys.argv
    if not skip_build:
        success = build_frontend()
        if not success:
            print(" [X] Halting due to frontend build error.")
            sys.exit(1)
    
    start_backend()
