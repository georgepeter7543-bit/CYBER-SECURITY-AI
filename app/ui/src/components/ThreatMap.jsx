import React, { useState, useEffect, useRef } from 'react';
import { Globe2, Pause, Play, Trash2, ShieldAlert } from 'lucide-react';

const NODES = {
  ARUSHA: { name: "Arusha HQ (Tanzania)", lat: -3.3869, lon: 36.6830, region: "EAST AFRICA", isHq: true, ip: "102.214.32.0/24" },
  DAR: { name: "Dar es Salaam Node (Tanzania)", lat: -6.7924, lon: 39.2083, region: "EAST AFRICA", ip: "197.250.0.0/16" },
  NAIROBI: { name: "Nairobi Gateway (Kenya)", lat: -1.2921, lon: 36.8219, region: "EAST AFRICA", ip: "196.201.214.0/24" },
  KIGALI: { name: "Kigali Cyber Hub (Rwanda)", lat: -1.9441, lon: 30.0619, region: "EAST AFRICA", ip: "197.243.0.0/16" },
  JOHANNESBURG: { name: "Johannesburg Sentinel (South Africa)", lat: -26.2041, lon: 28.0473, region: "AFRICA", ip: "196.25.1.0/24" },
  LAGOS: { name: "Lagos Core Switch (Nigeria)", lat: 6.5244, lon: 3.3792, region: "AFRICA", ip: "197.210.0.0/16" },
  CAIRO: { name: "Cairo Regional NOC (Egypt)", lat: 30.0444, lon: 31.2357, region: "AFRICA", ip: "156.192.0.0/16" },
  LONDON: { name: "London Cyber Command (UK)", lat: 51.5074, lon: -0.1278, region: "EUROPE", ip: "195.66.224.0/19" },
  FRANKFURT: { name: "Frankfurt IXP (Germany)", lat: 50.1109, lon: 8.6821, region: "EUROPE", ip: "80.237.128.0/17" },
  NEW_YORK: { name: "New York Financial Grid (USA)", lat: 40.7128, lon: -74.0060, region: "AMERICAS", ip: "198.51.100.0/24" },
  SILICON_VALLEY: { name: "Silicon Valley Cloud Core (USA)", lat: 37.3875, lon: -122.0575, region: "AMERICAS", ip: "199.16.156.0/22" },
  TOKYO: { name: "Tokyo Defense Core (Japan)", lat: 35.6762, lon: 139.6503, region: "ASIA_PACIFIC", ip: "133.242.0.0/16" },
};

const REGIONS = ["WORLD", "AFRICA", "EAST AFRICA", "EUROPE", "AMERICAS"];

const REGION_BOUNDS = {
  WORLD: { minLat: -60, maxLat: 78, minLon: -160, maxLon: 170 },
  AFRICA: { minLat: -38, maxLat: 40, minLon: -22, maxLon: 55 },
  "EAST AFRICA": { minLat: -15, maxLat: 6, minLon: 26, maxLon: 45 },
  EUROPE: { minLat: 34, maxLat: 72, minLon: -15, maxLon: 40 },
  AMERICAS: { minLat: -58, maxLat: 72, minLon: -130, maxLon: -32 },
};

export default function ThreatMap() {
  const canvasRef = useRef(null);
  const [region, setRegion] = useState("WORLD");
  const [isPaused, setIsPaused] = useState(false);
  const [threatFeed, setThreatFeed] = useState([
    { time: "14:20:11", origin: "Frankfurt IXP", target: "Arusha HQ (Tanzania)", vector: "DDoS SYN-Flood Incursion", severity: "CRITICAL", action: "BLOCKED (Peter Core)" },
    { time: "14:20:08", origin: "Silicon Valley Cloud", target: "Nairobi Gateway", vector: "Zero-Day Kerberos Exploit", severity: "HIGH", action: "BLOCKED" },
    { time: "14:20:04", origin: "London Cyber Command", target: "Johannesburg Sentinel", vector: "Credential Stuffing Wave", severity: "MEDIUM", action: "RATE-LIMITED" },
    { time: "14:19:59", origin: "Tokyo Defense Core", target: "Arusha HQ (Tanzania)", vector: "Automated Port Sweep", severity: "LOW", action: "MONITORED" },
  ]);

  const arcsRef = useRef([]);

  // Coordinate projector
  const project = (lat, lon, width, height) => {
    const bounds = REGION_BOUNDS[region];
    const normX = (lon - bounds.minLon) / (bounds.maxLon - bounds.minLon);
    const normY = (bounds.maxLat - lat) / (bounds.maxLat - bounds.minLat);
    return {
      x: 30 + normX * (width - 60),
      y: 30 + normY * (height - 60)
    };
  };

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let animId;
    let radarAngle = 0;

    // Spawn random arcs
    const interval = setInterval(() => {
      if (isPaused) return;
      const keys = Object.keys(NODES);
      const originKey = keys[Math.floor(Math.random() * keys.length)];
      const targetKey = Math.random() < 0.6 ? "ARUSHA" : keys[Math.floor(Math.random() * keys.length)];
      if (originKey === targetKey) return;

      const threats = [
        { vector: "APT-41 C2 Exfiltration", sev: "CRITICAL", color: "#FF0055" },
        { vector: "Ransomware Lateral Move", sev: "HIGH", color: "#FF6600" },
        { vector: "SSH Brute-Force Wave", sev: "MEDIUM", color: "#FACC15" },
        { vector: "DNS Tunneling Exploit", sev: "HIGH", color: "#FF6600" },
      ];
      const threat = threats[Math.floor(Math.random() * threats.length)];

      arcsRef.current.push({
        origin: NODES[originKey],
        target: NODES[targetKey],
        progress: 0,
        speed: 0.015 + Math.random() * 0.01,
        color: threat.color,
        radius: 0,
        finished: false
      });

      // Update feed
      setThreatFeed(prev => [
        {
          time: new Date().toLocaleTimeString(),
          origin: NODES[originKey].name,
          target: NODES[targetKey].name,
          vector: threat.vector,
          severity: threat.sev,
          action: "BLOCKED (Peter Defense Core)"
        },
        ...prev.slice(0, 15)
      ]);
    }, 2200);

    const render = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      const width = canvas.width;
      const height = canvas.height;

      // 1. Tactical Grid
      ctx.strokeStyle = "rgba(24, 32, 48, 0.45)";
      ctx.lineWidth = 1;
      ctx.setLineDash([2, 4]);
      for (let x = 0; x < width; x += 45) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, height);
        ctx.stroke();
      }
      for (let y = 0; y < height; y += 45) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(width, y);
        ctx.stroke();
      }
      ctx.setLineDash([]);

      // 2. Animated Attack Arcs
      arcsRef.current.forEach(arc => {
        const p0 = project(arc.origin.lat, arc.origin.lon, width, height);
        const p2 = project(arc.target.lat, arc.target.lon, width, height);
        const midX = (p0.x + p2.x) / 2;
        const midY = (p0.y + p2.y) / 2;
        const dx = p2.x - p0.x;
        const dy = p2.y - p0.y;
        const dist = Math.hypot(dx, dy);
        const curvature = Math.min(dist * 0.35, 80);
        const ctrlX = midX - (dy / dist) * curvature;
        const ctrlY = midY + (dx / dist) * curvature;

        // Draw trajectory
        ctx.beginPath();
        ctx.moveTo(p0.x, p0.y);
        ctx.quadraticCurveTo(ctrlX, ctrlY, p2.x, p2.y);
        ctx.strokeStyle = arc.color + "33";
        ctx.lineWidth = 1.5;
        ctx.stroke();

        // Projectile Head
        const t = arc.progress;
        const invT = 1 - t;
        const hx = invT * invT * p0.x + 2 * invT * t * ctrlX + t * t * p2.x;
        const hy = invT * invT * p0.y + 2 * invT * t * ctrlY + t * t * p2.y;

        if (arc.progress < 1) {
          ctx.beginPath();
          ctx.arc(hx, hy, 4, 0, Math.PI * 2);
          ctx.fillStyle = arc.color;
          ctx.fill();

          ctx.beginPath();
          ctx.arc(hx, hy, 7, 0, Math.PI * 2);
          ctx.fillStyle = arc.color + "55";
          ctx.fill();

          arc.progress += arc.speed;
        } else {
          // Impact ripple
          arc.radius += 1.2;
          ctx.beginPath();
          ctx.arc(p2.x, p2.y, arc.radius, 0, Math.PI * 2);
          ctx.strokeStyle = arc.color + Math.floor(Math.max(0, 255 * (1 - arc.radius / 30))).toString(16).padStart(2, '0');
          ctx.lineWidth = 2;
          ctx.stroke();

          if (arc.radius > 30) arc.finished = true;
        }
      });
      arcsRef.current = arcsRef.current.filter(a => !a.finished);

      // 3. Draw Nodes
      Object.values(NODES).forEach(node => {
        const pt = project(node.lat, node.lon, width, height);
        if (pt.x < 0 || pt.x > width || pt.y < 0 || pt.y > height) return;

        if (node.isHq) {
          // Arusha HQ Glowing Rings
          ctx.beginPath();
          ctx.arc(pt.x, pt.y, 10, 0, Math.PI * 2);
          ctx.strokeStyle = "#00FF66";
          ctx.lineWidth = 1.5;
          ctx.stroke();

          ctx.beginPath();
          ctx.arc(pt.x, pt.y, 5, 0, Math.PI * 2);
          ctx.fillStyle = "#00FF66";
          ctx.fill();

          ctx.fillStyle = "#00FF66";
          ctx.font = "bold 11px Inter, sans-serif";
          ctx.fillText("★ ARUSHA HQ [TANZANIA]", pt.x + 12, pt.y + 4);
        } else {
          ctx.beginPath();
          ctx.arc(pt.x, pt.y, 4, 0, Math.PI * 2);
          ctx.fillStyle = node.region === "EAST AFRICA" ? "#38BDF8" : "#00D2FF";
          ctx.fill();

          ctx.fillStyle = "#94A3B8";
          ctx.font = "10px Inter, sans-serif";
          ctx.fillText(node.name.split(" ")[0], pt.x + 8, pt.y + 3);
        }
      });

      // 4. Rotating Radar HUD
      const rcx = width - 60;
      const rcy = height - 60;
      const rrad = 40;
      radarAngle += 0.03;

      ctx.beginPath();
      ctx.arc(rcx, rcy, rrad, 0, Math.PI * 2);
      ctx.strokeStyle = "#00D2FF55";
      ctx.stroke();

      ctx.beginPath();
      ctx.moveTo(rcx, rcy);
      ctx.lineTo(rcx + rrad * Math.cos(radarAngle), rcy + rrad * Math.sin(radarAngle));
      ctx.strokeStyle = "#00D2FF";
      ctx.lineWidth = 2;
      ctx.stroke();

      animId = requestAnimationFrame(render);
    };

    render();
    return () => {
      cancelAnimationFrame(animId);
      clearInterval(interval);
    };
  }, [region, isPaused]);

  return (
    <div className="p-8 flex flex-col gap-6 max-w-7xl mx-auto h-full overflow-y-auto">
      {/* Header & Filter Controls */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#1E2330] pb-4">
        <div>
          <h2 className="text-2xl font-bold text-[#00D2FF] tracking-wide font-sans flex items-center gap-2">
            <Globe2 className="w-6 h-6 text-[#00D2FF]" />
            GLOBAL THREAT INTELLIGENCE & ATTACK MAP
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Real-time orbital attack trajectories, telemetry mesh, and East Africa defense node monitoring.
          </p>
        </div>

        {/* Region Filter Buttons */}
        <div className="flex items-center gap-1.5 bg-[#12141A] p-1.5 rounded-lg border border-[#1E2330]">
          <span className="text-[11px] font-bold text-slate-400 px-2 uppercase">SECTOR:</span>
          {REGIONS.map(reg => (
            <button
              key={reg}
              onClick={() => setRegion(reg)}
              className={`px-3 py-1 text-xs font-semibold rounded transition ${
                region === reg
                  ? "bg-[#00D2FF]/20 text-[#00D2FF] border border-[#00D2FF]/50"
                  : "text-slate-400 hover:text-white"
              }`}
            >
              {reg}
            </button>
          ))}
        </div>
      </div>

      {/* 2D Vector Canvas */}
      <div className="relative bg-[#0A0A0C] border border-[#1E2330] rounded-xl overflow-hidden shadow-2xl h-[420px]">
        <canvas
          ref={canvasRef}
          width={1000}
          height={420}
          className="w-full h-full block"
        />
        <div className="absolute top-4 left-4 font-mono text-[11px] text-[#00D2FF] bg-[#12141A]/80 px-2.5 py-1 rounded border border-[#1E2330]">
          SECTOR: {region} // MERCATOR PROJECTION 2D
        </div>
      </div>

      {/* Live Streaming Threat Feed Table */}
      <div className="border border-[#1E2330] rounded-xl overflow-hidden bg-[#101217]">
        <div className="flex items-center justify-between px-5 py-3 bg-[#161922] border-b border-[#1E2330]">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
            <span className="text-xs font-bold text-[#00D2FF] uppercase tracking-wider">
              Live Incoming Threat Feed (Global Sensors)
            </span>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setIsPaused(!isPaused)}
              className="flex items-center gap-1 text-xs px-2.5 py-1 bg-[#12141A] border border-[#2B3142] rounded text-slate-300 hover:text-white"
            >
              {isPaused ? <Play className="w-3 h-3" /> : <Pause className="w-3 h-3" />}
              <span>{isPaused ? "Resume" : "Pause"}</span>
            </button>
            <button
              onClick={() => setThreatFeed([])}
              className="flex items-center gap-1 text-xs px-2.5 py-1 bg-[#12141A] border border-[#2B3142] rounded text-slate-300 hover:text-white"
            >
              <Trash2 className="w-3 h-3" />
              <span>Clear</span>
            </button>
          </div>
        </div>

        <div className="max-h-60 overflow-y-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-[#12141A] text-slate-400 uppercase font-semibold border-b border-[#1E2330] sticky top-0">
              <tr>
                <th className="py-2.5 px-4">Time</th>
                <th className="py-2.5 px-4">Origin Node</th>
                <th className="py-2.5 px-4">Target Node</th>
                <th className="py-2.5 px-4">Attack Vector</th>
                <th className="py-2.5 px-4">Severity</th>
                <th className="py-2.5 px-4">Defense Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#1A1F2B]">
              {threatFeed.map((item, i) => (
                <tr key={i} className="hover:bg-[#161922]/50 transition">
                  <td className="py-2.5 px-4 font-mono text-slate-400">{item.time}</td>
                  <td className="py-2.5 px-4 font-medium text-slate-200">{item.origin}</td>
                  <td className={`py-2.5 px-4 font-medium ${item.target.includes("Arusha") ? "text-[#00FF66] font-bold" : "text-slate-200"}`}>
                    {item.target}
                  </td>
                  <td className="py-2.5 px-4 font-mono text-slate-300">{item.vector}</td>
                  <td className="py-2.5 px-4 font-bold">
                    <span className={
                      item.severity === "CRITICAL" ? "text-rose-400" :
                      item.severity === "HIGH" ? "text-amber-500" :
                      item.severity === "MEDIUM" ? "text-amber-400" : "text-cyan-400"
                    }>
                      {item.severity}
                    </span>
                  </td>
                  <td className="py-2.5 px-4 text-emerald-400 font-semibold">{item.action}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
