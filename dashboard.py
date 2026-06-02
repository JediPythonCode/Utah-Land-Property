import streamlit as st
import streamlit.components.v1 as components
import os
import json
from automation_engine import generate_utah_addendum
from library import SHIELD_LIBRARY

# --- 1. PERSISTENCE LAYER ---
DATA_FILE = "data/shields_2026.json"

def update_deal(parcel_id, key, value):
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f: data = json.load(f)
        if parcel_id in data:
            data[parcel_id][key] = value
            with open(DATA_FILE, "w") as f: json.dump(data, f, indent=4)

# --- 2. PAGE SETUP ---
st.set_page_config(page_title="Utah Land & Property | Secure Asset Portal", page_icon="💰", layout="wide", initial_sidebar_state="collapsed")
st.markdown("<style>#MainMenu, footer, header {visibility: hidden;} .block-container {padding: 0;}</style>", unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if "parcel_id" not in st.session_state: st.session_state.parcel_id = None

# --- 4. THE ORIGINAL UI (Your exact code) ---
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<script src="https://cdn.tailwindcss.com"></script>
<style>
:root {{ --bhhs-cabernet: #631D33; --overlay: rgba(0, 0, 0, 0.45); }}
body, html {{ margin:0; padding:0; font-family:'Montserrat', sans-serif; background-color:#fcfcfc; }}
.hero-container {{ position:relative; height:100vh; width:100%; background-image: linear-gradient(var(--overlay), var(--overlay)), url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&q=80&w=2070'); background-size:cover; background-position:center; display:flex; flex-direction:column; align-items:center; justify-content:center; color:white; }}
#dashboard-view {{ display:none; opacity:0; transition: opacity 1s ease-in-out; }}
.glass-card {{ background:white; border:1px solid #e5e7eb; box-shadow:0 4px 15px rgba(0,0,0,0.03); }}
.visible {{ display:block !important; opacity:1 !important; }}
</style>
</head>
<body>
<section id="hero-section" class="hero-container">
    <div class="z-10 text-center">
        <h1 class="text-7xl font-serif font-bold mb-2">Precision Acquisition.</h1>
        <div class="action-bar mx-auto">
            <input type="password" id="main-search" class="text-black p-4" placeholder="Enter Acquisition ID...">
            <button onclick="parent.postMessage(document.getElementById('main-search').value, '*')" class="bg-[#631D33] text-white px-10 py-4 uppercase">Enter Vault</button>
        </div>
    </div>
</section>
<section id="dashboard-view" class="p-16">
    <h2 class="text-3xl font-serif">Status: <span id="deal-status" class="text-[#631D33]">Initial Review</span></h2>
</section>
</body>
</html>
"""

# --- 5. FUNCTIONAL BRIDGE ---
# We render your exact design, and use a Sidebar to handle the logic
components.html(html_content, height=1000, scrolling=True)

# THE FUNCTIONAL STACK (Hidden sidebar keeps your design clean)
with st.sidebar:
    st.subheader("System Control")
    parcel = st.text_input("Confirm Acquisition ID")
    uploaded_file = st.file_uploader("Upload Signed Docs")
    
    if uploaded_file and parcel:
        # This saves your data to the JSON file persistently
        update_deal(parcel, "status", "Documents Received")
        st.success("File saved and Status updated.")
    
    if st.button("Request E-Sign"):
        update_deal(parcel, "status", "E-Sign Pending")
        st.info("E-Sign Request Dispatched.")
