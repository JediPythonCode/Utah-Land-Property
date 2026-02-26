import streamlit as st
import streamlit.components.v1 as components
import os
import json

# --- 1. CORE LOGIC ---
try:
    from library import SHIELD_LIBRARY
    from automation_engine import generate_utah_addendum, generate_repc
except ImportError:
    # fallback for development
    SHIELD_LIBRARY = {"FinCEN_2026": "Active", "Assignment_Gator": "Active"}
    def generate_utah_addendum(data, shields):
        return "temp_addendum.pdf"
    def generate_repc(data):
        return "temp_repc.pdf"

# --- 2. PAGE SETUP ---
st.set_page_config(
    page_title="Utah Land & Property | Secure Asset Portal",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 3. PASSWORD SECRET ---
SECRET_PASSWORD = st.secrets.get("acquisition_password", "defaultpassword")

# --- 4. HIDE STREAMLIT UI ---
st.markdown("""
<style>
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {padding: 0;}
    [data-testid="stAppViewContainer"] { background-color: #fcfcfc; }
</style>
""", unsafe_allow_html=True)

# --- 5. SHIELD KEYS ---
shield_keys = list(SHIELD_LIBRARY.keys())

# --- 6. HTML DASHBOARD CONTENT ---
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Montserrat:wght@300;400;600&display=swap" rel="stylesheet">
<script src="https://cdn.tailwindcss.com"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
:root {{ --bhhs-cabernet: #631D33; --overlay: rgba(0,0,0,0.45); }}
body, html {{ margin:0; padding:0; font-family:'Montserrat',sans-serif; background:#fcfcfc; overflow-x:hidden; }}
.hero-container {{ position:relative; height:100vh; width:100%; background-image: linear-gradient(var(--overlay),var(--overlay)), url('https://images.unsplash.com/photo-1572120360610-d971b9b6398d?auto=format&fit=crop&w=2070'); background-size: cover; background-position:center; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; color:white; transition: transform 0.8s, opacity 0.6s; }}
.action-bar {{ background:white; padding:0.5rem; display:flex; width:90%; max-width:900px; box-shadow:0 10px 40px rgba(0,0,0,0.4); }}
.action-input {{ flex-grow:1; border:none; padding:1.2rem 2rem; font-size:1rem; color:#333; outline:none; }}
.action-button {{ background:var(--bhhs-cabernet); color:white; padding:0 2.5rem; text-transform:uppercase; letter-spacing:2px; font-size:0.8rem; font-weight:600; cursor:pointer; border:none; }}
#dashboard-view {{ display:none; opacity:0; transition:opacity 1s; }}
.glass-card {{ background:white; border:1px solid #e5e7eb; box-shadow:0 4px 15px rgba(0,0,0,0.03); }}
.accent-border {{ border-left:5px solid var(--bhhs-cabernet); }}
.fade-out-up {{ transform: translateY(-100%); opacity:0; }}
.visible {{ display:block !important; opacity:1 !important; }}
</style>
</head>
<body>

<section id="hero-section" class="hero-container">
    <header class="absolute top-0 left-0 p-10 flex flex-col text-left">
        <div class="text-2xl font-bold font-serif tracking-tight">UTAH LAND & PROPERTY</div>
        <div class="text-[0.65rem] uppercase tracking-[3px]">Acquisition, Investment, Development</div>
    </header>
    <div class="z-10 px-6">
        <h1 class="text-7xl font-serif font-bold mb-2">Precision Acquisition.</h1>
        <p class="text-[0.9rem] uppercase tracking-[6px] mb-6 font-300">The Gold Standard in Utah Land Asset Strategy.</p>
        <div class="action-bar mx-auto">
            <input type="password" id="acquisition-id" class="action-input" placeholder="Enter Acquisition ID...">
            <button onclick="login()" class="action-button">Access Vault</button>
        </div>
        <p class="text-[10px] text-gray-200 mt-4">Utah Land & Property Inc, are not licensed real estate agents or real estate brokers. We are investment professionals. All activity is monitored and compliant with Utah state regulations.</p>
    </div>
</section>

<section id="dashboard-view" class="min-h-screen bg-[#FDFDFD] pb-24">
    <div class="max-w-7xl mx-auto px-10 mt-16">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-10 mb-16">
            <div class="glass-card accent-border p-10">
                <div class="text-[10px] uppercase tracking-[3px] text-gray-400 mb-2 font-bold">Current Portfolio</div>
                <div class="text-4xl font-serif font-bold text-[var(--bhhs-cabernet)]">REPC + Addenda</div>
                <div class="text-[10px] text-emerald-600 mt-3 font-bold tracking-widest uppercase">View & Print Contracts</div>
            </div>
            <div class="glass-card p-10">
                <div class="text-[10px] uppercase tracking-[3px] text-gray-400 mb-2 font-bold">Total Land Holdings</div>
                <div class="text-4xl font-serif font-bold">18.42 AC</div>
            </div>
            <div class="glass-card p-10">
                <div class="text-[10px] uppercase tracking-[3px] text-gray-400 mb-2 font-bold">Liquidity Status</div>
                <div class="text-4xl font-serif font-bold">Premium</div>
            </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-10">
            <div class="glass-card p-12 h-[500px] flex flex-col">
                <h2 class="font-serif text-3xl mb-8">Asset Performance Trajectory</h2>
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
                        <button onclick="executeContracts()" class="w-full bg-[var(--bhhs-cabernet)] text-white py-4 font-bold uppercase tracking-[2px] text-xs">Generate & Preview Contracts</button>
                     </div>
                </div>
            </div>
        </div>
    </div>
</section>

<script>
const SECRET_PASSWORD = "{SECRET_PASSWORD}";

function login() {{
    const entered = document.getElementById('acquisition-id').value;
    if (entered === SECRET_PASSWORD) {{
        document.getElementById('hero-section').classList.add('fade-out-up');
        setTimeout(() => {{
            document.getElementById('hero-section').style.display = 'none';
            document.getElementById('dashboard-view').classList.add('visible');
            initChart();
        }}, 700);
    }} else {{
        alert('Invalid Acquisition ID');
    }}
}}

function initChart() {{
    const ctx = document.getElementById('stochasticChart').getContext('2d');
    new Chart(ctx, {{
        type: 'line',
        data: {{
            labels: ['M1', 'M2', 'M3', 'M4', 'M5', 'M6'],
            datasets: [{{ data: [8.74,8.85,8.80,8.92,9.10,9.25], borderColor:'#631D33', tension:0.4 }}]
        }},
        options: {{ responsive:true, maintainAspectRatio:false }}
    }});
}}

function executeContracts() {{
    const name = document.getElementById('seller-name-input').value;
    const addr = document.getElementById('property-address-input').value;
    window.parent.postMessage({{ type:'execute_contract', seller:name, address:addr }}, '*');
    alert("Contracts generated for: " + name + "\\nCheck sidebar to view or download.");
}}
</script>

</body>
</html>
"""

# --- 7. RENDER HTML ---
components.html(html_content, height=1000, scrolling=True)

# --- 8. SIDEBAR: PDF ENGINE & CONTRACT VIEW ---
with st.sidebar:
    st.markdown("### 💰 SECURE CONTRACT CENTER")
    st.info("Fill out the 'Property Address' above, then generate contracts. Preview and download below.")

    # Confirm details
    final_seller = st.text_input("Confirm Seller", "Owen")
    final_addr = st.text_input("Confirm Address", "")

    if st.button("Generate & Download REPC + Addenda"):
        if not final_addr:
            st.error("Address Required.")
        else:
            # REPC first
            repc_path = generate_repc({"seller": final_seller, "address": final_addr})
            addendum_path = generate_utah_addendum({"seller": final_seller, "address": final_addr, "addendum_no":"1"}, shield_keys)

            for file_path, fname in [(repc_path, f"REPC_{final_seller}.pdf"), (addendum_path, f"Addendum_{final_seller}.pdf")]:
                if os.path.exists(file_path):
                    with open(file_path, "rb") as f:
                        st.download_button(
                            label=f"Download {fname}",
                            data=f,
                            file_name=fname,
                            mime="application/pdf"
                        )
