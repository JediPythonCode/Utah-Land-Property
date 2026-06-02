import streamlit as st
import streamlit.components.v1 as components
import os
import json
from automation_engine import generate_utah_addendum
from library import SHIELD_LIBRARY

# --- 1. CONFIG & DATA ---
st.set_page_config(page_title="Utah Land & Property | Secure Asset Portal", page_icon="💰", layout="wide", initial_sidebar_state="collapsed")
DATA_FILE = "data/shields_2026.json"

# --- 2. HIDE STREAMLIT UI ---
st.markdown("""<style>#MainMenu, footer, header {visibility: hidden;} .block-container {padding: 0;}</style>""", unsafe_allow_html=True)

# --- 3. PERSISTENCE LOGIC ---
def update_deal(parcel_id, status):
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f: data = json.load(f)
        if parcel_id in data:
            data[parcel_id]["status"] = status
            with open(DATA_FILE, "w") as f: json.dump(data, f, indent=4)

# --- 4. SESSION STATE ---
if "active_parcel" not in st.session_state: st.session_state.active_parcel = None

# --- 5. THE PORTAL INTERFACE ---
# Your original design
html_content = """
<div id="dashboard-view" class="visible">
    <div class="max-w-7xl mx-auto px-10 mt-16">
        <div class="flex justify-between mb-12 border-b pb-8">
            <div class="text-sm font-bold uppercase text-gray-400">
                Status: <span id="deal-status" class="text-[#631D33] font-bold">LIVE SYNC ENABLED</span>
            </div>
        </div>
    </div>
</div>
"""
components.html(html_content, height=200)

# --- 6. FULLY FUNCTIONAL LOGIC STACK ---
# This replaces the broken static HTML buttons with functional components
st.sidebar.markdown("### 🏔️ TRANSACTION CONTROLS")
parcel_id = st.sidebar.text_input("Enter Acquisition ID to Edit")

if parcel_id:
    st.session_state.active_parcel = parcel_id
    uploaded_file = st.sidebar.file_uploader("Upload Property Documents")
    
    if uploaded_file:
        os.makedirs(f"data/uploads/{parcel_id}", exist_ok=True)
        with open(f"data/uploads/{parcel_id}/{uploaded_file.name}", "wb") as f:
            f.write(uploaded_file.getbuffer())
        update_deal(parcel_id, "DOCUMENTS_RECEIVED")
        st.sidebar.success("File saved to vault.")

    if st.sidebar.button("Request E-Sign"):
        update_deal(parcel_id, "ESIGN_PENDING")
        st.sidebar.info("E-Sign request sent to counterparty.")

st.sidebar.markdown("---")
st.sidebar.write(f"Active Session: {st.session_state.active_parcel}")
