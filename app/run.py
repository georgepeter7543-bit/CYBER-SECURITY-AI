#!/usr/bin/env python3
"""
Launcher alias for app/main.py
Ensures `python run.py` works seamlessly even when invoked inside the `app/` folder.
"""

import sys
import os

current_dir = os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
for p in [current_dir, parent_dir]:
    if p not in sys.path:
        sys.path.insert(0, p)

from app.main import run_api_server, run_desktop_gui

if __name__ == "__main__":
    if "--desktop" in sys.argv or "-d" in sys.argv:
        run_desktop_gui()
    else:
        run_api_server()
