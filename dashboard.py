import streamlit as st
import streamlit.components.v1 as components
import os
import json

# --- 1. PAGE SETUP (Original) ---
st.set_page_config(
    page_title="Utah Land & Property | Secure Asset Portal",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. STYLING (Original) ---
st.markdown("""
    <style>
        #MainMenu, footer, header {visibility: hidden;}
        .block-container {padding: 0;}
        [data-testid="stAppViewContainer"] { background-color: #fcfcfc; }
    </style>
""", unsafe_allow_html=True)

# --- 3. PERSISTENCE LAYER ---
DATA_FILE = "data/shields_2026.json"

def update_json_data(parcel_id, status):
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f: data = json.load(f)
        if parcel_id in data:
            data[parcel_id]["status"] = status
            with open(DATA_FILE, "w") as f: json.dump(data, f, indent=4)

# --- 4. ORIGINAL HTML DESIGN (Unmolested) ---
# Note: I have updated the button 'onclick' to trigger the backend logic via URL params
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
.hero-container {{ position:relative; height:100vh; width:100%; background-image: linear-gradient(var(--overlay), var(--overlay)), url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&q=80&w=2070'); background-size:cover; background-position:center; display:flex; flex-direction:column; align-items:center; justify-content:center; color:white; text-align:center; transition: transform 0.8s ease, opacity 0.6s ease; }}
.action-bar {{ background:white; padding:0.5rem; display:flex; width:90%; max-width:900px; box-shadow:0 10px 40px rgba(0,0,0,0.4); }}
.action-input {{ flex-grow:1; border:none; padding:1.2rem 2rem; font-size:1rem; color:#333; outline:none; }}
.action-button {{ background:var(--bhhs-cabernet); color:white; padding:0 2.5rem; text-transform:uppercase; letter-spacing:2px; font-size:0.8rem; font-weight:600; cursor:pointer; border:none; }}
#dashboard-view {{ display:none; opacity:0; transition: opacity 1s ease-in-out; }}
.glass-card {{ background:white; border:1px solid #e5e7eb; box-shadow:0 4px 15px rgba(0,0,0,0.03); }}
.fade-out-up {{ transform:translateY(-100%); opacity:0; }}
.visible {{ display:block !important; opacity:1 !important; }}
.disclaimer {{ font-size:12px; font-weight:bold; color:white; }}
</style>
</head>
<body>
<section id="hero-section" class="hero-container">
    <header class="absolute top-0 left-0 p-10"><div class="text-2xl font-bold font-serif tracking-tight">UTAH LAND & PROPERTY</div></header>
    <div class="z-10 px-6 text-center">
        <h1 class="text-7xl font-serif font-bold mb-2">Precision Acquisition.</h1>
        <div class="action-bar mx-auto">
            <input type="password" id="main-search" class="action-input" placeholder="Enter Acquisition ID...">
            <button onclick="handleLogin()" class="action-button">Enter Vault</button>
        </div>
    </div>
    <p class="mt-6 disclaimer">Notice: Utah Land & Property Inc. is a private investment firm.</p>
</section>
<section id="dashboard-view" class="min-h-screen bg-[#FDFDFD] pb-24">
    <div class="max-w-7xl mx-auto px-10 mt-16">
        <div class="flex justify-between mb-12 border-b pb-8">
            <div class="text-sm font-bold uppercase">Status: <span id="deal-status" class="text-bhhs-cabernet">Initial Review</span></div>
            <div class="flex gap-4">
                <button onclick="window.parent.location.href='?action=upload'" class="bg-gray-100 px-6 py-2 text-xs font-bold uppercase">Upload Documents</button>
                <button onclick="window.parent.location.href='?action=esign'" class="bg-[var(--bhhs-cabernet)] text-white px-6 py-2 text-xs font-bold uppercase">Request E-Sign</button>
            </div>
        </div>
    </div>
</section>
<script>
function handleLogin() {{
    document.getElementById('hero-section').classList.add('fade-out-up');
    setTimeout(() => {{ document.getElementById('hero-section').style.display = 'none'; document.getElementById('dashboard-view').classList.add('visible'); }}, 700);
}}
</script>
</body>
</html>
"""

# --- 5. RENDER & FUNCTIONAL LOGIC ---
components.html(html_content, height=1000, scrolling=True)

# Functional Bridge (Using URL Params to avoid external module crashes)
params = st.query_params
p_id = "USER_SESSION_PARCEL" # Replace with your dynamic ID capture
if "action" in params:
    if params["action"] == "upload":
        with st.sidebar:
            uploaded = st.file_uploader("Upload Docs")
            if uploaded:
                update_json_data(p_id, "DOCS_RECEIVED")
                st.success("File Processed.")
    elif params["action"] == "esign":
        st.sidebar.info("E-Sign Request Dispatched.")
        if st.sidebar.button("Confirm Request"):
            update_json_data(p_id, "ESIGN_PENDING")
