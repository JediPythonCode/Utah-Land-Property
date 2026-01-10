import streamlit as st
from streamlit_autorefresh import st_autorefresh
import os
import glob
import pandas as pd
from datetime import datetime
from cryptography.fernet import Fernet

# ── 1. CONFIG & ENCRYPTION ──────────────────────────────────────────────────
st.set_page_config(page_title="Utah Land & Property", layout="wide", initial_sidebar_state="collapsed")
st_autorefresh(interval=600000, key="ulp_refresh")

# Initialize Encryption logic
if "secret_key" not in st.secrets:
    # Fallback for local dev; in production, use the key from your secrets dashboard
    ENCR_KEY = b'6_Wb7R-5N5_W_h_Z9F-4Qp3o9-G7_X_z1H-8I_w_9k0=' 
else:
    ENCR_KEY = st.secrets["secret_key"].encode()

fernet = Fernet(ENCR_KEY)

# ── 2. BRANDING & STYLING (GLOBAL) ──────────────────────────────────────────
# We place this OUTSIDE the auth logic so it never disappears.
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&family=Oswald:wght@500;700&display=swap');
        
        .stApp { background-color: #f8f9fa !important; }
        header, footer, [data-testid="stHeader"] { display: none !important; }
        
        .viewport-top-container { 
            display: flex; flex-direction: column; justify-content: center; 
            align-items: center; min-height: 40vh; padding-top: 50px; 
            text-align: center; width: 100%; 
        }
        
        .brand-title { 
            font-family: 'Inter', sans-serif !important; font-size: clamp(38px, 8vw, 78px) !important; 
            font-weight: 900 !important; color: #1a3c6d !important; letter-spacing: -1.5px !important; 
            margin-bottom: 0px !important; line-height: 1.0 !important; 
        }
        
        .brand-subtitle { 
            font-family: 'Oswald', sans-serif !important; font-size: clamp(1rem, 3vw, 1.35rem) !important; 
            color: #6b7280 !important; letter-spacing: 3px !important; font-weight: 500 !important; 
            margin-top: 10px !important; margin-bottom: 1.5rem !important; 
        }
        
        .framework-text { 
            color: #4b5563 !important; font-size: 1.05rem !important; max-width: 800px !important; 
            margin: 0 auto 2rem !important; line-height: 1.7 !important; font-family: 'Inter', sans-serif !important; 
        }

        .pulse-lock { 
            height: 12px; width: 12px; background: #10b981; border-radius: 50%; 
            display: inline-block; margin-right: 12px; 
            box-shadow: 0 0 12px rgba(16,185,129,0.5); animation: pulse 2s infinite; 
        }
        
        @keyframes pulse { 
            0% { box-shadow: 0 0 0 0 rgba(16,185,129,0.7); } 
            70% { box-shadow: 0 0 0 12px rgba(16,185,129,0); } 
            100% { box-shadow: 0 0 0 0 rgba(16,185,129,0); } 
        }
        
        .access-text { 
            font-family: 'Oswald', sans-serif !important; font-size: 0.9rem !important; 
            color: #1a3c6d !important; font-weight: 700 !important; letter-spacing: 2px !important; 
        }
    </style>
""", unsafe_allow_html=True)

# ── 3. CORE LOGIC ────────────────────────────────────────────────────────────
# [Keep your save_encrypted, read_encrypted, and logger functions here...]

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# ── 4. THE UI FLOW ───────────────────────────────────────────────────────────
if not st.session_state.authenticated:
    # LOGIN SCREEN (STYLING PRESERVED)
    st.markdown("""
        <div class="viewport-top-container">
            <div class="brand-title">Utah Land & Property</div>
            <div class="brand-subtitle">Strategic Asset Protection Framework</div>
            <div class="framework-text">
                <strong>Privacy Creation Preservation • Creative Land & Real Estate Deal Structure</strong>
            </div>
            <div style="margin-bottom: 2rem;">
                <span class="pulse-lock"></span>
                <span class="access-text">SECURE CLIENT PORTAL ENCRYPTED ACCESS ONLY</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    _, col_mid, _ = st.columns([1, 1.6, 1])
    with col_mid:
        user_id = st.text_input("User ID", placeholder="Username", label_visibility="collapsed")
        pwd = st.text_input("Key", type="password", placeholder="Access Key", label_visibility="collapsed")
        
        if st.button("Access Portal", use_container_width=True, type="primary"):
            users = st.secrets.get("users", {})
            if user_id in users and str(users[user_id]["key"]) == pwd:
                st.session_state.authenticated = True
                st.session_state.user_id = user_id
                st.session_state.user_role = users[user_id]["role"]
                st.rerun()
            else:
                st.error("Access Denied: Invalid Credentials")

else:
    # ── 5. AUTHENTICATED DASHBOARD ──────────────────────────────────────────
    # [Your Admin/Buyer logic goes here...]
    st.title(f"{st.session_state.user_role} Portal")
    if st.button("Secure Logout"):
        st.session_state.authenticated = False
        st.rerun()
