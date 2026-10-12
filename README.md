# PETER CYBER SECURITY PROGRAM
### Enterprise Native Desktop Architecture & Cybersecurity Suite

> **Architectural Standard**: 100% Native C++/Qt Desktop Engine via PyQt6.  
> **Strict Compliance**: Zero HTML, Zero CSS, Zero JavaScript, Zero WebViews.  
> **Aesthetic Standard**: Obsidian Stealth Theme (`#0A0A0C`), Hardware-Accelerated Vector QPainter.

---

## 🛡️ Executive System Overview

The **PETER CYBER SECURITY PROGRAM** is a native desktop application engineered for enterprise security operations centers (SOC), incident response teams, and zero-trust threat monitoring. Built with Python and PyQt6, the application achieves high-performance vector rendering, multithreaded non-blocking telemetry, and dark-mode controls.

---

## 📐 Modular Architecture

```
PETER CYBER SECURITY PROGRAM/
├── run.py                          # Primary application launcher
├── requirements.txt                # Native dependencies (PyQt6, psutil)
├── app/
│   ├── __init__.py                 # Version metadata
│   ├── main.py                     # High-DPI setup, dark QPalette, event loop
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py               # Theme colors, global nodes (Arusha HQ), constants
│   │   ├── system_monitor.py       # Non-blocking QThread hardware & network telemetry
│   │   └── security_engine.py      # Multi-engine scanner, MD5/SHA-256 & entropy calculator
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── main_window.py          # Top Navigation Bar, live telemetry pills, QStackedWidget
│   │   ├── style.py                # Pure Native Qt widget stylesheet (QSS)
│   │   ├── widgets/
│   │   │   ├── __init__.py
│   │   │   ├── drag_drop_zone.py   # Native QPainter Drag-and-Drop file analyzer
│   │   │   ├── threat_canvas.py    # Hardware-accelerated 2D vector canvas with Bezier arcs
│   │   │   ├── chat_bubble.py      # Native chat console widget with code box rendering
│   │   │   └── stat_card.py        # Executive cyber metric cards
│   │   └── modules/
│   │       ├── __init__.py
│   │       ├── virus_scanner.py    # Module 2: Virus Scanner (#00FF66)
│   │       ├── threat_map.py       # Module 3: Global Threat Map & Feed (#00D2FF)
│   │       ├── ai_assistant.py     # Module 4: AI Security Chat Assistant (#06B6D4 / #A855F7)
│   │       └── vulnerability_view.py # Module 5: System Vulnerability Overview (#FACC15)
└── tests/
    ├── __init__.py
    └── test_components.py          # Automated component and GUI unit tests
```

---

## 🎨 Modular Interface & Color Themes

### 1. Top Navigation Bar (Obsidian Base: `#0A0A0C` / `#101217`)
- **Branding**: "PETER CYBER SECURITY PROGRAM" with enterprise build badge.
- **Real-Time Telemetry Strip**:
  - `CPU`: Real-time core utilization percentage via `psutil` in dedicated thread.
  - `RAM`: Physical RAM utilization in GB and percentage.
  - `AI CORE`: `NEURAL-DEFENSE v4.2 [ONLINE]` status pill.
  - `NETWORK`: Real-time dynamic `TX / RX` throughput rate.
- **Segmented Tab Switcher**: Switches between modules with animated indicator underlines.

---

### 2. Virus Scanner Module (Accent: Matrix Neon Green `#00FF66`)
- **Native File Drag-and-Drop Widget**:
  - Drag-and-drop support with hover animations, high-tech corner brackets, and vector shield icon.
  - Automatic cryptographic metadata generation upon drop: **MD5**, **SHA-256**, **Shannon Entropy** calculation, and exact byte size.
- **Real-Time Progress Engine**:
  - Multi-stage scan progression bar:
    1. Cryptographic Hash Validation
    2. Bytecode & PE Header Decompilation
    3. YARA Dynamic Rule Pattern Matching (240,000+ signatures)
    4. Ring-0 Kernel Sandbox Behavioral Emulation
    5. Deep Neural Threat Scoring
- **Multi-Engine Result Table**:
  - Columns: `SECURITY ENGINE`, `ENGINE TYPE`, `DETECTION STATUS`, `THREAT VECTOR`, `RISK SCORE`, `RECOMMENDED ACTION`.
  - Engines: *PETER Neural Core v4.2*, *CrowdStrike Falcon Heuristic*, *ClamAV Signature Engine*, *YARA Dynamic Ruleset*, *Kernel Sandboxing Sandbox-01*, *Entropy & Packing Inspector*.
- **Actions**:
  - `▶ EXECUTE DEEP HEURISTIC SCAN`
  - `⏹ ABORT`
  - `🛡️ QUARANTINE THREAT` (Neutralizes permissions to `0000` into Peter Vault)
  - `📄 EXPORT FORENSIC REPORT` (Generates structured JSON report)

---

### 3. Global Threat Map Module (Accent: Tech Neon Blue `#00D2FF`)
- **2D Custom Vector Canvas**:
  - Hardware-accelerated with native `QPainter` antialiasing and double-buffering.
  - Mercator projection of continental vector polygons, tactical longitude/latitude grid, and HUD radar sweep.
  - **East Africa & Arusha Node Prominence**:
    - Highlights **Arusha HQ (Tanzania)** at `[-3.3869, 36.6830]` with pulsing golden/green defense rings, beacon tag, and tactical telemetry.
    - Regional nodes: Dar es Salaam, Nairobi, Kigali, Kampala, Johannesburg, Lagos, Cairo, London, Frankfurt, New York, Silicon Valley, Tokyo, Singapore, Sydney.
  - **Animated Bezier Attack Arcs**:
    - Quadratic Bezier curves connecting source and target nodes.
    - Glowing photon particles traveling along trajectories with trailing alpha falloff.
    - Expanding concentric impact rings at target upon hit.
- **Region Filter Controls**:
  - Instant zoom and camera focus: `WORLD`, `AFRICA`, `EAST AFRICA` (Arusha/Tanzania close-up), `EUROPE`, `AMERICAS`.
- **Live Streaming Threat Feed Table**:
  - Real-time event log with `TIMESTAMP`, `ORIGIN NODE`, `TARGET NODE`, `THREAT VECTOR`, `SEVERITY` (Critical `#FF0055`, High `#FF6600`, Medium `#FACC15`, Low `#00D2FF`), and `DEFENSE ACTION`.
  - Pause/Resume streaming toggle and clear feed buttons.

---

### 4. HackerGPT Recon & AI Assistant Module (Custom Cyberpunk Console)
- **Exact HackerGPT Visual Fidelity**:
  - **Top Bar**: Hamburger drawer toggle `☰`, centered `HackerGPT` branding, and `+ chat` button to spawn fresh recon sessions.
  - **Reconnaissance Snapshot Grid**:
    - Generates target recon summaries (`<target> - Quick Recon Snapshot`).
    - Dotted table layout (`Item` | `Details`): `IP Address`, `WHOIS`, and expandable `HTTP Fingerprint`.
    - Collapsible disclosure: Click **"▶ Click to expand"** to reveal/hide full JSON fingerprints.
  - **Monospace Code Container**:
    - Dark navy/charcoal background (`#171A23`) with header displaying `text` or `json` on the left and a functional `📄 Copy` button on the right.
  - **Custom-Painted Cyberpunk Input Box**:
    - Hardware-accelerated `QPainter` drawing a chamfered polygon with stepped notch cutout and dashed accents (`- - - - -`).
    - Multi-line text editor with placeholder `Message HackerGPT`.
    - `📁 Upload` button to attach security artifacts, PCAP captures, and binaries.
    - Cyber arrow send button (`▶`) with keyboard shortcuts (`Enter` to submit, `Shift+Enter` for newline).
  - **Session History Drawer**:
    - Toggleable via `☰` menu to quickly switch between recon targets (`cybergym.hackergpt.app`, `arusha-core.tz`, `port-audit-192.168.1.1`, etc.).

---

### 5. System Vulnerability Overview (Accent: Cyber Gold `#FACC15`)
- **Executive Metrics Grid**:
  - `Active CVE Disclosures`: Immediate count of critical and high vulnerabilities.
  - `Security Posture Score`: Numerical evaluation (e.g., `94.8 / 100`).
  - `Zero-Trust Compliance`: Continuous percentage evaluation across all network interfaces.
  - `Monitored Daemons`: Status of active system services.
- **Native Filesystem Tree Explorer**:
  - High-tech tree browser navigating critical files: Kernel images (`/boot/vmlinuz`), hosts configurations (`/etc/hosts`), PAM authentication policies (`/etc/pam.d`), dev endpoints, and root certificates.
- **Vulnerability Inspector & Remediation Panel**:
  - Displays selected node details, CVSS status badge, and remediation directives.
  - Interactive **"⚡ APPLY HARDENING PATCH"** button that remediates permissions, updates posture score, and resolves alerts.

---

## 🚀 Unified Full-Stack Architecture & Execution

The application can be run as a **unified full-stack web service** (where Python Flask serves the compiled React SPA directly on a single port with relative `/api/...` endpoints) or as a **native PyQt6 desktop application**.

### 1. Install Dependencies
```bash
# Python backend dependencies
pip install -r requirements.txt

# React frontend dependencies
cd app/ui
npm install
cd ../..
```

### 2. Single-Command Build & Run (Unified Full-Stack)
Compile the React frontend into `app/ui/dist/` and launch the unified Python server with one command:

**Cross-Platform (Python):**
```bash
python build_and_run.py
```

**PowerShell:**
```powershell
.\build_and_run.ps1
```

**Terminal Manual Command:**
```bash
cd app/ui && npm run build && cd ../.. && python app/main.py
```

Open **`http://localhost:5000`** in your browser. All API endpoints (`/api/telemetry`, `/api/scan`, `/api/recon`, `/api/threats`, `/api/vulnerabilities`) and non-API web routes are served seamlessly from the same origin.

---

### 3. Native Desktop Mode
To launch the native hardware-accelerated PyQt6 desktop application window:
```bash
python app/main.py --desktop
# or
python run.py
```

---

### 4. Run Automated Tests
```bash
python -m unittest tests/test_components.py
```

---

## 🔒 Security Architecture Highlights
- **Thread Isolation**: The UI main loop is isolated from telemetry collection and heuristic scanning tasks using dedicated `QThread` workers.
- **Native Memory Safety**: No Chromium / Electron / WebView overhead or cross-site scripting attack surface.
- **Cryptographic Enclaves**: All cryptographic hash routines use Python standard library `hashlib` with streaming 64 KB chunk buffers to prevent high memory consumption during large binary inspections.
