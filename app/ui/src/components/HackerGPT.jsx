import React, { useState } from 'react';
import { Menu, Plus, Copy, Check, Upload, ArrowRight, ChevronRight, ChevronDown } from 'lucide-react';

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

export default function HackerGPT() {
  const [copied, setCopied] = useState(false);
  const [expanded, setExpanded] = useState(true);
  const [inputVal, setInputVal] = useState('');
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [messages, setMessages] = useState([
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

  const handleCopy = (data) => {
    navigator.clipboard.writeText(JSON.stringify(data, null, 2));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleSend = () => {
    if (!inputVal.trim()) return;
    const query = inputVal.trim();
    setInputVal('');

    const newMessages = [...messages, { type: 'user', text: query }];

    // Realistic automated recon response
    const targetClean = query.replace(/^(check|scan|inspect)\s+/i, '').replace(/\/$/, '');
    const isArusha = /arusha|tz|tanzania/i.test(query);

    const generatedRecon = {
      type: 'recon',
      target: targetClean || 'target.cybersec.local',
      ip: isArusha ? '102.214.32.14' : '198.51.100.82',
      whois: isArusha 
        ? 'Tanzania Network Information Centre (tzNIC) - Peter Defense Grid Arusha.' 
        : 'ARIN Registry - Cloudflare / Fastly Edge Proxy.',
      jsonData: {
        target: `http://${targetClean || 'target.cybersec.local'}`,
        http_status: 200,
        request_config: {
          headers: {
            "User-Agent": "HackerGPT/4.2 (Zero-Trust Recon Engine; x64)"
          }
        },
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
    };

    setMessages([...newMessages, generatedRecon]);
  };

  const handleNewChat = () => {
    setMessages([
      {
        type: 'user',
        text: 'New reconnaissance session initialized.'
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
            if (msg.type === 'user') {
              return (
                <div key={idx} className="pb-3 border-b border-[#212530]">
                  <p className="text-sm font-medium text-slate-200">
                    {msg.text}
                  </p>
                </div>
              );
            }

            if (msg.type === 'recon') {
              return (
                <div key={idx} className="flex flex-col gap-4 max-w-4xl">
                  {/* Recon Title */}
                  <h2 className="text-base font-bold text-white tracking-wide">
                    {msg.target} - Quick Recon Snapshot
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
                        onClick={() => setExpanded(!expanded)}
                        className="flex items-center gap-1 text-slate-400 hover:text-white transition text-xs"
                      >
                        {expanded ? <ChevronDown className="w-3.5 h-3.5" /> : <ChevronRight className="w-3.5 h-3.5" />}
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
                          onClick={() => handleCopy(msg.jsonData)}
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

            return null;
          })}
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
            placeholder="Message HackerGPT"
            rows={2}
            className="w-full bg-transparent border-none text-slate-100 placeholder-slate-500 text-sm focus:outline-none resize-none"
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
              className="w-9 h-8 bg-[#1A1E29] border border-[#353D52] hover:border-cyan-500/50 hover:bg-[#242B3B] text-slate-300 hover:text-white rounded-md flex items-center justify-center transition shadow"
            >
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </footer>
    </div>
  );
}
