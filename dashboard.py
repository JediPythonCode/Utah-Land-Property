import streamlit as st
from streamlit_autorefresh import st_autorefresh
import os
import json
import pandas as pd
from datetime import datetime
from cryptography.fernet import Fernet

# ── 1. CONFIG & REFRESH ──────────────────────────────────────────────────────
st.set_page_config(page_title="Utah Land & Property | Terminal", layout="wide", initial_sidebar_state="collapsed")
st_autorefresh(interval=10000, key="ulp_live_ping")

def initialize_system():
    try:
        key = st.secrets.get("secret_key")
        users_data = st.secrets.get("users")
        if not key or users_data is None:
            st.error("🚨 SYSTEM ERROR: secrets.toml missing 'secret_key' or '[users]'.")
            st.stop()
        return Fernet(key.encode()), dict(users_data)
    except Exception as e:
        st.error(f"🚨 SYSTEM CRITICAL: Secrets unreachable. {e}")
        st.stop()

fernet, USER_DB = initialize_system()

# ── 2. THE QXTRADE ALPHA AUTHENTICATION ENGINE ──────────────────────────────
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown('''
    <style>
        @import url("https://fonts.googleapis.com/css2?family=Inter:wght@900&family=Oswald:wght@700&display=swap");
        
        .stApp { background-color: #FFFFFF !important; }
        header, footer, [data-testid="stHeader"] { display: none !important; }
        
        /* Massive Industrial Blue Title */
        .terminal-title-auth { 
            font-family: "Inter", sans-serif; 
            font-size: clamp(32px, 12vw, 80px); 
            font-weight: 900; 
            color: #1d428a; 
            letter-spacing: -4px; 
            line-height: 0.85; 
            margin-bottom: 20px; 
            text-align: center; 
            text-transform: uppercase;
        }
        
        /* Sync Pulse Box */
        .sync-box { text-align: center; margin-bottom: 30px; }
        .pulse-dot { 
            height: 12px; width: 12px; background-color: #00ff41; 
            border-radius: 50%; display: inline-block; margin-right: 8px; 
            box-shadow: 0 0 10px #00ff41; animation: pulse-green 1.5s infinite; 
        }
        @keyframes pulse-green { 
            0% { box-shadow: 0 0 0px 0px rgba(0, 255, 65, 0.7); } 
            70% { box-shadow: 0 0 0px 10px rgba(0, 255, 65, 0); } 
            100% { box-shadow: 0 0 0px 0px rgba(0, 255, 65, 0); } 
        }
        .sync-label { 
            font-family: "Oswald", sans-serif; font-size: 15px; 
            color: #1d428a; letter-spacing: 2px; font-weight: bold; 
        }

        /* QxTrade Gold Card Mimicry */
        .auth-container {
            background-color: #FDD017 !important; 
            background-image: url("https://www.transparenttextures.com/patterns/carbon-fibre.png") !important; 
            border-top: 8px solid #1a1a1a !important; 
            border-radius: 4px 25px 4px 25px !important; 
            padding: 50px !important;
            box-shadow: 0 15px 35px rgba(0,0,0,0.3) !important;
            text-align: center;
        }
        
        /* Terminal Button Styling */
        .stButton>button {
            background-color: #1a1a1a !important;
            color: #00ff41 !important;
            font-family: 'Oswald', sans-serif !important;
            border: 2px solid #00ff41 !important;
            letter-spacing: 2px !important;
            font-weight: bold !important;
            height: 50px !important;
            text-transform: uppercase !important;
        }
        
        /* Input Overrides */
        div[data-baseweb="input"] {
            background-color: white !important;
            border-radius: 4px !important;
        }
    </style>
    
    <div style="padding: 8vh 5% 5% 5%; text-align: center;">
        <div class="terminal-title-auth">Utah Land<br>& Property</div>
        <div class="sync-box">
            <span class="pulse-dot"></span>
            <span class="sync-label">SECURE TRANSACTION PORTAL</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    _, col_mid, _ = st.columns([1, 1.8, 1])
    with col_mid:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        u_id = st.text_input("ID", placeholder="ACCESS ID", label_visibility="collapsed").strip().lower()
        u_key = st.text_input("KEY", type="password", placeholder="PRIVATE SECURITY KEY", label_visibility="collapsed").strip()
        if st.button("AUTHENTICATE TERMINAL", use_container_width=True):
            if u_id in USER_DB and str(USER_DB[u_id].get("key")) == u_key:
                st.session_state.authenticated = True
                st.session_state.user_id = u_id
                st.session_state.user_role = USER_DB[u_id].get("role", "Buyer")
                st.rerun()
            else:
                st.error("ACCESS DENIED: INVALID CREDENTIALS")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ── 3. MAIN DASHBOARD CSS ──────────────────────────────────────────────────
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@900&family=Oswald:wght@700&display=swap');
        .stApp { background-color: #FFFFFF !important; }
        .main-title { 
            font-family: 'Inter', sans-serif; font-size: clamp(40px, 12vw, 85px) !important; 
            font-weight: 900 !important; color: #1d428a !important; letter-spacing: -4px; 
            line-height: 0.85; text-align: center; margin-bottom: 10px;
        }
        .intel-header { 
            background: linear-gradient(to right, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c) !important; 
            -webkit-background-clip: text !important; 
            -webkit-text-fill-color: transparent !important; 
            font-family: 'Inter', sans-serif !important; 
            font-weight: 900 !important; 
            font-size: clamp(30px, 8vw, 55px) !important; 
            text-align: center !important; 
            text-transform: uppercase;
            margin-top: -20px;
        }
        .bento-card {
            background: #f8fafc; border: 1px solid #e2e8f0;
            padding: 24px; border-radius: 16px; color: #1d428a;
        }
    </style>
""", unsafe_allow_html=True)

# ── 4. DASHBOARD HEADER ──────────────────────────────────────────────────────
role, u_id = st.session_state.user_role, st.session_state.user_id

st.markdown(f'''
    <div style="text-align: center;">
        <h1 class="main-title">Utah Land & Property</h1>
        <div class="sync-box">
            <span class="pulse-dot"></span>
            <span class="sync-label">STATION ACTIVE: {u_id.upper()} | {datetime.now().strftime("%H:%M:%S")}</span>
        </div>
    </div>
''', unsafe_allow_html=True)

st.markdown('<h1 class="intel-header">Asset Intelligence</h1>', unsafe_allow_html=True)

# ── 5. CORE SYSTEM LOGIC ───────────────────────────────────────────────────
VAULT_BASE = "vault"
for folder in ["general", "buyer_docs", "admin_inbox", "pipeline"]:
    os.makedirs(os.path.join(VAULT_BASE, folder), exist_ok=True)

def read_encrypted(file_path):
    try:
        with open(file_path, "rb") as f: return fernet.decrypt(f.read())
    except: return None

# ── 6. INTERFACE ─────────────────────────────────────────────────────────────
if role == "Buyer":
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown('<div class="bento-card"><h3>🔒 Secure Document Vault</h3>', unsafe_allow_html=True)
        # Logic to list encrypted documents here
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="bento-card"><h3>📤 Transmission Node</h3>', unsafe_allow_html=True)
        st.file_uploader("Upload to Utah Land & Property", label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

# ── 7. FOOTER ────────────────────────────────────────────────────────────────
st.markdown(f"""
    <br><hr>
    <div style="display: flex; justify-content: center; gap: 30px; opacity: 0.8; font-size: 11px; font-family: 'Oswald'; color: #1d428a;">
        <div style="display: flex; align-items: center;"><span class="pulse-dot" style="height:6px; width:6px; margin-right:5px;"></span>SYSTEM: ENCRYPTED</div>
        <div style="font-weight: bold;">© 2026 UTAH LAND & PROPERTY | TERMINAL V2.4</div>
    </div>
""", unsafe_allow_html=True)

with st.sidebar:
    if st.button("TERMINAL EXIT"):
        st.session_state.authenticated = False
        st.rerun()
