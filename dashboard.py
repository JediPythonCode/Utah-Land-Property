import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import pandas as pd

# --- SAFE IMPORT LOGIC ---
try:
    from library import SHIELD_LIBRARY
except ImportError:
    SHIELD_LIBRARY = {"Error": "library.py not found in root directory"}

# 1. INSTITUTIONAL CONFIG
st.set_page_config(
    page_title="Utah Land & Property | Secure Asset Portal",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. BRANDING & UI OVERRIDE
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {padding: 0;}
        [data-testid="stAppViewContainer"] { background-color: #fcfcfc; }
        .stMultiSelect [data-baseweb="tag"] { background-color: #631D33 !important; }
        .stButton>button { 
            background-color: #631D33; color: white; border-radius: 0px; 
            border: none; text-transform: uppercase; letter-spacing: 2px; width: 100%;
            height: 3rem; font-weight: 600;
        }
    </style>
""", unsafe_allow_html=True)

if 'vault_access' not in st.session_state:
    st.session_state.vault_access = False

# 3. THE FRONT DOOR (Minimal HTML for stability)
html_hero = """
<div style="height:100vh; display:flex; align-items:center; justify-content:center; background:#631D33; color:white; font-family:serif;">
    <div style="text-align:center;">
        <h1>UTAH LAND & PROPERTY</h1>
        <p>SECURE ASSET PORTFOLIO</p>
        <button onclick="parent.window.location.reload()" style="padding:10px 20px; cursor:pointer;">RELOAD SYSTEM</button>
    </div>
</div>
"""

# Admin Toggle in Sidebar to bypass the error
with st.sidebar:
    st.write("System Status")
    if st.button("Unlock Vault Manually"):
        st.session_state.vault_access = True

if not st.session_state.vault_access:
    st.markdown("### Vault Locked")
    st.info("Use the sidebar toggle to bypass the hero screen for testing.")
    components.html(html_hero, height=600)
else:
    st.title("PRIVATE CLIENT PORTFOLIO")
    st.write("Stochastic Model: **ACTIVE**")
    
    # Shield Selector from Library
    selected = st.multiselect("Select Active Shields:", options=list(SHIELD_LIBRARY.keys()))
    
    if st.button("Generate Test Addendum"):
        st.success("Logic Stacked Successfully.")
