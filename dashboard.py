import React, { useState, useEffect } from 'react';
import { 
  TrendingUp, 
  Map as MapIcon, 
  Activity, 
  Lock, 
  ChevronRight, 
  LogOut,
  Clock,
  ShieldCheck,
  BarChart3,
  Globe
} from 'lucide-react';

const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [passkey, setPasskey] = useState('');
  const [currentTime, setCurrentTime] = useState('');

  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      setCurrentTime(now.toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit',
        second: '2-digit',
        hour12: false 
      }) + ' MST');
    };
    updateTime();
    const timer = setInterval(updateTime, 1000);
    return () => clearInterval(timer);
  }, []);

  const handleLogin = (e) => {
    e.preventDefault();
    if (passkey.length >= 4) {
      setIsAuthenticated(true);
    }
  };

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-[#050505] flex flex-col items-center justify-center font-serif text-[#e0e0e0] overflow-hidden relative">
        {/* Cinematic Background */}
        <div className="absolute inset-0 z-0">
          <img 
            src="https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&q=80&w=2000" 
            className="w-full h-full object-cover opacity-20 scale-105"
            alt="Mountain Landscape"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-[#050505] via-[#050505]/80 to-transparent" />
        </div>

        <div className="relative z-10 w-full max-w-md px-10 text-center">
          <div className="mb-16 space-y-6">
            <div className="flex justify-center mb-8">
              <div className="w-12 h-[1px] bg-[#d4af37] self-center" />
              <Lock className="mx-4 text-[#d4af37] opacity-60" size={20} />
              <div className="w-12 h-[1px] bg-[#d4af37] self-center" />
            </div>
            <h1 className="text-4xl md:text-5xl font-light tracking-[0.15em] mb-2 uppercase">
              Utah Land <span className="text-[#d4af37] font-normal">&</span> Prop
            </h1>
            <p className="font-sans text-[10px] tracking-[0.5em] text-white/30 uppercase">
              Private Wealth Management
            </p>
          </div>

          <form onSubmit={handleLogin} className="space-y-8">
            <div className="relative border-b border-white/10 focus-within:border-[#d4af37] transition-colors">
              <input 
                type="password"
                placeholder="ENTER ACCESS KEY"
                value={passkey}
                onChange={(e) => setPasskey(e.target.value)}
                className="w-full bg-transparent py-4 text-center font-sans text-xs tracking-[0.4em] focus:outline-none placeholder:text-white/10 text-[#d4af37]"
              />
            </div>
            <button 
              type="submit"
              className="w-full py-4 border border-[#d4af37]/40 hover:bg-[#d4af37] hover:text-black transition-all duration-500 font-sans text-[10px] tracking-[0.6em] uppercase"
            >
              Authorize
            </button>
          </form>

          <div className="mt-20 flex flex-col items-center space-y-2 opacity-20 hover:opacity-100 transition-opacity duration-700">
            <div className="h-[40px] w-[1px] bg-[#d4af37]" />
            <p className="font-sans text-[8px] tracking-[0.3em] uppercase">
              Tier IV Secure Environment
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0a0a0a] text-[#f0f0f0] font-sans selection:bg-[#d4af37]/30">
      {/* Top Navigation */}
      <nav className="border-b border-white/5 px-10 py-6 flex justify-between items-center bg-[#0a0a0a]/90 backdrop-blur-xl sticky top-0 z-50">
        <div className="flex items-center space-x-8">
          <div className="text-xl font-serif tracking-[0.4em] text-[#d4af37] cursor-pointer">ULP</div>
          <div className="hidden lg:flex items-center space-x-6 text-[9px] tracking-[0.3em] text-white/30 uppercase">
            <span className="text-[#d4af37] flex items-center gap-2"><div className="w-1 h-1 rounded-full bg-[#d4af37] animate-pulse" /> Live Portfolio</span>
            <span className="hover:text-white transition-colors cursor-pointer">Global Markets</span>
            <span className="hover:text-white transition-colors cursor-pointer">Advisory</span>
          </div>
        </div>
        
        <div className="flex items-center space-x-8">
          <div className="hidden md:flex flex-col items-end">
            <span className="text-[10px] tracking-widest text-white/40">{currentTime}</span>
            <span className="text-[8px] tracking-[0.2em] text-[#d4af37]/60">ENCRYPTED SESSION</span>
          </div>
          <button 
            onClick={() => setIsAuthenticated(false)}
            className="p-2 hover:text-[#d4af37] transition-colors"
          >
            <LogOut size={18} strokeWidth={1.5} />
          </button>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-10 pt-20 pb-12">
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-16 gap-8">
          <div>
            <h4 className="text-[#d4af37] text-[10px] tracking-[0.5em] uppercase mb-4">Executive Summary</h4>
            <h2 className="text-5xl md:text-7xl font-serif font-light tracking-tight">Portfolio Performance</h2>
          </div>
          <div className="bg-white/5 p-4 border-l border-[#d4af37] flex gap-8">
            <div>
              <p className="text-[9px] text-white/40 uppercase tracking-widest mb-1">AUM</p>
              <p className="text-xl font-serif">$24.8M</p>
            </div>
            <div>
              <p className="text-[9px] text-white/40 uppercase tracking-widest mb-1">YTD Return</p>
              <p className="text-xl font-serif text-emerald-500">+12.4%</p>
            </div>
          </div>
        </div>

        {/* Intelligence Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          {[
            { label: 'Real Estate Holdings', value: '14 Assets', sub: 'Summit & Wasatch Co.', icon: MapIcon },
            { label: 'Liquidity Position', value: '$4.2M', sub: 'Cash Equivalents', icon: Activity },
            { label: 'Market Sentiment', value: 'Bullish', sub: 'Utah Growth Index', icon: Globe },
          ].map((card, i) => (
            <div key={i} className="group p-10 bg-[#0f0f0f] border border-white/5 hover:border-[#d4af37]/20 transition-all duration-500">
              <card.icon size={24} className="text-[#d4af37] mb-8 opacity-40 group-hover:opacity-100 transition-opacity" strokeWidth={1} />
              <p className="text-[10px] tracking-[0.3em] uppercase text-white/30 mb-2">{card.label}</p>
              <h3 className="text-3xl font-serif mb-2">{card.value}</h3>
              <p className="text-[10px] tracking-widest text-white/20 uppercase">{card.sub}</p>
            </div>
          ))}
        </div>

        {/* Secondary Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 p-10 bg-[#0f0f0f] border border-white/5">
            <div className="flex justify-between items-center mb-12">
              <h4 className="text-[11px] tracking-[0.4em] uppercase text-white/60 flex items-center gap-3">
                <BarChart3 size={14} className="text-[#d4af37]" /> Growth Trajectory
              </h4>
              <div className="text-[9px] tracking-widest text-white/20">QUARTERLY AGGREGATE</div>
            </div>
            <div className="h-[300px] flex items-end justify-between gap-2">
              {[60, 45, 80, 55, 90, 70, 100, 85, 95, 75, 110, 105].map((h, i) => (
                <div key={i} className="flex-1 group relative">
                  <div 
                    className="w-full bg-[#d4af37]/10 group-hover:bg-[#d4af37]/30 transition-all duration-700 border-t border-[#d4af37]/20 group-hover:border-[#d4af37]"
                    style={{ height: `${h}%` }}
                  />
                </div>
              ))}
            </div>
          </div>

          <div className="p-10 bg-[#0f0f0f] border border-white/5">
            <h4 className="text-[11px] tracking-[0.4em] uppercase text-white/60 mb-10">Recent Logins</h4>
            <div className="space-y-8">
              {[
                { loc: 'Salt Lake City, UT', device: 'Workstation 01', time: 'Just Now' },
                { loc: 'Park City, UT', device: 'Mobile Device', time: '4h ago' },
                { loc: 'London, UK', device: 'Secure Gateway', time: '1d ago' },
              ].map((log, i) => (
                <div key={i} className="flex justify-between items-start border-b border-white/5 pb-4 last:border-0">
                  <div>
                    <p className="text-sm font-medium text-white/80">{log.loc}</p>
                    <p className="text-[9px] tracking-widest text-white/30 uppercase">{log.device}</p>
                  </div>
                  <span className="text-[9px] text-[#d4af37]/60 font-mono uppercase">{log.time}</span>
                </div>
              ))}
            </div>
            <button className="w-full mt-12 py-4 border border-white/5 text-[9px] tracking-[0.4em] uppercase text-white/30 hover:text-[#d4af37] hover:border-[#d4af37]/30 transition-all">
              Security Audit
            </button>
          </div>
        </div>
      </div>

      <footer className="py-20 border-t border-white/5 flex flex-col items-center">
        <div className="text-[#d4af37] font-serif tracking-[0.8em] text-xs mb-6">UTAH LAND & PROPERTY</div>
        <p className="text-[9px] tracking-[0.4em] text-white/10 uppercase mb-8">Confidential Asset Management Interface</p>
        <div className="flex space-x-12 text-[8px] tracking-[0.2em] text-white/20 uppercase">
          <span className="hover:text-white transition-colors cursor-pointer">Protocol 4.0</span>
          <span className="hover:text-white transition-colors cursor-pointer">End-to-End Encryption</span>
          <span className="hover:text-white transition-colors cursor-pointer">Privacy Policy</span>
        </div>
      </footer>
    </div>
  );
};

export default App;
