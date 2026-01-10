import streamlit as st
from streamlit_autorefresh import st_autorefresh
import os
import glob
from datetime import datetime

# ── 1. CONFIG & AUTO-REFRESH ───────────────────────────────────────────────
st.set_page_config(
    page_title="Utah Land & Property",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Gentle refresh (every 10 min)
st_autorefresh(interval=600000, key="ulp_refresh")

# ── 2. AUTHENTICATION GATE ──────────────────────────────────────────────────
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    # --- YOUR LOCK SCREEN CSS/HTML ---
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&family=Oswald:wght@500;700&display=swap');
        .stApp { background-color: #f8f9fa !important; }
        header, footer, [data-testid="stHeader"] { display: none !important; }
        .brand-title { font-family: 'Inter', sans-serif; font-size: clamp(42px, 10vw, 78px); font-weight: 900; color: #1a3c6d; letter-spacing: -1.5px; text-align: center; margin: 0.4em 0 0.1em; }
        .brand-subtitle { font-family: 'Oswald', sans-serif; font-size: 1.35rem; color: #6b7280; text-align: center; letter-spacing: 3px; font-weight: 500; margin-bottom: 2.5rem; }
        .privacy-notice { text-align: center; color: #4b5563; font-size: 0.95rem; max-width: 640px; margin: 0 auto 2.5rem; line-height: 1.6; }
        .lock-container { max-width: 480px; margin: 0 auto; padding: 2.5rem 1.5rem; background: white; border-radius: 12px; box-shadow: 0 10px 35px rgba(0,0,0,0.08); border: 1px solid #e5e7eb; }
        .pulse-lock { height: 12px; width: 12px; background: #10b981; border-radius: 50%; display: inline-block; margin-right: 10px; box-shadow: 0 0 12px rgba(16,185,129,0.5); animation: pulse 2s infinite; }
        @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(16,185,129,0.7); } 70% { box-shadow: 0 0 0 12px rgba(16,185,129,0); } 100% { box-shadow: 0 0 0 0 rgba(16,185,129,0); } }
    </style>
    <div style="padding: 12vh 5% 4vh;">
        <div class="brand-title">Utah Land & Property</div>
        <div class="brand-subtitle">Strategic Asset Framework</div>
        <div class="privacy-notice">
            Asset Protection • Privacy Preservation • Creative Land Financing Solutions<br><br>
            <strong>Secure Client Portal</strong> — Encrypted access only.
        </div>
        <div class="lock-container">
            <div style="text-align:center; margin-bottom:1.8rem;">
                <span class="pulse-lock"></span>
                <span style="font-family:Oswald; color:#1a3c6d; font-weight:700; letter-spacing:1.5px;">CLIENT SECURE ACCESS</span>
            </div>
    """, unsafe_allow_html=True)

    pwd = st.text_input("Access Key", type="password", placeholder="Enter private key", label_visibility="collapsed")

    if st.button("Access Secure Area", use_container_width=True, type="primary"):
        passwords = st.secrets.get("PASSWORDS", {})
        if pwd in [passwords.get("CLIENT", "default123"), passwords.get("ADMIN", "admin999")]:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Invalid key — access denied.")
    st.markdown("</div></div>", unsafe_allow_html=True)
    st.stop()

# ── LOGOUT BUTTON (Optional) ────────────────────────────────────────────────
with st.sidebar:
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()

# ── 3. MAIN APP — AUTHENTICATED ─────────────────────────────────────────────
# (Continue with the rest of your UI code here...)
