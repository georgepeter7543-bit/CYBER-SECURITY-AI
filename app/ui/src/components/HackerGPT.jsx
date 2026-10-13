import React, { useState, useEffect, useRef } from 'react';
import { Menu, Plus, Copy, Check, Upload, ArrowRight, ChevronRight, ChevronDown, Shield } from 'lucide-react';
import { API_BASE_URL } from '../config';

const defaultReconJson = {
  "target": "http://cybergym.hackergpt.app",
  "http_status": 200,
  "request_config": {
    "headers": {
      "User-Agent": "Opera/9.80 (Windows NT 6.1; U; fi) Presto/2.7.62 Version/11.00"
    }
  },
  "plugins": {
    "Country": { "string": ["UNITED STATES"], "module": ["US"] },
    "HTML5": {},
    "IP": { "string": ["34.231.169.117"] },
    "JQuery": { "version": ["2.2.4"] },
    "Script": { "string": ["module"] },
    "Title": { "string": ["CyberGym"] },
    "UncommonHeaders": { "string": ["access-control-allow-origin,x-content-type-options,feature-policy,x-re..."] }
  }
};

// ─── Initial welcome greeting (mirrors backend INITIAL_GREETING) ───────────
const INITIAL_GREETING = "Hey! How can I assist you with your cybersecurity or computer safety today?";

// ─── AssistantMessage: renders AI text responses (greetings, security advice,
//     out-of-scope notices) with a styled badge header ──────────────────────
function AssistantMessage({ text, badge = "PETER CYBER DEFENSE AI", timestamp }) {
  const lines = text.split('\n');
  return (
    <div className="flex flex-col gap-2 max-w-4xl bg-[#0E1118] border border-[#1E2330] border-l-2 border-l-cyan-500 rounded-lg p-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <span className="flex items-center gap-1.5 text-xs font-bold text-cyan-400 tracking-wide">
          <Shield className="w-3.5 h-3.5" />
          {badge}
        </span>
        <span className="text-[10px] font-mono text-slate-600">{timestamp}</span>
      </div>
      {/* Body */}
      <div className="text-sm text-slate-200 leading-relaxed space-y-1">
        {lines.map((line, i) => (
          <p key={i} className={line.trim() === '' ? 'h-2' : ''}>{line}</p>
        ))}
      </div>
    </div>
  );
}

// ─── ReconCard: renders domain reconnaissance snapshots ──────────────────────
function ReconCard({ msg, expanded, onToggleExpand, copied, onCopy }) {
  return (
    <div className="flex flex-col gap-4 max-w-4xl">
      {/* Recon Title */}
      <h2 className="text-base font-bold text-white tracking-wide">
        {msg.target} — Quick Recon Snapshot
      </h2>

      {/* Dotted Recon Table */}
      <div className="border border-dashed border-[#3D4454] rounded-sm text-sm">
        {/* Header */}
        <div className="flex px-4 py-2.5 font-bold text-white bg-transparent border-b border-dashed border-[#3D4454]">
          <div className="w-44 shrink-0">Item</div>
          <div className="text-slate-500 px-3">|</div>
          <div className="flex-1">Details</div>
        </div>

        {/* IP Row */}
        <div className="flex px-4 py-2.5 text-slate-200 border-b border-dashed border-[#3D4454]">
          <div className="w-44 shrink-0 font-semibold">IP Address</div>
          <div className="text-slate-500 px-3">|</div>
          <div className="flex-1 font-mono">{msg.ip}</div>
        </div>

        {/* WHOIS Row */}
        <div className="flex px-4 py-2.5 text-slate-200 border-b border-dashed border-[#3D4454]">
          <div className="w-44 shrink-0 font-semibold">WHOIS</div>
          <div className="text-slate-500 px-3">|</div>
          <div className="flex-1 text-slate-300">{msg.whois}</div>
        </div>

        {/* HTTP Fingerprint Row */}
        <div className="flex px-4 py-2.5 text-slate-200">
          <div className="w-44 shrink-0 font-semibold">HTTP Fingerprint</div>
          <div className="text-slate-500 px-3">|</div>
          <button
            onClick={onToggleExpand}
            className="flex items-center gap-1 text-slate-400 hover:text-white transition text-xs"
          >
            {expanded
              ? <ChevronDown className="w-3.5 h-3.5" />
              : <ChevronRight className="w-3.5 h-3.5" />
            }
            <span>{expanded ? 'Click to collapse' : 'Click to expand'}</span>
          </button>
        </div>
      </div>

      {/* JSON Code Box */}
      {expanded && (
        <div className="bg-[#171A23] border border-[#282E3D] rounded-lg overflow-hidden">
          {/* Code Header */}
          <div className="flex items-center justify-between px-4 py-2 border-b border-[#282E3D]/50 text-xs">
            <span className="text-slate-400 font-sans">text</span>
            <button
              onClick={onCopy}
              className="flex items-center gap-1 text-slate-400 hover:text-white transition"
            >
              {copied ? (
                <>
                  <Check className="w-3.5 h-3.5 text-emerald-400" />
                  <span className="text-emerald-400 font-semibold">Copied</span>
                </>
              ) : (
                <>
                  <Copy className="w-3.5 h-3.5" />
                  <span>Copy</span>
                </>
              )}
            </button>
          </div>
          {/* Code Body */}
          <pre className="p-4 text-xs font-mono text-slate-200 overflow-x-auto leading-relaxed">
            {JSON.stringify(msg.jsonData, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}

// ─── Main HackerGPT Component ─────────────────────────────────────────────────
export default function HackerGPT() {
  const [copied, setCopied] = useState(false);
  const [expanded, setExpanded] = useState(true);
  const [inputVal, setInputVal] = useState('');
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const bottomRef = useRef(null);

  // ── Initial state: clean greeting + first recon demo ──────────────────────
  const [messages, setMessages] = useState([
    {
      type: 'assistant',
      text: INITIAL_GREETING,
      badge: 'PETER CYBER DEFENSE AI',
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })
    },
    {
      type: 'user',
      text: 'Check cybergym.hackergpt.app/'
    },
    {
      type: 'recon',
      target: 'cybergym.hackergpt.app',
      ip: '34.231.169.117',
      whois: 'No publicly-available WHOIS record was returned for the sub-domain.',
      jsonData: defaultReconJson
    }
  ]);

  // Auto-scroll to latest message
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleCopy = (data) => {
    navigator.clipboard.writeText(JSON.stringify(data, null, 2));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const getTimestamp = () =>
    new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });

  // ── Send handler: POST to /api/chat (unified chatbot engine) ──────────────
  const handleSend = async () => {
    if (!inputVal.trim() || isLoading) return;
    const query = inputVal.trim();
    setInputVal('');

    const userMsg = { type: 'user', text: query };
    const updatedMessages = [...messages, userMsg];
    setMessages(updatedMessages);
    setIsLoading(true);

    try {
      const res = await fetch(`${API_BASE_URL}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: query })
      });

      if (res.ok) {
        const data = await res.json();
        const scope = data.scope || 'SECURITY';

        if (scope === 'RECON') {
          // Domain reconnaissance response
          setMessages([...updatedMessages, {
            type: 'recon',
            target: data.target || query,
            ip: data.ip || '198.51.100.82',
            whois: data.whois || 'ARIN Registry - Cloudflare / Fastly Edge Proxy.',
            jsonData: data.fingerprint || defaultReconJson
          }]);
        } else if (scope === 'OUT_OF_SCOPE') {
          // Scope restriction notice
          setMessages([...updatedMessages, {
            type: 'assistant',
            text: data.reply || data.message || 'I am dedicated specifically to cybersecurity and computer safety topics.',
            badge: 'SCOPE POLICY ENFORCED',
            timestamp: getTimestamp()
          }]);
        } else {
          // Greeting or security advisory text
          const badge = scope === 'GREETING'
            ? 'PETER CYBER DEFENSE AI'
            : `CYBER DEFENSE // ${data.target || 'ADVISORY'}`;

          setMessages([...updatedMessages, {
            type: 'assistant',
            text: data.reply || data.message || 'Security advisory generated.',
            badge,
            timestamp: getTimestamp()
          }]);
        }
        setIsLoading(false);
        return;
      }
    } catch (err) {
      console.warn(`[HackerGPT] Backend at ${API_BASE_URL} unreachable, using local heuristic fallback.`, err);
    }

    // ── Offline / fallback simulation ─────────────────────────────────────────
    const targetClean = query.replace(/^(check|scan|inspect|recon)\s+/i, '').replace(/\/$/, '').trim();
    const isArusha = /arusha|tz|tanzania/i.test(query);
    const isDomainQuery = /^(check|scan|inspect|recon)\s+/i.test(query) ||
      /https?:\/\//.test(query) ||
      /\b[a-z0-9-]+\.(app|com|org|net|tz|io|gov|edu|co|ai)\b/i.test(query);

    const isOutOfScope = !isDomainQuery && /\b(cook|recipe|bake|pasta|pizza|cake|sport|football|soccer|nba|movie|actor|celebrity|music|song|dating|horoscope|gardening)\b/i.test(query);

    if (isOutOfScope) {
      setMessages([...updatedMessages, {
        type: 'assistant',
        text: 'I am dedicated specifically to cybersecurity and computer safety topics. I am unable to assist with that request, but I would be glad to help you with threat analysis, computer troubleshooting, safety precautions, hardware security, or network hardening.\n\nHow can I help protect your computer or network today?',
        badge: 'SCOPE POLICY ENFORCED',
        timestamp: getTimestamp()
      }]);
    } else if (isDomainQuery) {
      setMessages([...updatedMessages, {
        type: 'recon',
        target: targetClean || 'target.cybersec.local',
        ip: isArusha ? '102.214.32.14' : '198.51.100.82',
        whois: isArusha
          ? 'Tanzania Network Information Centre (tzNIC) - Peter Defense Grid Arusha.'
          : 'ARIN Registry - Cloudflare / Fastly Edge Proxy.',
        jsonData: {
          target: `http://${targetClean || 'target.cybersec.local'}`,
          http_status: 200,
          request_config: { headers: { "User-Agent": "HackerGPT/4.2 (Zero-Trust Recon Engine; x64)" } },
          plugins: {
            Country: { string: [isArusha ? "TANZANIA" : "UNITED STATES"], module: [isArusha ? "TZ" : "US"] },
            HTML5: {},
            IP: { string: [isArusha ? "102.214.32.14" : "198.51.100.82"] },
            WAF: { string: ["Cloudflare / Peter Shield Active"] },
            SecurityHeaders: { string: ["Strict-Transport-Security, X-Frame-Options: DENY"] },
            OpenPorts: { string: ["80/TCP, 443/TCP (TLS 1.3)"] },
            VulnerabilityWeight: "0.0 - SECURE"
          }
        }
      }]);
    } else {
      // Generic security advisory fallback
      setMessages([...updatedMessages, {
        type: 'assistant',
        text: 'Apply zero-trust principles: always verify identity and file integrity before granting access, keep all software patched against known CVE vulnerabilities, and operate under the Principle of Least Privilege to minimize breach impact.\n\nUse "Check <url>" to run a live reconnaissance snapshot, or ask about threats, password safety, firewalls, or hardware security.',
        badge: 'CYBER DEFENSE // ADVISORY',
        timestamp: getTimestamp()
      }]);
    }

    setIsLoading(false);
  };

  // ── New Chat: reset to clean greeting ─────────────────────────────────────
  const handleNewChat = () => {
    setMessages([
      {
        type: 'assistant',
        text: INITIAL_GREETING,
        badge: 'PETER CYBER DEFENSE AI',
        timestamp: getTimestamp()
      }
    ]);
  };

  return (
    <div className="flex flex-col h-full bg-[#0A0A0C] text-slate-100 relative">
      {/* 1. TOP HEADER BAR */}
      <header className="flex items-center justify-between px-6 py-3 bg-[#0E1015] border-b border-[#232733]">
        <button
          onClick={() => setSidebarOpen(!sidebarOpen)}
          className="p-1 text-slate-400 hover:text-white rounded transition hover:bg-[#1A1E29]"
          title="Toggle Recon Sessions"
        >
          <Menu className="w-5 h-5" />
        </button>

        <h1 className="text-xl font-bold tracking-wide text-white font-sans">
          HackerGPT
        </h1>

        <button
          onClick={handleNewChat}
          className="flex items-center gap-1.5 px-3.5 py-1.5 text-xs font-semibold bg-[#161821] text-slate-300 border border-[#2F3545] rounded-md hover:bg-[#1F232F] hover:text-white transition"
        >
          <Plus className="w-3.5 h-3.5" />
          <span>chat</span>
        </button>
      </header>

      {/* 2. CHAT STREAM & OPTIONAL SIDEBAR */}
      <div className="flex flex-1 overflow-hidden">
        {/* Optional Drawer */}
        {sidebarOpen && (
          <aside className="w-64 bg-[#0B0D12] border-r border-[#1E222D] p-4 flex flex-col gap-2">
            <span className="text-[11px] font-bold text-slate-500 uppercase tracking-wider">
              Recon Sessions
            </span>
            {[
              'cybergym.hackergpt.app',
              'arusha-core.tz [Tanzania HQ]',
              'port-audit-192.168.1.1',
              'cve-2026-31902-openssl',
              'zero-trust-firewall-synth'
            ].map((sess, i) => (
              <button
                key={i}
                onClick={() => {
                  setInputVal(`Check ${sess}`);
                  setSidebarOpen(false);
                }}
                className="text-left text-xs p-2 rounded text-slate-400 hover:text-cyan-400 hover:bg-[#161922] transition truncate"
              >
                {sess}
              </button>
            ))}
          </aside>
        )}

        {/* Main Chat Scroll Area */}
        <main className="flex-1 overflow-y-auto p-6 flex flex-col gap-6">
          {messages.map((msg, idx) => {
            // ── User message ────────────────────────────────────────────────
            if (msg.type === 'user') {
              return (
                <div key={idx} className="pb-3 border-b border-[#212530]">
                  <p className="text-sm font-medium text-slate-200">{msg.text}</p>
                </div>
              );
            }

            // ── AI text message (greeting / security advice / out-of-scope) ─
            if (msg.type === 'assistant') {
              return (
                <AssistantMessage
                  key={idx}
                  text={msg.text}
                  badge={msg.badge}
                  timestamp={msg.timestamp}
                />
              );
            }

            // ── Recon snapshot ───────────────────────────────────────────────
            if (msg.type === 'recon') {
              return (
                <ReconCard
                  key={idx}
                  msg={msg}
                  expanded={expanded}
                  onToggleExpand={() => setExpanded(!expanded)}
                  copied={copied}
                  onCopy={() => handleCopy(msg.jsonData)}
                />
              );
            }

            return null;
          })}

          {/* Loading indicator */}
          {isLoading && (
            <div className="flex items-center gap-2 text-slate-500 text-xs font-mono animate-pulse">
              <Shield className="w-3.5 h-3.5 text-cyan-600" />
              <span>Analyzing query...</span>
            </div>
          )}

          <div ref={bottomRef} />
        </main>
      </div>

      {/* 3. BOTTOM CYBERPUNK CHAMFERED INPUT CONSOLE */}
      <footer className="p-6 pt-2">
        <div className="relative bg-[#111319] border border-[#384054] rounded-xl p-4 flex flex-col gap-3 max-w-4xl mx-auto shadow-2xl">
          {/* Top Notch Graphic Line */}
          <div className="absolute -top-[1px] left-8 w-20 border-t-2 border-dashed border-[#525D78]" />
          <div className="absolute -bottom-[1px] right-8 w-16 border-b-2 border-dashed border-[#525D78]" />

          <textarea
            value={inputVal}
            onChange={(e) => setInputVal(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSend();
              }
            }}
            placeholder="Message HackerGPT — ask about threats, malware, security best practices, or 'Check <domain>'"
            rows={2}
            className="w-full bg-transparent border-none text-slate-100 placeholder-slate-600 text-sm focus:outline-none resize-none"
          />

          <div className="flex items-center justify-between pt-1">
            <button
              onClick={() => alert("Upload file/payload dialog triggered.")}
              className="flex items-center gap-1.5 px-3 py-1.5 bg-[#171A23] border border-[#2B3142] rounded-md text-xs font-medium text-slate-400 hover:text-white hover:bg-[#1D212D] transition"
            >
              <Upload className="w-3.5 h-3.5" />
              <span>Upload</span>
            </button>

            <button
              onClick={handleSend}
              disabled={isLoading}
              className="w-9 h-8 bg-[#1A1E29] border border-[#353D52] hover:border-cyan-500/50 hover:bg-[#242B3B] text-slate-300 hover:text-white rounded-md flex items-center justify-center transition shadow disabled:opacity-40"
            >
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </footer>
    </div>
  );
}
