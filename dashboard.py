import streamlit as st
import streamlit.components.v1 as components
import os
from datetime import datetime
from automation_engine import generate_utah_addendum
from library import SHIELD_LIBRARY

# --- 1. PAGE SETUP (FORCE SIDEBAR) ---
st.set_page_config(
    page_title="Utah Land & Property | Secure Asset Portal",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded" 
)

# --- 2. CSS: SIDEBAR VISIBILITY & NO GAPS ---
st.markdown("""
    <style>
        #MainMenu, footer, header {visibility: hidden;}
        
        /* This pushes the main content to the right so it doesn't hide the sidebar */
        .main .block-container {
            padding-left: 5rem !important;
            padding-right: 5rem !important;
            max-width: 100% !important;
        }

        /* High-contrast Sidebar */
        [data-testid="stSidebar"] {
            background-color: #631D33 !important;
            color: white !important;
            border-right: 2px solid #D4AF37;
        }
        
        /* Make sidebar text white for readability */
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] label {
            color: white !important;
        }

        .stButton>button { 
            background-color: #D4AF37 !important; 
            color: black !important; 
            font-weight: bold; 
            border-radius: 0; 
            width: 100%; 
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. LOGIC PREP ---
SECRET_PASSWORD = st.secrets.get("acquisition_password", "gold2026")
contracts_list = ["REPC"] + [k for k in SHIELD_LIBRARY.keys() if k != "REPC"]

# --- 4. HTML/CSS DASHBOARD ---
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Montserrat:wght@300;400;600&display=swap" rel="stylesheet">
<script src="https://cdn.tailwindcss.com"></script>
<style>
:root {{ --bhhs-cabernet: #631D33; --overlay: rgba(0, 0, 0, 0.45); }}
body, html {{ margin:0; padding:0; font-family:'Montserrat', sans-serif; background-color:#fcfcfc; color:#1a1a1a; overflow-x:hidden; }}
.hero-container {{ position:relative; height:100vh; width:100%; background-image: linear-gradient(var(--overlay), var(--overlay)), url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&q=80&w=2070'); background-size:cover; background-position:center; display:flex; flex-direction:column; align-items:center; justify-content:center; color:white; text-align:center; }}
.action-bar {{ background:white; padding:0.5rem; display:flex; width:90%; max-width:900px; box-shadow:0 10px 40px rgba(0,0,0,0.4); }}
.action-input {{ flex-grow:1; border:none; padding:1.2rem 2rem; font-size:1rem; color:#333; outline:none; }}
.action-button {{ background:var(--bhhs-cabernet); color:white; padding:0 2.5rem; text-transform:uppercase; letter-spacing:2px; font-size:0.8rem; font-weight:600; cursor:pointer; border:none; }}
#dashboard-view {{ display:none; opacity:0; transition: opacity 1s ease-in-out; }}
.glass-card {{ background:white; border:1px solid #e5e7eb; box-shadow:0 4px 15px rgba(0,0,0,0.03); }}
.visible {{ display:block !important; opacity:1 !important; }}
label {{ font-size:10px; text-transform:uppercase; font-weight:bold; color:#6b7280; }}
input, select {{ font-size:14px; padding:0.5rem; border:1px solid #d1d5db; border-radius:4px; width:100%; color: black !important; }}
.disclaimer {{ font-size:12px; font-weight:bold; color:white; margin-top: 2rem; max-width: 800px; line-height: 1.4; }}
</style>
</head>
<body>
<section id="hero-section" class="hero-container">
    <header class="absolute top-0 left-0 p-10">
        <div class="text-2xl font-bold font-serif tracking-tight">UTAH LAND & PROPERTY</div>
    </header>
    <div class="z-10 px-6 text-center flex flex-col items-center">
        <h1 class="text-7xl font-serif font-bold mb-2">Precision Acquisition.</h1>
        <p class="text-[0.9rem] uppercase tracking-[6px] mb-12 font-300">The Gold Standard in Utah Land Asset Strategy.</p>
        <div class="action-bar">
            <input type="password" id="main-search" class="action-input" placeholder="Enter Acquisition ID...">
            <button onclick="handleLogin()" class="action-button">Enter Vault</button>
        </div>
        <p class="disclaimer">
            Utah Land & Property Inc, are not licensed real estate agents or brokers. We are investment professionals. All activity is monitored and compliant with Utah regulations.
        </p>
    </div>
</section>

<section id="dashboard-view" class="min-h-screen bg-[#FDFDFD] pb-24">
    <div class="max-w-7xl mx-auto px-10 mt-16 grid grid-cols-1 lg:grid-cols-2 gap-10">
        <div class="glass-card p-12">
            <h2 class="font-serif text-3xl mb-8">Property & Contract</h2>
            <div class="space-y-4">
                <div><label>Seller Name</label><input type="text" id="s-name" value="Owen"></div>
                <div><label>Property Address</label><input type="text" id="s-addr" placeholder="Enter Utah Address"></div>
                <div><label>Parcel ID</label><input type="text" id="s-parcel" placeholder="Enter Parcel ID"></div>
                <div>
                    <label>Select Contracts</label>
                    <select id="s-contracts" multiple size="8">
                        {"".join([f'<option value="{c}">{c}</option>' for c in contracts_list])}
                    </select>
                </div>
                <button onclick="syncData()" class="w-full bg-[var(--bhhs-cabernet)] text-white py-4 font-bold uppercase tracking-[2px] text-xs">Sync to Sidebar Printer</button>
            </div>
        </div>
        <div class="glass-card p-12">
            <h2 class="font-serif text-3xl mb-8">Status Log</h2>
            <textarea id="preview-area" rows="15" class="w-full border p-4 font-mono text-sm" readonly></textarea>
        </div>
    </div>
</section>

<script>
function handleLogin() {{
    if(document.getElementById('main-search').value === "{SECRET_PASSWORD}") {{
        document.getElementById('hero-section').style.display = 'none';
        document.getElementById('dashboard-view').classList.add('visible');
    }} else {{ alert('Access Denied'); }}
}}
function syncData() {{
    const name = document.getElementById('s-name').value;
    const addr = document.getElementById('s-addr').value;
    document.getElementById('preview-area').value = "READY TO BIND\\nSELLER: "+name+"\\nADDR: "+addr+"\\n\\nSIDEBAR PRINTER IS NOW ACTIVE ON THE LEFT.";
}}
</script>
</body>
</html>
"""

components.html(html_content, height=1000, scrolling=True)

# --- 5. SIDEBAR: SECURE PRINTER (FORCED VISIBLE ON LEFT) ---
with st.sidebar:
    st.title("🏔️ PRINTER TRAY")
    st.markdown("Select your date and verify before generating.")
    
    # DYNAMIC DATE PICKER
    selected_date = st.date_input("Contract Date", datetime.now())
    
    st.markdown("---")
    f_n = st.text_input("Verify Seller", value="Owen")
    f_a = st.text_input("Verify Address")
    f_p = st.text_input("Verify Parcel ID")
    f_t = st.text_area("Selected Docs (comma separated)")

    if st.button("GENERATE FINAL PDF"):
        if f_n and f_a:
            deal_data = {{
                "seller_name": f_n,
                "address": f_a,
                "parcel_id": f_p,
                "repc_date": selected_date.strftime("%m/%d/%Y"),
                "addendum_no": "1"
            }}
            try:
                pdf = generate_utah_addendum(deal_data, [c.strip() for c in f_t.split(",")])
                if pdf and os.path.exists(pdf):
                    with open(pdf, "rb") as f:
                        st.download_button("📥 DOWNLOAD REPC", f, file_name=f"REPC_{f_n}.pdf")
            except Exception as e:
                st.error(f"Error: {e}")
