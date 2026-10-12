#!/usr/bin/env python3
"""
Quick Launcher for PETER CYBER SECURITY PROGRAM
"""

import sys
import os

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.main import main

if __name__ == "__main__":
    main()
