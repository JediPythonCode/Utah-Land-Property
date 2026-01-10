import streamlit as st
from streamlit_autorefresh import st_autorefresh
import os
import json
import pandas as pd
from datetime import datetime
from cryptography.fernet import Fernet

# ── 1. CONFIG & SECURE ENCRYPTION ─────────────────────────────────────────────
st.set_page_config(
    page_title="Utah Land & Property", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

STAGES = ["Application", "Processing", "Underwriting", "Approved", "Closed"]

# Live heartbeat refresh (10 seconds)
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

# ── 2. CORE CSS (MIMICKING QXTRADE TERMINAL) ──────────────────────────────────
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@900&family=Oswald:wght@700&display=swap');
        
        /* Layout Resets */
        .stApp { background-color: #FFFFFF !important; }
        header, [data-testid="stHeader"] { display: none !important; }
        .block-container { padding-top: 2rem !important; }

        /* Massive Terminal Typography */
        .ulp-terminal-title { 
            font-family: "Inter", sans-serif; 
            font-size: clamp(32px, 12vw, 85px); 
            font-weight: 900; 
            color: #1a3c6d; 
            letter-spacing: -4px; 
            line-height: 0.85; 
            text-align: center; 
            text-transform: uppercase;
            margin-bottom: 10px;
        }

        /* Pulse Sync Box */
        .sync-box { text-align: center; margin-bottom: 30px; }
        .pulse-dot { 
            height: 10px; width: 10px; background-color: #00ff41; 
            border-radius: 50%; display: inline-block; margin-right: 8px; 
            box-shadow: 0 0 12px #00ff41; animation: pulse-green 1.5s infinite; 
        }
        @keyframes pulse-green { 
            0% { box-shadow: 0 0 0px 0px rgba(0, 255, 65, 0.7); } 
            70% { box-shadow: 0 0 0px 10px rgba(0, 255, 65, 0); } 
            100% { box-shadow: 0 0 0px 0px rgba(0, 255, 65, 0); } 
        }
        .sync-label { 
            font-family: "Oswald", sans-serif; font-size: 14px; 
            color: #1a3c6d; letter-spacing: 3px; font-weight: bold; 
        }

        /* Bento Card Styling */
        .bento-card {
            background: #f8fafc; border: 1px solid #e2e8f0;
            padding: 24px; border-radius: 16px; margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        }
        
        /* Tab Navigation */
        .stTabs [data-baseweb="tab-list"] { gap: 10px; justify-content: center; }
        .stTabs [data-baseweb="tab"] {
            font-family: 'Oswald', sans-serif; background-color: #f1f5f9;
            padding: 10px 25px; border-radius: 8px 8px 0 0;
        }
        .stTabs [aria-selected="true"] { background-color: #1a3c6d !important; color: white !important; }
    </style>
""", unsafe_allow_html=True)

# ── 3. AUTHENTICATION GATE ────────────────────────────────────────────────────
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown(f'''
    <div style="padding: 10vh 5% 0 5%; text-align: center;">
        <div style="font-size: 60px; margin-bottom: 10px;">🔐</div>
        <div class="ulp-terminal-title">Utah Land<br>& Property</div>
        <div class="sync-box">
            <span class="pulse-dot"></span>
            <span class="sync-label">SECURE ENTRY POINT</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    _, col_mid, _ = st.columns([1, 4, 1])
    with col_mid:
        with st.container(border=True):
            u_id_input = st.text_input("ID", placeholder="ENTER ACCESS ID", label_visibility="collapsed").strip().lower()
            u_pwd_input = st.text_input("KEY", type="password", placeholder="ENTER PRIVATE KEY", label_visibility="collapsed").strip()
            if st.button("CONTINUE TO TERMINAL", use_container_width=True):
                if u_id_input in USER_DB and str(USER_DB[u_id_input].get("key")) == u_pwd_input:
                    st.session_state.authenticated = True
                    st.session_state.user_id = u_id_input
                    st.session_state.user_role = USER_DB[u_id_input].get("role", "Buyer")
                    st.rerun()
                else:
                    st.error("ACCESS DENIED")
    st.stop()

# ── 4. LOGIC ENGINE ───────────────────────────────────────────────────────────
VAULT_BASE = "vault"
for folder in ["general", "buyer_docs", "admin_inbox", "pipeline"]:
    os.makedirs(os.path.join(VAULT_BASE, folder), exist_ok=True)

def save_encrypted(file_path, data):
    with open(file_path, "wb") as f: f.write(fernet.encrypt(data))

def read_encrypted(file_path):
    try:
        with open(file_path, "rb") as f: return fernet.decrypt(f.read())
    except: return None

def get_pipeline(u_id):
    path = os.path.join(VAULT_BASE, "pipeline", f"{u_id}.json")
    if os.path.exists(path):
        with open(path, "r") as f: return json.load(f).get("stage", STAGES[0])
    return STAGES[0]

def update_pipeline(u_id, stage):
    path = os.path.join(VAULT_BASE, "pipeline", f"{u_id}.json")
    with open(path, "w") as f:
        json.dump({"stage": stage, "updated": str(datetime.now())}, f)

# ── 5. TERMINAL HEADER ────────────────────────────────────────────────────────
role, u_id = st.session_state.user_role, st.session_state.user_id

st.markdown(f'''
    <div style="text-align: center;">
        <h1 class="ulp-terminal-title">Utah Land & Property</h1>
        <div class="sync-box">
            <span class="pulse-dot"></span>
            <span class="sync-label">STATION SYNC: {datetime.now().strftime("%H:%M:%S")} | {u_id.upper()}</span>
        </div>
    </div>
''', unsafe_allow_html=True)

# ── 6. ROLE INTERFACES ────────────────────────────────────────────────────────
if role == "Admin":
    t1, t2, t3 = st.tabs(["PIPELINE CONTROL", "VAULT INBOX", "AUDIT LOG"])
    
    with t1:
        st.subheader("Transaction Pipeline")
        buyers = [u for u in USER_DB if USER_DB[u]['role'] == 'Buyer']
        for buyer in buyers:
            with st.container(border=True):
                c1, c2, c3 = st.columns([1, 2, 1])
                c1.write(f"**{buyer.upper()}**")
                curr = get_pipeline(buyer)
                stage = c2.selectbox("Update Stage", STAGES, index=STAGES.index(curr), key=f"p_{buyer}")
                if c3.button("Push Update", key=f"b_{buyer}"):
                    update_pipeline(buyer, stage)
                    st.toast(f"Updated {buyer}")

    with t2:
        st.subheader("Admin Inbox")
        inbox_dir = os.path.join(VAULT_BASE, "admin_inbox")
        files = os.listdir(inbox_dir)
        if files:
            for f in files:
                data = read_encrypted(os.path.join(inbox_dir, f))
                if data: st.download_button(f"Decrypt & Review: {f}", data, file_name=f)
        else:
            st.info("No documents in inbox.")

elif role == "Buyer":
    current_stage = get_pipeline(u_id)
    
    # 2026 Progress Tracker
    cols = st.columns(len(STAGES))
    for i, s in enumerate(STAGES):
        active = STAGES.index(current_stage) >= i
        color = "#1a3c6d" if active else "#cbd5e1"
        cols[i].markdown(f"<p style='text-align:center; color:{color}; font-size:0.75rem;'>{'✅' if active else '○'}<br><b>{s.upper()}</b></p>", unsafe_allow_html=True)
    st.progress(STAGES.index(current_stage) / (len(STAGES)-1))

    st.markdown("<br>", unsafe_allow_html=True)
    col_l, col_r = st.columns([1.5, 1])

    with col_l:
        st.markdown('<div class="bento-card"><h3>Secure Document Vault</h3>', unsafe_allow_html=True)
        doc_dir = os.path.join(VAULT_BASE, "buyer_docs")
        user_docs = [f for f in os.listdir(doc_dir) if f.startswith(f"ENCR_{u_id}_")]
        if user_docs:
            for d in user_docs:
                data = read_encrypted(os.path.join(doc_dir, d))
                if data: st.download_button(f"📥 DOWNLOAD: {d.replace(f'ENCR_{u_id}_', '')}", data, key=d)
        else:
            st.write("Your secure vault is currently empty.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="bento-card"><h3>Submit Documents</h3>', unsafe_allow_html=True)
        up = st.file_uploader("Upload", label_visibility="collapsed")
        if st.button("TRANSMIT TO AGENT", use_container_width=True) and up:
            save_encrypted(os.path.join(VAULT_BASE, "admin_inbox", f"FROM_{u_id}_{up.name}"), up.getvalue())
            st.success("Securely Transmitted.")
        st.markdown('</div>', unsafe_allow_html=True)

# ── 7. PRODUCTION FOOTER ──────────────────────────────────────────────────────
st.markdown(f"""
    <br><hr>
    <div style="display: flex; justify-content: center; gap: 30px; opacity: 0.8; font-size: 11px; font-family: 'Oswald'; color: #1a3c6d;">
        <div style="display: flex; align-items: center;"><span class="green-pulse" style="height:6px; width:6px; margin-right:5px;"></span>SYSTEM: ENCRYPTED NODE</div>
        <div>STATION: LOCAL_SYNC</div>
        <div style="font-weight: bold;">© 2026 UTAH LAND & PROPERTY | TRANSACTION TERMINAL</div>
    </div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown(f"**Operator:** {u_id.upper()}")
    if st.button("TERMINAL LOGOUT"):
        st.session_state.authenticated = False
        st.rerun()
