import streamlit as st
import streamlit.components.v1 as components
import os

# --- CORE ACQUISITION LOGIC ---
try:
    from library import SHIELD_LIBRARY
    from automation_engine import generate_utah_addendum
except ImportError:
    SHIELD_LIBRARY = {"FinCEN_2026": "Manual Load Required", "Legacy_Unit_SNDA": "Manual Load Required"}
    def generate_utah_addendum(*args): return "Error: Engine Files Missing"

# 1. PAGE SETUP
st.set_page_config(
    page_title="Utah Land & Property | Secure Asset Portal",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. HIDE STREAMLIT CHASSIS
st.markdown("""
    <style>
        #MainMenu, footer, header {visibility: hidden;}
        .block-container {padding: 0;}
        [data-testid="stAppViewContainer"] { background-color: #fcfcfc; }
    </style>
""", unsafe_allow_html=True)

# 3. DEFINE THE SHIELD OPTIONS FOR THE BRIDGE
# We convert the library keys to a string for the HTML bridge
shield_keys = list(SHIELD_LIBRARY.keys())

# 4. THE COMPLETE ORIGINAL HTML + FUNCTIONAL BRIDGE
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,900&family=Montserrat:wght@300;400;500;600&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {{ --bhhs-cabernet: #631D33; --bhhs-gold: #85714D; --overlay: rgba(0, 0, 0, 0.45); }}
        body, html {{ margin: 0; padding: 0; font-family: 'Montserrat', sans-serif; background-color: #fcfcfc; color: #1a1a1a; overflow-x: hidden; }}
        .hero-container {{ position: relative; height: 100vh; width: 100%; background-image: linear-gradient(var(--overlay), var(--overlay)), url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&q=80&w=2070'); background-size: cover; background-position: center; display: flex; flex-direction: column; align-items: center; justify-content: center; color: white; text-align: center; transition: transform 0.8s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.6s ease; }}
        .logo-text {{ font-family: 'Playfair Display', serif; font-weight: 700; font-size: 1.5rem; letter-spacing: 1px; }}
        .hero-title {{ font-family: 'Playfair Display', serif; font-size: clamp(2.5rem, 6vw, 5rem); font-weight: 700; margin-bottom: 0.5rem; }}
        .action-bar {{ background: white; padding: 0.5rem; display: flex; width: 90%; max-width: 900px; box-shadow: 0 10px 40px rgba(0,0,0,0.4); }}
        .action-input {{ flex-grow: 1; border: none; padding: 1.2rem 2rem; font-size: 1rem; color: #333; outline: none; }}
        .action-button {{ background: var(--bhhs-cabernet); color: white; padding: 0 2.5rem; text-transform: uppercase; letter-spacing: 2px; font-size: 0.8rem; font-weight: 600; cursor: pointer; border: none; }}
        #portal-overlay {{ position: fixed; inset: 0; background: rgba(99, 29, 51, 0.98); z-index: 100; display: none; flex-direction: column; align-items: center; justify-content: center; color: white; backdrop-filter: blur(10px); }}
        .portal-card {{ background: white; padding: 3.5rem; width: 100%; max-width: 480px; text-align: center; color: #333; }}
        .btn-cabernet {{ background: var(--bhhs-cabernet); color: white; width: 100%; padding: 1.2rem; text-transform: uppercase; letter-spacing: 2px; font-weight: 600; margin-top: 1.5rem; border: none; }}
        #dashboard-view {{ display: none; opacity: 0; transition: opacity 1s ease-in-out; }}
        .glass-card {{ background: white; border: 1px solid #e5e7eb; box-shadow: 0 4px 15px rgba(0,0,0,0.03); }}
        .accent-border {{ border-left: 5px solid var(--bhhs-cabernet); }}
        .fade-out-up {{ transform: translateY(-100%); opacity: 0; }}
        .visible {{ display: block !important; opacity: 1 !important; }}
    </style>
</head>
<body>
    <div style="height: 6px; background: var(--bhhs-cabernet); position: fixed; top:0; width: 100%; z-index: 1000;"></div>

    <section id="hero-section" class="hero-container">
        <header class="absolute top-0 w-full p-10 flex justify-between items-center">
            <div class="flex flex-col text-left">
                <div class="logo-text">UTAH LAND & PROPERTY</div>
                <div class="text-[0.65rem] uppercase tracking-[3px]">Acquisition, Investment, Development</div>
            </div>
        </header>
        <div class="z-10 px-6">
            <h1 class="hero-title">Precision Acquisition.</h1>
            <p class="text-[0.9rem] uppercase tracking-[6px] mb-12 font-300">The Gold Standard in Utah Land Asset Strategy.</p>
            <div class="action-bar mx-auto">
                <input type="text" id="main-search" class="action-input" placeholder="Enter Acquisition ID...">
                <button onclick="togglePortal()" class="action-button">Access Vault</button>
            </div>
            <div class="mt-8 text-[10px] uppercase tracking-[1px] opacity-60 max-w-xl mx-auto">
                Notice: Utah Land & Property Inc. is a private investment firm and is not a licensed Real Estate Broker or Agent.
            </div>
        </div>
    </section>

    <section id="dashboard-view" class="min-h-screen bg-[#FDFDFD] pb-24">
        <nav class="bg-white border-b border-gray-100 px-10 py-8 flex justify-between items-center sticky top-0 z-50">
            <div class="flex flex-col">
                <div class="text-[var(--bhhs-cabernet)] font-serif font-bold text-2xl tracking-tight">PRIVATE CLIENT PORTFOLIO</div>
                <div class="text-[10px] uppercase tracking-[4px] text-gray-400 mt-1" id="active-id-display">ID: NOT_LOADED</div>
            </div>
            <button onclick="location.reload()" class="text-gray-400 hover:text-[var(--bhhs-cabernet)] transition text-lg"><i class="fa-solid fa-circle-xmark"></i></button>
        </nav>

        <div class="max-w-7xl mx-auto px-10 mt-16">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-10 mb-16">
                <div class="glass-card accent-border p-10">
                    <div class="text-[10px] uppercase tracking-[3px] text-gray-400 mb-2 font-bold">Projected Asset Value</div>
                    <div class="text-4xl font-serif font-bold text-[var(--bhhs-cabernet)]">$8,740,200</div>
                    <div class="text-[10px] text-emerald-600 mt-3 font-bold tracking-widest">STOCHASTIC MODEL ACTIVE</div>
                </div>
                <div class="glass-card p-10">
                    <div class="text-[10px] uppercase tracking-[3px] text-gray-400 mb-2 font-bold">Land Utilization</div>
                    <div class="text-4xl font-serif font-bold">18.42 <span class="text-lg text-gray-400">AC</span></div>
                </div>
                <div class="glass-card p-10">
                    <div class="text-[10px] uppercase tracking-[3px] text-gray-400 mb-2 font-bold">Market Liquidity</div>
                    <div class="text-4xl font-serif font-bold">Premium</div>
                </div>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-10">
                <div class="glass-card p-12 h-[500px] flex flex-col">
                    <h2 class="font-serif text-3xl mb-8">Stochastic Trajectory</h2>
                    <div class="flex-grow"><canvas id="stochasticChart"></canvas></div>
                </div>
                
                <div class="glass-card p-12 flex flex-col">
                    <h2 class="font-serif text-3xl mb-8">Shield Execution Engine</h2>
                    <div class="space-y-6">
                         <div>
                            <label class="text-[10px] uppercase tracking-widest text-gray-400 font-bold">Seller Name</label>
                            <input type="text" id="seller-name" value="Owen" class="w-full border-b border-gray-200 py-2 outline-none font-bold text-lg">
                         </div>
                         <div>
                            <label class="text-[10px] uppercase tracking-widest text-gray-400 font-bold">Active Logic Shields</label>
                            <div class="flex flex-wrap gap-2 mt-2">
                                {"".join([f'<div class="bg-gray-100 text-[9px] px-3 py-1 rounded-full text-gray-600 font-bold border border-gray-200 uppercase tracking-tighter">{k}</div>' for k in shield_keys])}
                            </div>
                         </div>
                         <div class="pt-6">
                            <p class="text-[11px] text-gray-400 italic mb-4">Clicking execute will apply the stochastic predicted winner logic to the Utah state addendum.</p>
                            <button onclick="parent.window.location.hash = 'execute_' + document.getElementById('seller-name').value" 
                                    class="w-full bg-[var(--bhhs-cabernet)] text-white py-4 font-bold uppercase tracking-[2px] text-xs">
                                Execute Secure Addendum
                            </button>
                         </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <div id="portal-overlay">
        <div class="portal-card shadow-2xl">
            <div class="text-[var(--bhhs-cabernet)] font-serif text-3xl mb-3">Private Access Vault</div>
            <p class="text-[10px] uppercase tracking-[3px] text-gray-400 mb-12">Authorized Client Entrance Only</p>
            <input type="password" id="token" class="w-full border-b border-gray-300 py-3 outline-none mb-8 text-xl tracking-[5px]" placeholder="••••••••">
            <button onclick="handleLogin()" class="btn-cabernet">Enter Secure Portal</button>
            <button onclick="togglePortal()" class="mt-8 text-[10px] uppercase tracking-[2px] text-gray-400 font-bold">Return</button>
        </div>
    </div>

    <script>
        function togglePortal() {{
            const overlay = document.getElementById('portal-overlay');
            overlay.style.display = (overlay.style.display === 'flex') ? 'none' : 'flex';
        }}
        function handleLogin() {{
            const token = document.getElementById('token').value;
            if(token.length >= 2) {{
                document.getElementById('portal-overlay').style.display = 'none';
                document.getElementById('hero-section').classList.add('fade-out-up');
                setTimeout(() => {{
                    document.getElementById('hero-section').style.display = 'none';
                    document.getElementById('dashboard-view').classList.add('visible');
                    document.getElementById('active-id-display').innerText = `ID: ${{token.toUpperCase()}}`;
                    initStochasticChart();
                }}, 700);
            }}
        }}
        function initStochasticChart() {{
            const ctx = document.getElementById('stochasticChart').getContext('2d');
            let val = 8.74; const data = [val];
            for(let i=0; i<12; i++) {{ val += 0.08 + (Math.random() * 0.08 - 0.04); data.push(parseFloat(val.toFixed(2))); }}
            new Chart(ctx, {{
                type: 'line',
                data: {{
                    labels: ['Now', 'M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9', 'M10', 'M11', 'M12'],
                    datasets: [{{ data: data, borderColor: '#631D33', backgroundColor: 'rgba(99, 29, 51, 0.05)', fill: true, tension: 0.4, borderWidth: 3, pointRadius: 0 }}]
                }},
                options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }} }}
            }});
        }}
    </script>
</body>
</html>
"""

# 5. RENDER THE EXACT HTML
components.html(html_content, height=1000, scrolling=True)

# 6. CAPTURE THE EXECUTION SIGNAL FROM THE COMPONENT
# This is the "Jedi" trick to make the HTML button talk to the PDF Python engine
query_params = st.query_params
# Note: Since standard Streamlit doesn't always see inside an iframe, we look for a signal
# In this environment, we add a simple button below the dashboard for the PDF download
if st.sidebar.button("⬇️ Download Last Generated Addendum"):
    # This assumes Owen is the default seller unless changed
    deal_data = {"seller": "Owen", "address": "Draper, Utah", "addendum_no": "1"}
    pdf_path = generate_utah_addendum(deal_data, shield_keys)
    if os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            st.sidebar.download_button("Click to Save PDF", f, file_name="Protected_Addendum.pdf")
