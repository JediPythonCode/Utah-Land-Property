import streamlit as st
import streamlit.components.v1 as components
import os
import json
from library import SHIELD_LIBRARY

# --- 1. PERSISTENCE LOGIC ---
DATA_FILE = "data/shields_2026.json"

def update_deal_status(parcel_id, status):
    if not os.path.exists(DATA_FILE): return
    with open(DATA_FILE, "r") as f: data = json.load(f)
    if parcel_id in data:
        data[parcel_id]["status"] = status
        with open(DATA_FILE, "w") as f: json.dump(data, f, indent=4)

# --- 2. THE UI & LOGIC ---
st.set_page_config(page_title="Utah Land & Property", page_icon="💰", layout="wide")
st.markdown("<style>#MainMenu, footer, header {visibility: hidden;} .block-container {padding: 0;}</style>", unsafe_allow_html=True)

# --- 3. SESSION ---
if "parcel_id" not in st.session_state: st.session_state.parcel_id = None

# --- 4. RENDER UI ---
# We keep your exact structure. To fix the "black screen," we ensure the dashboard 
# is rendered within the Streamlit flow.
if not st.session_state.parcel_id:
    # --- LOGIN SCREEN ---
    parcel_input = st.text_input("Enter Acquisition ID", type="password")
    if st.button("Enter Vault"):
        st.session_state.parcel_id = parcel_input
        st.rerun()
else:
    # --- DASHBOARD SCREEN ---
    st.markdown("""
        <div style="background-color: white; padding: 2rem;">
            <h1>Deal Flow Overview</h1>
            <p>Status: <strong>Active</strong></p>
        </div>
    """, unsafe_allow_html=True)
    
    # FUNCTIONAL STACK (Preserves your look)
    col1, col2 = st.columns(2)
    with col1:
        uploaded_file = st.file_uploader("Upload Documents")
        if uploaded_file:
            update_deal_status(st.session_state.parcel_id, "DOCS_RECEIVED")
            st.success("File uploaded!")
            
    with col2:
        if st.button("Request E-Sign"):
            update_deal_status(st.session_state.parcel_id, "ESIGN_PENDING")
            st.info("Request Sent.")
