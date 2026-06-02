import streamlit as st
import streamlit.components.v1 as components
import os
import json
from library import SHIELD_LIBRARY
from automation_engine import generate_utah_addendum

# --- 1. PERSISTENCE LAYER ---
DATA_FILE = "data/shields_2026.json"

def get_deal_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def update_deal(parcel_id, key, value):
    data = get_deal_data()
    if parcel_id in data:
        data[parcel_id][key] = value
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

# --- 2. PAGE SETUP ---
st.set_page_config(page_title="Utah Land & Property | Secure Asset Portal", page_icon="💰", layout="wide", initial_sidebar_state="collapsed")
st.markdown("<style>#MainMenu, footer, header {visibility: hidden;} .block-container {padding: 0;}</style>", unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if "active_parcel" not in st.session_state: st.session_state.active_parcel = None

# --- 4. DATA FETCHING ---
deal_status = "Initial Review"
if st.session_state.active_parcel:
    deal = get_deal_data().get(st.session_state.active_parcel, {})
    deal_status = deal.get("status", "Initial Review")

# --- 5. THE PORTAL INTERFACE ---
# Your original design + the dynamic Status Bridge
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<script src="https://cdn.tailwindcss.com"></script>
<style>
:root {{ --bhhs-cabernet: #631D33; }}
.hero-container {{ position:relative; height:100vh; background-image: linear-gradient(rgba(0,0,0,0.45), rgba(0,0,0,0.45)), url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&q=80&w=2070'); background-size:cover; background-position:center; display:flex; flex-direction:column; align-items:center; justify-content:center; color:white; }}
.visible {{ display:block !important; }}
</style>
</head>
<body>
    <section id="hero-section" class="hero-container">
        <div class="text-center">
            <h1 class="text-7xl font-serif font-bold">Precision Acquisition.</h1>
            <input type="text" id="id-input" class="text-black p-4 mt-8" placeholder="Enter Acquisition ID...">
            <button onclick="parent.postMessage(document.getElementById('id-input').value, '*')" class="bg-[#631D33] px-10 py-3 mt-4 text-white uppercase font-bold">Enter Vault</button>
        </div>
    </section>
    <section id="dashboard-view" class="p-16">
        <div class="max-w-7xl mx-auto glass-card p-12">
            <h2 class="text-3xl font-serif mb-8">Status: <span class="text-[#631D33]">{deal_status}</span></h2>
            <div class="border-2 border-dashed p-10 text-center">Drag & Drop Documents</div>
        </div>
    </section>
</body>
</html>
"""

components.html(html_content, height=1000)

# --- 6. LOGIC STACK (Backend Handler) ---
# This manages the data updates based on actions
with st.sidebar:
    st.subheader("Transaction Management")
    uploaded_file = st.file_uploader("Upload Signed Docs")
    if uploaded_file:
        update_deal(st.session_state.active_parcel, "status", "Documents Uploaded")
        st.success("Status Updated: Documents Uploaded")
        st.rerun()

    if st.button("Request E-Sign"):
        update_deal(st.session_state.active_parcel, "status", "E-Sign Pending")
        st.rerun()
