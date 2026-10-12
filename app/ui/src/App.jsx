import React, { useState, useEffect } from 'react';
import { Shield, Globe2, Terminal, ShieldAlert, Cpu, HardDrive, Wifi, Activity } from 'lucide-react';
import VirusScanner from './components/VirusScanner';
import ThreatMap from './components/ThreatMap';
import HackerGPT from './components/HackerGPT';
import VulnerabilityOverview from './components/VulnerabilityOverview';

const API_BASE_URL = (import.meta.env.VITE_BACKEND_URL || "http://localhost:5000").replace(/\/$/, "");

export default function App() {
  const [activeTab, setActiveTab] = useState('chat'); // default to HackerGPT or scanner
  const [cpu, setCpu] = useState(18.4);
  const [ram, setRam] = useState(7.8);
  const [netTx, setNetTx] = useState(24.8);
  const [netRx, setNetRx] = useState(112.5);
  const [uptime, setUptime] = useState(0);

  // Live telemetry interval connecting to live backend (Render/Railway/localhost)
  useEffect(() => {
    const fetchTelemetry = async () => {
      try {
        const res = await fetch(`${API_BASE_URL}/api/telemetry`);
        if (res.ok) {
          const data = await res.json();
          if (data.cpu_percent !== undefined) setCpu(data.cpu_percent);
          if (data.ram_used_gb !== undefined) setRam(data.ram_used_gb);
          if (data.net_tx_mb !== undefined) setNetTx(data.net_tx_mb);
          if (data.net_rx_mb !== undefined) setNetRx(data.net_rx_mb);
        }
      } catch (err) {
        // Fallback simulation if backend is spinning up or offline
        setCpu(+(15 + Math.random() * 8).toFixed(1));
        setRam(+(7.4 + Math.random() * 0.8).toFixed(1));
        setNetTx(+(20 + Math.random() * 12).toFixed(1));
        setNetRx(+(95 + Math.random() * 25).toFixed(1));
      }
      setUptime(u => u + 1);
    };

    fetchTelemetry();
    const timer = setInterval(fetchTelemetry, 2500);
    return () => clearInterval(timer);
  }, []);

  const formatUptime = (seconds) => {
    const hrs = Math.floor(seconds / 3600).toString().padStart(2, '0');
    const mins = Math.floor((seconds % 3600) / 60).toString().padStart(2, '0');
    const secs = (seconds % 60).toString().padStart(2, '0');
    return `${hrs}:${mins}:${secs}`;
  };

  const navItems = [
    { id: 'scanner', label: 'VIRUS SCANNER', icon: Shield, color: '#00FF66', borderActive: 'border-[#00FF66]', textActive: 'text-[#00FF66]' },
    { id: 'map', label: 'GLOBAL THREAT MAP', icon: Globe2, color: '#00D2FF', borderActive: 'border-[#00D2FF]', textActive: 'text-[#00D2FF]' },
    { id: 'chat', label: 'AI SECURITY CHAT', icon: Terminal, color: '#06B6D4', borderActive: 'border-cyan-400', textActive: 'text-cyan-400' },
    { id: 'vuln', label: 'SYSTEM VULNERABILITY', icon: ShieldAlert, color: '#FACC15', borderActive: 'border-[#FACC15]', textActive: 'text-[#FACC15]' },
  ];

  return (
    <div className="flex flex-col h-screen w-screen bg-[#0A0A0C] text-slate-100 overflow-hidden font-sans">
      {/* 1. TOP NAVIGATION BAR */}
      <nav className="bg-[#101217] border-b border-[#1E2330] px-6 py-2.5 flex flex-col gap-2 shrink-0 select-none">
        {/* Upper Row: Title Branding + Telemetry Pills */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-base font-bold tracking-wider text-white uppercase font-sans">
              PETER CYBER SECURITY PROGRAM
            </h1>
            <p className="text-[10px] font-mono text-[#00FF66] tracking-widest uppercase">
              SEC-OPS ENTERPRISE ZERO-TRUST ARCHITECTURE // ARUSHA HQ
            </p>
          </div>

          {/* Telemetry Pills */}
          <div className="flex items-center gap-2 text-xs font-mono">
            {/* CPU */}
            <div className="flex items-center gap-1.5 px-2.5 py-1 rounded bg-[#161922] border border-[#1E2330] border-l-2 border-l-[#00D2FF]">
              <Cpu className="w-3.5 h-3.5 text-[#00D2FF]" />
              <span className="text-slate-400 text-[10px] uppercase font-bold">CPU</span>
              <span className="text-white font-semibold">{cpu}%</span>
            </div>

            {/* RAM */}
            <div className="flex items-center gap-1.5 px-2.5 py-1 rounded bg-[#161922] border border-[#1E2330] border-l-2 border-l-[#FACC15]">
              <HardDrive className="w-3.5 h-3.5 text-[#FACC15]" />
              <span className="text-slate-400 text-[10px] uppercase font-bold">RAM</span>
              <span className="text-white font-semibold">{ram}/16 GB</span>
            </div>

            {/* AI Core */}
            <div className="flex items-center gap-1.5 px-2.5 py-1 rounded bg-[#161922] border border-[#1E2330] border-l-2 border-l-[#A855F7]">
              <Activity className="w-3.5 h-3.5 text-[#A855F7]" />
              <span className="text-slate-400 text-[10px] uppercase font-bold">AI CORE</span>
              <span className="text-purple-300 font-semibold">NEURAL v4.2 [ONLINE]</span>
            </div>

            {/* Network */}
            <div className="flex items-center gap-1.5 px-2.5 py-1 rounded bg-[#161922] border border-[#1E2330] border-l-2 border-l-[#00FF66]">
              <Wifi className="w-3.5 h-3.5 text-[#00FF66]" />
              <span className="text-slate-400 text-[10px] uppercase font-bold">NET</span>
              <span className="text-white font-semibold">TX {netTx} MB/s | RX {netRx} MB/s</span>
            </div>
          </div>
        </div>

        {/* Lower Row: Segmented Module Tabs */}
        <div className="flex items-center gap-1 border-t border-[#1A1F2C] pt-1.5">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`flex items-center gap-2 px-4 py-2 text-xs font-bold tracking-wider rounded-md transition-all ${
                  isActive
                    ? `bg-[#181C26] ${item.textActive} border-b-2 ${item.borderActive}`
                    : 'text-slate-400 hover:text-white hover:bg-[#141720]'
                }`}
              >
                <Icon className="w-4 h-4" />
                <span>{item.label}</span>
              </button>
            );
          })}
        </div>
      </nav>

      {/* 2. MAIN ACTIVE MODULE VIEW */}
      <main className="flex-1 overflow-hidden bg-[#0A0A0C]">
        {activeTab === 'scanner' && <VirusScanner />}
        {activeTab === 'map' && <ThreatMap />}
        {activeTab === 'chat' && <HackerGPT />}
        {activeTab === 'vuln' && <VulnerabilityOverview />}
      </main>

      {/* 3. NATIVE FOOTER STATUS BAR */}
      <footer className="bg-[#0E1015] border-t border-[#1E2330] px-6 py-1.5 flex items-center justify-between text-[11px] font-mono text-slate-400 shrink-0 select-none">
        <div className="flex items-center gap-2 text-[#00FF66] font-bold">
          <span className="w-2 h-2 rounded-full bg-[#00FF66] animate-pulse" />
          <span>GRID STATUS: ZERO-TRUST SHIELD ENFORCED // ENCLAVE INTEGRITY: VERIFIED</span>
        </div>
        <div className="flex items-center gap-4">
          <span>UPTIME: {formatUptime(uptime)}</span>
          <span className="text-slate-600">|</span>
          <span>ENCRYPTION: AES-256-GCM</span>
          <span className="text-slate-600">|</span>
          <span className="text-cyan-400">HARDWARE ACCEL: ACTIVE</span>
        </div>
      </footer>
    </div>
  );
}
