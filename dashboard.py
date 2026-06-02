import streamlit as st
import os
import json
from library import SHIELD_LIBRARY

# --- 1. CONFIG ---
st.set_page_config(page_title="Utah Land & Property | Secure Asset Portal", page_icon="💰", layout="wide")
st.markdown("""
    <style>
        #MainMenu, footer, header {visibility: hidden;}
        .block-container {padding: 0 !important;}
        :root { --bhhs-cabernet: #631D33; }
        .hero-container { position:relative; height:100vh; width:100%; background-image: linear-gradient(rgba(0,0,0,0.45), rgba(0,0,0,0.45)), url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&q=80&w=2070'); background-size:cover; }
    </style>
""", unsafe_allow_html=True)

# --- 2. PERSISTENCE ---
def update_json(parcel_id, status):
    path = "data/shields_2026.json"
    if os.path.exists(path):
        with open(path, "r") as f: data = json.load(f)
        if parcel_id in data:
            data[parcel_id]["status"] = status
            with open(path, "w") as f: json.dump(data, f, indent=4)

# --- 3. UI LAYER ---
# Instead of components.html, we use st.markdown to inject the code.
# This avoids the "black screen" sandbox issue.
st.markdown("""
<section class="hero-container flex flex-col items-center justify-center text-white">
    <h1 class="text-7xl font-serif font-bold mb-2">Precision Acquisition.</h1>
    <p class="uppercase tracking-[6px] mb-12">The Gold Standard in Utah Land Asset Strategy.</p>
</section>
""", unsafe_allow_html=True)

# --- 4. FUNCTIONAL LOGIC ---
# Now that the UI is rendered by Streamlit, these will work perfectly:
parcel = st.text_input("Enter Acquisition ID")
if parcel:
    st.success(f"Vault Accessed: {parcel}")
    col1, col2 = st.columns(2)
    
    with col1:
        file = st.file_uploader("Upload Documents")
        if file:
            update_json(parcel, "DOCS_RECEIVED")
    
    with col2:
        if st.button("Request E-Sign"):
            update_json(parcel, "ESIGN_PENDING")
            st.info("E-Sign Request Dispatched.")
