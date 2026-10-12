"""
Configuration, Color Palettes, and System Definitions
PETER CYBER SECURITY PROGRAM
"""

import os
from dataclasses import dataclass
from typing import Dict, Tuple

# Application Metadata
APP_TITLE = "PETER CYBER SECURITY PROGRAM"
APP_SUBTITLE = "ENTERPRISE ZERO-TRUST ARCHITECTURE & THREAT INTELLIGENCE"
APP_VERSION = "4.8.2-ENTERPRISE"
AI_ENGINE_MODEL = "NEURAL-DEFENSE v4.2"

# Color Palette (Obsidian Stealth Theme)
class CyberTheme:
    # Canvas & Backgrounds
    BG_OBSIDIAN = "#0A0A0C"       # Core window background
    BG_SURFACE = "#101217"        # Panel surface
    BG_CARD = "#161922"           # Elevated card surface
    BG_CARD_HOVER = "#1E2230"     # Interactive hover state
    BG_INPUT = "#0D0F14"          # Native input fields
    BG_CODE = "#08090C"           # Monospace code containers

    # Borders & Dividers
    BORDER_DARK = "#1A1E29"
    BORDER_MID = "#252B3B"
    BORDER_LIGHT = "#353D52"

    # Typography
    TEXT_MAIN = "#F1F5F9"
    TEXT_MUTED = "#94A3B8"
    TEXT_DARK = "#64748B"

    # Module Color Accents
    COLOR_SCANNER = "#00FF66"      # Module 2: Matrix Neon Green
    COLOR_THREAT_MAP = "#00D2FF"   # Module 3: Tech Neon Blue
    COLOR_AI_CYAN = "#06B6D4"      # Module 4: Cyber Cyan
    COLOR_AI_PURPLE = "#A855F7"    # Module 4: Cyber Purple
    COLOR_VULN_GOLD = "#FACC15"    # Module 5: Cyber Gold

    # Threat Severity Indicators
    SEVERITY_CRITICAL = "#FF0055"
    SEVERITY_HIGH = "#FF6600"
    SEVERITY_MEDIUM = "#FACC15"
    SEVERITY_LOW = "#00D2FF"
    SEVERITY_INFO = "#38BDF8"
    STATUS_SECURE = "#00FF66"


@dataclass
class MapNode:
    id: str
    name: str
    lat: float
    lon: float
    region: str
    is_hq: bool = False
    ip_range: str = "10.0.0.0/8"


# Global Threat Map Nodes (Focusing strongly on East Africa / Arusha Tanzania)
GLOBAL_NODES: Dict[str, MapNode] = {
    # EAST AFRICA REGION
    "ARUSHA": MapNode("ARUSHA", "Arusha HQ (Tanzania)", -3.3869, 36.6830, "EAST AFRICA", is_hq=True, ip_range="102.214.32.0/24"),
    "DAR": MapNode("DAR", "Dar es Salaam Node (Tanzania)", -6.7924, 39.2083, "EAST AFRICA", ip_range="197.250.0.0/16"),
    "NAIROBI": MapNode("NAIROBI", "Nairobi Gateway (Kenya)", -1.2921, 36.8219, "EAST AFRICA", ip_range="196.201.214.0/24"),
    "KIGALI": MapNode("KIGALI", "Kigali Cyber Hub (Rwanda)", -1.9441, 30.0619, "EAST AFRICA", ip_range="197.243.0.0/16"),
    "KAMPALA": MapNode("KAMPALA", "Kampala Datacenter (Uganda)", 0.3476, 32.5825, "EAST AFRICA", ip_range="196.43.128.0/20"),

    # REST OF AFRICA
    "JOHANNESBURG": MapNode("JOHANNESBURG", "Johannesburg Sentinel (South Africa)", -26.2041, 28.0473, "AFRICA", ip_range="196.25.1.0/24"),
    "LAGOS": MapNode("LAGOS", "Lagos Core Switch (Nigeria)", 6.5244, 3.3792, "AFRICA", ip_range="197.210.0.0/16"),
    "CAIRO": MapNode("CAIRO", "Cairo Regional NOC (Egypt)", 30.0444, 31.2357, "AFRICA", ip_range="156.192.0.0/16"),
    "CASABLANCA": MapNode("CASABLANCA", "Casablanca Node (Morocco)", 33.5731, -7.5898, "AFRICA", ip_range="196.200.128.0/18"),

    # EUROPE
    "FRANKFURT": MapNode("FRANKFURT", "Frankfurt IXP (Germany)", 50.1109, 8.6821, "EUROPE", ip_range="80.237.128.0/17"),
    "LONDON": MapNode("LONDON", "London Cyber Command (UK)", 51.5074, -0.1278, "EUROPE", ip_range="195.66.224.0/19"),
    "AMSTERDAM": MapNode("AMSTERDAM", "AMS-IX Hub (Netherlands)", 52.3676, 4.9041, "EUROPE", ip_range="194.109.0.0/16"),
    "STOCKHOLM": MapNode("STOCKHOLM", "Stockholm Defense Node (Sweden)", 59.3293, 18.0686, "EUROPE", ip_range="193.180.0.0/16"),

    # AMERICAS
    "NEW_YORK": MapNode("NEW_YORK", "New York Financial Grid (USA)", 40.7128, -74.0060, "AMERICAS", ip_range="198.51.100.0/24"),
    "SILICON_VALLEY": MapNode("SILICON_VALLEY", "Silicon Valley Cloud Core (USA)", 37.3875, -122.0575, "AMERICAS", ip_range="199.16.156.0/22"),
    "SAO_PAULO": MapNode("SAO_PAULO", "São Paulo Defense Node (Brazil)", -23.5505, -46.6333, "AMERICAS", ip_range="200.160.0.0/20"),
    "WASHINGTON": MapNode("WASHINGTON", "Washington Cyber Ops (USA)", 38.9072, -77.0369, "AMERICAS", ip_range="192.0.2.0/24"),

    # ASIA & PACIFIC
    "TOKYO": MapNode("TOKYO", "Tokyo Defense Core (Japan)", 35.6762, 139.6503, "ASIA_PACIFIC", ip_range="133.242.0.0/16"),
    "SINGAPORE": MapNode("SINGAPORE", "Singapore Straits Gateway", 1.3521, 103.8198, "ASIA_PACIFIC", ip_range="202.166.0.0/19"),
    "SYDNEY": MapNode("SYDNEY", "Sydney Defense Grid (Australia)", -33.8688, 151.2093, "ASIA_PACIFIC", ip_range="139.130.0.0/16"),
}

# Supported Regions for Map Filter
REGIONS = ["WORLD", "AFRICA", "EAST AFRICA", "EUROPE", "AMERICAS"]
