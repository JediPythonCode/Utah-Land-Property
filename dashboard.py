import React, { useState, useEffect } from 'react';
import { 
  TrendingUp, 
  Map as MapIcon, 
  Activity, 
  Lock, 
  ChevronRight, 
  LogOut,
  Clock,
  ShieldCheck
} from 'lucide-react';

const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [passkey, setPasskey] = useState('');
  const [currentTime, setCurrentTime] = useState(new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }));

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }));
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  const handleLogin = (e) => {
    e.preventDefault();
    if (passkey.length > 3) {
      setIsAuthenticated(true);
    }
  };

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-[#050505] flex flex-col items-center justify-center font-serif text-[#e0e0e0] overflow-hidden">
        {/* Background Image with heavy vignette */}
        <div className="absolute inset-0 z-0">
          <img 
            src="https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&q=80&w=2070" 
            className="w-full h-full object-cover opacity-30 scale-110"
            alt="Utah Mountains"
          />
          <div className="absolute inset-0 bg-gradient-to-b from-[#050505]/60 via-[#050505]/90 to-[#050505]" />
        </div>

        <div className="relative z-10 w-full max-w-md px-8 text-center">
          <div className="mb-12 space-y-4">
            <h3 className="tracking-[0.6em] text-[#d4af37] text-xs font-light uppercase opacity-80">Established 1998</h3>
            <h1 className="text-5xl md:text-6xl font-medium tracking-tight mb-2">Utah Land <span className="text-[#d4af37]">&</span> Property</h1>
            <p className="font-sans text-[10px] tracking-[0.4em] text-white/40 uppercase">Private Asset Management Portal</p>
          </div>

          <form onSubmit={handleLogin} className="space-y-6">
            <div className="relative group">
              <input 
                type="password"
                placeholder="CLIENT ACCESS KEY"
                value={passkey}
                onChange={(e) => setPasskey(e.target.value)}
                className="w-full bg-transparent border-b border-white/10 py-4 text-center font-sans text-sm tracking-[0.3em] focus:outline-none focus:border-[#d4af37] transition-all placeholder:text-white/20"
              />
            </div>
            <button 
              type="submit"
              className="w-full group relative overflow-hidden border border-[#d4af37]/40 py-4 px-8 transition-all hover:bg-[#d4af37] hover:text-black"
            >
              <span className="font-sans text-[10px] tracking-[0.5em] uppercase transition-colors">Authenticate</span>
            </button>
          </form>

          <p className="mt-12 font-sans text-[9px] tracking-widest text-white/20 uppercase">
            Encrypted Session — Tier IV Security Environment
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#080808] text-[#e0e0e0] font-sans selection:bg-[#d4af37] selection:text-black">
      {/* Navigation */}
      <nav className="border-b border-white/5 px-8 py-6 flex justify-between items-center backdrop-blur-md sticky top-0 z-50 bg-[#080808]/80">
        <div className="flex items-center space-x-4">
          <div className="text-xl font-serif tracking-[0.3em] text-[#d4af37]">UL&P</div>
          <div className="h-4 w-[1px] bg-white/10 hidden md:block" />
          <div className="hidden md:flex items-center space-x-2 text-[10px] tracking-widest text-white/40">
            <ShieldCheck size={12} className="text-[#d4af37]" />
            <span>SECURE GATEWAY ACTIVE</span>
          </div>
        </div>
        
        <div className="flex items-center space-x-8 text-[10px] tracking-widest uppercase">
          <div className="hidden lg:flex space-x-6 text-white/60">
            <a href="#" className="hover:text-[#d4af37] transition-colors">Portfolio</a>
            <a href="#" className="hover:text-[#d4af37] transition-colors">Acquisitions</a>
            <a href="#" className="hover:text-[#d4af37] transition-colors">Reporting</a>
          </div>
          <div className="flex items-center space-x-4">
            <span className="text-white/40">{currentTime} MST</span>
            <button 
              onClick={() => setIsAuthenticated(false)}
              className="hover:text-[#d4af37] transition-colors flex items-center space-x-2"
            >
              <LogOut size={14} />
            </button>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-8 py-12 md:py-20">
        <header className="mb-16">
          <h2 className="font-serif text-5xl md:text-6xl mb-4 font-light">Portfolio Intelligence</h2>
          <p className="text-white/40 max-w-2xl text-sm leading-relaxed tracking-wide">
            Detailed performance analytics and management oversight for your private Utah land holdings and commercial assets.
          </p>
        </header>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-16">
          {[
            { label: 'Total Asset Value', value: '$18.42M', change: '+2.4%', icon: TrendingUp },
            { label: 'Acreage Under Mgmt', value: '1,240', change: 'Summit Co.', icon: MapIcon },
            { label: 'Active Listings', value: '12', change: '3 Pending', icon: Activity },
            { label: 'Annualized Yield', value: '8.14%', change: 'Projected', icon: TrendingUp },
          ].map((stat, i) => (
            <div key={i} className="group p-8 bg-[#0c0c0c] border border-white/5 hover:border-[#d4af37]/30 transition-all duration-500 relative overflow-hidden">
              <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                <stat.icon size={48} />
              </div>
              <p className="text-[10px] tracking-[0.2em] uppercase text-white/40 mb-4">{stat.label}</p>
              <h3 className="text-3xl font-serif text-[#d4af37] mb-2">{stat.value}</h3>
              <p className="text-[10px] tracking-widest text-white/20 uppercase">{stat.change}</p>
            </div>
          ))}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Chart Placeholder */}
          <div className="lg:col-span-2 p-8 bg-[#0c0c0c] border border-white/5">
            <div className="flex justify-between items-center mb-12">
              <h4 className="font-serif text-xl">Allocation by Region</h4>
              <div className="flex space-x-4 text-[9px] tracking-widest uppercase text-white/40">
                <span className="flex items-center space-x-2"><span className="w-2 h-2 rounded-full bg-[#d4af37]" /><span>Summit</span></span>
                <span className="flex items-center space-x-2"><span className="w-2 h-2 rounded-full bg-white/40" /><span>Wasatch</span></span>
              </div>
            </div>
            <div className="h-[300px] w-full flex items-end justify-between space-x-4">
              {[40, 70, 45, 90, 65, 80, 55, 100, 85, 95].map((h, i) => (
                <div key={i} className="flex-1 group relative">
                  <div 
                    className="bg-[#d4af37]/20 border-t border-[#d4af37] w-full transition-all duration-1000 group-hover:bg-[#d4af37]/40"
                    style={{ height: `${h}%` }}
                  />
                </div>
              ))}
            </div>
          </div>

          {/* Activity Sidebar */}
          <div className="p-8 bg-[#0c0c0c] border border-white/5 space-y-8">
            <div className="flex items-center justify-between">
              <h4 className="font-serif text-xl tracking-wide text-[#d4af37]">Audit Log</h4>
              <Clock size={16} className="text-white/20" />
            </div>
            
            <div className="space-y-6">
              {[
                { title: 'Park City Expansion', action: 'Permit Finalized', time: '2h ago' },
                { title: 'Heber Valley Parcel', action: 'Appraisal Updated', time: '1d ago' },
                { title: 'Moab Commercial', action: 'Contract Signed', time: '3d ago' },
                { title: 'Portfolio Review', action: 'Quarterly Audit', time: '5d ago' },
              ].map((item, i) => (
                <div key={i} className="group cursor-pointer border-b border-white/5 pb-4 last:border-0 hover:border-[#d4af37]/20 transition-colors">
                  <div className="flex justify-between items-start mb-1">
                    <p className="text-sm text-white/80 group-hover:text-[#d4af37] transition-colors font-medium tracking-wide">{item.title}</p>
                    <ChevronRight size={14} className="text-white/20 group-hover:translate-x-1 transition-transform" />
                  </div>
                  <div className="flex justify-between text-[10px] tracking-widest text-white/40 uppercase">
                    <span>{item.action}</span>
                    <span>{item.time}</span>
                  </div>
                </div>
              ))}
            </div>

            <button className="w-full mt-8 py-4 border border-white/10 text-[9px] tracking-[0.4em] uppercase hover:border-[#d4af37] transition-colors text-white/40 hover:text-[#d4af37]">
              View Full History
            </button>
          </div>
        </div>
      </main>

      <footer className="mt-20 border-t border-white/5 py-12 px-8 flex flex-col md:flex-row justify-between items-center text-[9px] tracking-[0.3em] text-white/20 uppercase">
        <p>&copy; 2024 Utah Land & Property Private Client Group</p>
        <div className="flex space-x-8 mt-4 md:mt-0">
          <a href="#" className="hover:text-white transition-colors">Terms of Access</a>
          <a href="#" className="hover:text-white transition-colors">Confidentiality</a>
          <a href="#" className="hover:text-white transition-colors">Support</a>
        </div>
      </footer>
    </div>
  );
};

export default App;
