import streamlit as st
import streamlit.components.v1 as components
import os
import json
from library import SHIELD_LIBRARY
from automation_engine import generate_utah_addendum

# --- 1. PERSISTENCE ENGINE (HIDDEN) ---
DATA_FILE = "data/shields_2026.json"
def update_json(parcel_id, status):
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f: data = json.load(f)
        if parcel_id in data:
            data[parcel_id]["status"] = status
            with open(DATA_FILE, "w") as f: json.dump(data, f, indent=4)

# --- 2. THE ORIGINAL CODE (Unchanged) ---
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
label {{ font-size:10px; text-transform:uppercase; font-weight:bold; color:#6b7280; }}
input, select {{ font-size:14px; padding:0.5rem; border:1px solid #d1d5db; border-radius:5px; width:100%; }}
.disclaimer {{ font-size:12px; font-weight:bold; color:white; }}
</style>
</head>
<body>
<section id="hero-section" class="hero-container">
    <header class="absolute top-0 left-0 p-10">
        <div class="text-2xl font-bold font-serif tracking-tight">UTAH LAND & PROPERTY</div>
        <div class="text-[0.65rem] uppercase tracking-[3px]">Acquisition, Investment, Development</div>
    </header>
    <div class="z-10 px-6 text-center">
        <h1 class="text-7xl font-serif font-bold mb-2">Precision Acquisition.</h1>
        <p class="text-[0.9rem] uppercase tracking-[6px] mb-12 font-300">The Gold Standard in Utah Land Asset Strategy.</p>
        <div class="action-bar mx-auto">
            <input type="password" id="main-search" class="action-input" placeholder="Enter Acquisition ID...">
            <button onclick="handleLogin()" class="action-button">Enter Vault</button>
        </div>
    </div>
    <p class="mt-6 disclaimer">Notice: Utah Land & Property Inc. is a private investment firm and is not a licensed Real Estate Broker or Agent.</p>
    <p class="mt-6 disclaimer">We do not represent third parties in the sale or purchase of real estate.</p>
</section>

<section id="dashboard-view" class="min-h-screen bg-[#FDFDFD] pb-24">
    <div class="max-w-7xl mx-auto px-10 mt-16">
        <div class="flex justify-between mb-12 border-b pb-8">
            <div class="text-sm font-bold uppercase tracking-widest text-gray-400">Status: <span id="deal-status" class="text-bhhs-cabernet">Initial Review</span></div>
            <div class="flex gap-4">
                <button onclick="window.location.href='?action=upload'" class="bg-gray-100 px-6 py-2 text-xs font-bold uppercase">Upload Documents</button>
                <button onclick="window.location.href='?action=esign'" class="bg-[var(--bhhs-cabernet)] text-white px-6 py-2 text-xs font-bold uppercase">Request E-Sign</button>
            </div>
        </div>
        </div>
</section>
<script>
function handleLogin() {{
    const entered = document.getElementById('main-search').value;
    document.getElementById('hero-section').classList.add('fade-out-up');
    setTimeout(() => {{
        document.getElementById('hero-section').style.display = 'none';
        document.getElementById('dashboard-view').classList.add('visible');
    }}, 700);
}}
</script>
</body>
</html>
"""

# --- 3. RENDER & LISTEN ---
components.html(html_content, height=1000, scrolling=True)

# The logic listens for the URL changes triggered by the HTML buttons
params = st.query_params
if "action" in params:
    # This logic updates your JSON without changing your HTML styling
    if params["action"] == "upload":
        update_json("CURRENT_PARCEL_ID", "DOCS_UPLOADED")
    elif params["action"] == "esign":
        update_json("CURRENT_PARCEL_ID", "ESIGN_PENDING")
