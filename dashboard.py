import streamlit as st
import streamlit.components.v1 as components
import os
import json

# --- 1. CORE LOGIC ---
try:
    from library import SHIELD_LIBRARY
    from automation_engine import generate_utah_addendum
except ImportError:
    SHIELD_LIBRARY = {"FinCEN_2026": "Active", "Assignment_Gator": "Active"}
    def generate_utah_addendum(d, s): return "temp.pdf"

# --- 2. PAGE SETUP ---
st.set_page_config(
    page_title="Utah Land & Property | Secure Asset Portal",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit UI completely
st.markdown("""
    <style>
        #MainMenu, footer, header {visibility: hidden;}
        .block-container {padding: 0;}
        [data-testid="stAppViewContainer"] { background-color: #fcfcfc; }
    </style>
""", unsafe_allow_html=True)

# --- 3. THE ORIGINAL LAYOUT (IDENTICAL) ---
# I have added the 'Address' input to your original layout logic
shield_keys = list(SHIELD_LIBRARY.keys())

html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Montserrat:wght@300;400;600&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {{ --bhhs-cabernet: #631D33; --overlay: rgba(0, 0, 0, 0.45); }}
        body, html {{ margin: 0; padding: 0; font-family: 'Montserrat', sans-serif; background-color: #fcfcfc; color: #1a1a1a; overflow-x: hidden; }}
        .hero-container {{ position: relative; height: 100vh; width: 100%; background-image: linear-gradient(var(--overlay), var(--overlay)), url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&q=80&w=2070'); background-size: cover; background-position: center; display: flex; flex-direction: column; align-items: center; justify-content: center; color: white; text-align: center; transition: transform 0.8s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.6s ease; }}
        .action-bar {{ background: white; padding: 0.5rem; display: flex; width: 90%; max-width: 900px; box-shadow: 0 10px 40px rgba(0,0,0,0.4); }}
        .action-input {{ flex-grow: 1; border: none; padding: 1.2rem 2rem; font-size: 1rem; color: #333; outline: none; }}
        .action-button {{ background: var(--bhhs-cabernet); color: white; padding: 0 2.5rem; text-transform: uppercase; letter-spacing: 2px; font-size: 0.8rem; font-weight: 600; cursor: pointer; border: none; }}
        #portal-overlay {{ position: fixed; inset: 0; background: rgba(99, 29, 51, 0.98); z-index: 100; display: none; flex-direction: column; align-items: center; justify-content: center; color: white; backdrop-filter: blur(10px); }}
        .portal-card {{ background: white; padding: 3.5rem; width: 100%; max-width: 480px; text-align: center; color: #333; }}
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
                <div class="text-2xl font-bold font-serif tracking-tight">UTAH LAND & PROPERTY</div>
                <div class="text-[0.65rem] uppercase tracking-[3px]">Acquisition, Investment, Development</div>
            </div>
        </header>
        <div class="z-10 px-6">
            <h1 class="text-7xl font-serif font-bold mb-2">Precision Acquisition.</h1>
            <p class="text-[0.9rem] uppercase tracking-[6px] mb-12 font-300">The Gold Standard in Utah Land Asset Strategy.</p>
            <div class="action-bar mx-auto">
                <input type="text" id="main-search" class="action-input" placeholder="Enter Acquisition ID...">
                <button onclick="togglePortal()" class="action-button">Access Vault</button>
            </div>
        </div>
    </section>

    <section id="dashboard-view" class="min-h-screen bg-[#FDFDFD] pb-24">
        <nav class="bg-white border-b border-gray-100 px-10 py-8 flex justify-between items-center sticky top-0 z-50">
            <div class="flex flex-col">
                <div class="text-[var(--bhhs-cabernet)] font-serif font-bold text-2xl tracking-tight">PRIVATE CLIENT PORTFOLIO</div>
                <div class="text-[10px] uppercase tracking-[4px] text-gray-400 mt-1" id="active-id-display">ID: OWEN</div>
            </div>
        </nav>

        <div class="max-w-7xl mx-auto px-10 mt-16">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-10 mb-16">
                <div class="glass-card accent-border p-10">
                    <div class="text-[10px] uppercase tracking-[3px] text-gray-400 mb-2 font-bold">Projected Asset Value</div>
                    <div class="text-4xl font-serif font-bold text-[var(--bhhs-cabernet)]">$8,740,200</div>
                    <div class="text-[10px] text-emerald-600 mt-3 font-bold tracking-widest uppercase">Stochastic Model Active</div>
                </div>
                <div class="glass-card p-10">
                    <div class="text-[10px] uppercase tracking-[3px] text-gray-400 mb-2 font-bold">Land Utilization</div>
                    <div class="text-4xl font-serif font-bold">18.42 AC</div>
                </div>
                <div class="glass-card p-10">
                    <div class="text-[10px] uppercase tracking-[3px] text-gray-400 mb-2 font-bold">Market Liquidity</div>
                    <div class="text-4xl font-serif font-bold">Premium</div>
                </div>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-10">
                <div class="glass-card p-12 h-[500px] flex flex-col">
                    <h2 class="font-serif text-3xl mb-8">Stochastic Trajectory</h2>
                    <canvas id="stochasticChart"></canvas>
                </div>
                
                <div class="glass-card p-12">
                    <h2 class="font-serif text-3xl mb-8">Shield Execution Engine</h2>
                    <div class="space-y-6">
                         <div>
                            <label class="text-[10px] uppercase font-bold text-gray-400">Seller Name</label>
                            <input type="text" id="seller-name-input" value="Owen" class="w-full border-b border-gray-200 py-2 outline-none font-bold text-lg">
                         </div>
                         <div>
                            <label class="text-[10px] uppercase font-bold text-gray-400">Property Address</label>
                            <input type="text" id="property-address-input" placeholder="Enter Utah Address..." class="w-full border-b border-gray-200 py-2 outline-none font-bold text-lg">
                         </div>
                         <div>
                            <label class="text-[10px] uppercase font-bold text-gray-400">Active Logic Shields</label>
                            <div class="flex flex-wrap gap-2 mt-2">
                                {"".join([f'<div class="bg-gray-100 text-[9px] px-3 py-1 rounded-full text-gray-600 font-bold border border-gray-200 uppercase">{k}</div>' for k in shield_keys])}
                            </div>
                         </div>
                         <div class="pt-6">
                            <button onclick="handleExecution()" class="w-full bg-[var(--bhhs-cabernet)] text-white py-4 font-bold uppercase tracking-[2px] text-xs">Execute Secure Addendum</button>
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
            <input type="password" id="token" class="w-full border-b border-gray-300 py-3 outline-none mb-8 text-xl text-center" placeholder="••••••••">
            <button onclick="handleLogin()" class="w-full bg-[var(--bhhs-cabernet)] text-white py-4 font-bold uppercase">Enter Secure Portal</button>
        </div>
    </div>

    <script>
        function togglePortal() {{ document.getElementById('portal-overlay').style.display = 'flex'; }}
        
        function handleLogin() {{
            document.getElementById('portal-overlay').style.display = 'none';
            document.getElementById('hero-section').classList.add('fade-out-up');
            setTimeout(() => {{
                document.getElementById('hero-section').style.display = 'none';
                document.getElementById('dashboard-view').classList.add('visible');
                initChart();
            }}, 700);
        }}

        function initChart() {{
            const ctx = document.getElementById('stochasticChart').getContext('2d');
            new Chart(ctx, {{
                type: 'line',
                data: {{
                    labels: ['M1', 'M2', 'M3', 'M4', 'M5', 'M6'],
                    datasets: [{{ data: [8.74, 8.85, 8.80, 8.92, 9.10, 9.25], borderColor: '#631D33', tension: 0.4 }}]
                }},
                options: {{ responsive: true, maintainAspectRatio: false }}
            }});
        }}

        function handleExecution() {{
            const name = document.getElementById('seller-name-input').value;
            const addr = document.getElementById('property-address-input').value;
            // Sending the data out to Streamlit
            window.parent.postMessage({{
                type: 'execute_contract',
                seller: name,
                address: addr
            }}, '*');
            alert("Contract logic bound for: " + name + "\\nProceed to sidebar for download.");
        }}
    </script>
</body>
</html>
"""

# --- 4. RENDER & BRIDGE ---
components.html(html_content, height=1000, scrolling=True)

# --- 5. THE HIDDEN ENGINE (SIDEBAR) ---
# Since we cannot have a "Save As" dialog pop up from inside the HTML component, 
# the Sidebar acts as the "Printer Tray" where the physical file appears.
with st.sidebar:
    st.markdown("### 🏔️ SECURE PRINTER TRAY")
    st.info("Fill out the 'Property Address' in the dashboard, then click Execute. Your file will appear here.")
    
    # These interact with the Python engine
    with st.expander("Stochastic Engine Settings", expanded=True):
        final_seller = st.text_input("Confirm Seller", "Owen")
        final_addr = st.text_input("Confirm Address", "")
    
    if st.button("Generate & Download PDF"):
        if not final_addr:
            st.error("Address Required.")
        else:
            data = {{"seller": final_seller, "address": final_addr, "addendum_no": "1"}}
            path = generate_utah_addendum(data, shield_keys)
            
            if os.path.exists(path):
                with open(path, "rb") as f:
                    st.download_button(
                        label="CLICK TO SAVE FINAL PDF",
                        data=f,
                        file_name=f"Addendum_{final_seller}.pdf",
                        mime="application/pdf"
                    )
