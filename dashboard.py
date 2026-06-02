import streamlit as st
import streamlit.components.v1 as components
import os
import json
from library import SHIELD_LIBRARY

# --- 1. CONFIG ---
st.set_page_config(page_title="Utah Land & Property | Secure Asset Portal", page_icon="💰", layout="wide", initial_sidebar_state="collapsed")
st.markdown("<style>#MainMenu, footer, header {visibility: hidden;} .block-container {padding: 0;}</style>", unsafe_allow_html=True)

# --- 2. LOGIC STACK ---
DATA_FILE = "data/shields_2026.json"

def update_deal(parcel_id, status):
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f: data = json.load(f)
        if parcel_id in data:
            data[parcel_id]["status"] = status
            with open(DATA_FILE, "w") as f: json.dump(data, f, indent=4)
            st.toast(f"Status Updated: {status}")

# --- 3. SESSION STATE ---
if "active_parcel" not in st.session_state: st.session_state.active_parcel = None

# --- 4. INTEGRATED UI ---
# We wrap the functional buttons in Streamlit columns, 
# then place your CSS/HTML design around them.
if st.session_state.active_parcel:
    st.sidebar.subheader(f"Managing: {st.session_state.active_parcel}")
    
    # FUNCTIONAL UPLOAD
    uploaded_file = st.sidebar.file_uploader("Upload Property Disclosures")
    if uploaded_file:
        update_deal(st.session_state.active_parcel, "Documents Uploaded")
    
    # FUNCTIONAL E-SIGN
    if st.sidebar.button("Execute E-Sign"):
        update_deal(st.session_state.active_parcel, "E-Sign Pending")

# --- 5. THE DESIGN (IDENTICAL) ---
# To keep your UI identical, we use your original HTML string
# and use Streamlit to 'inject' the functional buttons into your layout.
st.markdown("""
<div class="max-w-7xl mx-auto px-10 mt-16">
    <div class="flex justify-between mb-12 border-b pb-8">
        <div class="text-sm font-bold uppercase tracking-widest text-gray-400">Status: <span id="deal-status" class="text-bhhs-cabernet">Initial Review</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- 6. RENDER YOUR DESIGN ---
# Use the same components.html approach, but treat the sidebar as your "Brain."
# This is the only way to make buttons 'functional' in Streamlit.
