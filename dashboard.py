import streamlit as st
from streamlit_autorefresh import st_autorefresh
import os
import json
import pandas as pd
from datetime import datetime
from cryptography.fernet import Fernet

# ── 1. CONFIG & SECURE ENCRYPTION ─────────────────────────────────────────────
st.set_page_config(
    page_title="ULP | Secure Terminal",
    layout="wide",
    initial_sidebar_state="collapsed"
)

STAGES = ["Application", "Processing", "Underwriting", "Approved", "Closed"]

if "refresh_initialized" not in st.session_state:
    st_autorefresh(interval=600000, key="ulp_refresh")
    st.session_state.refresh_initialized = True

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

# ── 2. BRANDING & ADVANCED UI (TERMINAL STYLE) ────────────────────────────────
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=Oswald:wght@500;700&display=swap');
        
        /* Global Background & Reset */
        .stApp { background-color: #ffffff !important; }
        [data-testid="stHeader"] { display: none !important; }
        .block-container { padding-top: 2rem !important; }

        /* Typography */
        .ulp-title { 
            font-family: 'Inter', sans-serif; 
            font-size: clamp(35px, 8vw, 75px) !important; 
            font-weight: 900 !important; 
            color: #1a3c6d !important; 
            letter-spacing: -3px; 
            line-height: 0.85; 
            margin-bottom: 5px; 
            text-align: center; 
            text-transform: uppercase;
        }
        
        /* Status Pulse Indicator */
        .sync-container { text-align: center; margin-bottom: 30px; }
        .green-pulse { 
            height: 10px; width: 10px; background-color: #10b981; 
            border-radius: 50%; display: inline-block; margin-right: 8px; 
            box-shadow: 0 0 10px #10b981; animation: pulse-green 1.5s infinite; 
        }
        @keyframes pulse-green { 
            0% { box-shadow: 0 0 0px 0px rgba(16, 185, 129, 0.7); } 
            70% { box-shadow: 0 0 0px 10px rgba(16, 185, 129, 0); } 
            100% { box-shadow: 0 0 0px 0px rgba(16, 185, 129, 0); } 
        }
        .sync-text { 
            font-family: 'Oswald', sans-serif; font-size: 14px; 
            color: #64748b; letter-spacing: 2px; font-weight: bold;
        }

        /* Bento Cards */
        .bento-card {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            padding: 24px;
            border-radius: 16px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        }
        
        /* Tabs Styling */
        .stTabs [data-baseweb="tab-list"] { gap: 8px; justify-content: center; }
        .stTabs [data-baseweb="tab"] {
            font-family: 'Oswald', sans-serif; background-color: #f1f5f9;
            border-radius: 8px 8px 0 0; padding: 10px 20px;
        }
        .stTabs [aria-selected="true"] { background-color: #1a3c6d !important; color: white !important; }
    </style>
""", unsafe_allow_html=True)

# ── 3. CORE LOGIC & VAULT ─────────────────────────────────────────────────────
VAULT_BASE = "vault"
FOLDERS = ["general", "buyer_docs", "admin_inbox", "metadata", "pipeline"]
for folder in FOLDERS:
    os.makedirs(os.path.join(VAULT_BASE, folder), exist_ok=True)

def logger(user, action, details):
    try:
        path = os.path.join(VAULT_BASE, "general", "audit_log.csv")
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df = pd.DataFrame([[ts, user, action, str(details)]], columns=["Timestamp", "User", "Action", "Details"])
        df.to_csv(path, mode='a', header=not os.path.exists(path), index=False)
    except: pass

def save_encrypted(file_path, data, description=""):
    with open(file_path, "wb") as f: f.write(fernet.encrypt(data))
    meta_path = os.path.join(VAULT_BASE, "metadata", os.path.basename(file_path) + ".json")
    with open(meta_path, "w") as f:
        json.dump({"description": description, "timestamp": str(datetime.now())}, f)

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

# ── 4. AUTHENTICATION GATE ────────────────────────────────────────────────────
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown(f'''
    <div style="padding: 10vh 5% 0 5%; text-align: center;">
        <div class="ulp-title">Utah Land <br>& Property</div>
        <div class="sync-container">
            <span class="green-pulse"></span>
            <span class="sync-text">SECURE ACCESS POINT</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    _, col_mid, _ = st.columns([1, 1.2, 1])
    with col_mid:
        with st.container(border=True):
            u_id_input = st.text_input("ID", placeholder="USERNAME", label_visibility="collapsed").strip().lower()
            u_pwd_input = st.text_input("KEY", type="password", placeholder="PASSWORD", label_visibility="collapsed").strip()
            if st.button("AUTHENTICATE", use_container_width=True, type="primary"):
                if u_id_input in USER_DB and str(USER_DB[u_id_input].get("key")) == u_pwd_input:
                    st.session_state.authenticated = True
                    st.session_state.user_id = u_id_input
                    st.session_state.user_role = USER_DB[u_id_input].get("role", "Buyer")
                    logger(u_id_input, "Auth", "Success")
                    st.rerun()
                else:
                    st.error("INVALID CREDENTIALS")
    st.stop()

# ── 5. DASHBOARD HEADER ───────────────────────────────────────────────────────
role, u_id = st.session_state.user_role, st.session_state.user_id

st.markdown(f'''
    <div style="text-align: center; margin-top: -30px;">
        <h1 class="ulp-title">Utah Land & Property</h1>
        <div class="sync-container">
            <span class="green-pulse"></span>
            <span class="sync-text">STATION ACTIVE | {u_id.upper()} | {datetime.now().strftime("%H:%M:%S")}</span>
        </div>
    </div>
''', unsafe_allow_html=True)

st.sidebar.markdown(f"**Operator:** {u_id.upper()}")
st.sidebar.markdown(f"**Role:** {role}")
if st.sidebar.button("Terminal Logout"):
    st.session_state.authenticated = False
    st.rerun()

# ── 6. INTERFACE LOGIC ────────────────────────────────────────────────────────
if role == "Admin":
    t1, t2, t3, t4 = st.tabs(["PIPELINE", "DISTRIBUTION", "VAULT INBOX", "AUDIT LOG"])

    with t1:
        st.subheader("Deal-Flow Intelligence")
        buyers = [u for u in USER_DB if USER_DB[u]['role'] == 'Buyer']
        for buyer in buyers:
            col1, col2, col3 = st.columns([1, 2, 1])
            col1.write(f"**{buyer.upper()}**")
            current = get_pipeline(buyer)
            idx = STAGES.index(current) if current in STAGES else 0
            stage = col2.selectbox("Update Stage", STAGES, key=f"pipe_{buyer}", index=idx)
            if col3.button("Push", key=f"btn_{buyer}"):
                update_pipeline(buyer, stage)
                st.toast(f"Updated {buyer}")

    with t2:
        st.subheader("Secure Transmission")
        target = st.selectbox("Select Recipient", options=list(USER_DB.keys()))
        note = st.text_input("Transaction Note")
        files = st.file_uploader("Select Assets", accept_multiple_files=True)
        if st.button("ENCRYPT & SEND") and files:
            for f in files:
                path = os.path.join(VAULT_BASE, "buyer_docs", f"ENCR_{target}_{f.name}")
                save_encrypted(path, f.getvalue(), note)
            st.success("Assets Delivered.")

    with t3:
        st.subheader("Inbound Documents")
        inbox = os.path.join(VAULT_BASE, "admin_inbox")
        if os.path.exists(inbox):
            for b_file in os.listdir(inbox):
                with st.container(border=True):
                    st.write(f"📩 {b_file}")
                    data = read_encrypted(os.path.join(inbox, b_file))
                    if data: st.download_button("Decrypt & View", data, file_name=b_file, key=b_file)

    with t4:
        audit_path = os.path.join(VAULT_BASE, "general", "audit_log.csv")
        if os.path.exists(audit_path):
            st.dataframe(pd.read_csv(audit_path).sort_values(by="Timestamp", ascending=False), use_container_width=True)

elif role == "Buyer":
    # Pizza Tracker
    current_stage = get_pipeline(u_id)
    cols = st.columns(len(STAGES))
    for i, s in enumerate(STAGES):
        active = STAGES.index(current_stage) >= i
        color = "#1a3c6d" if active else "#cbd5e1"
        cols[i].markdown(f"<p style='text-align:center; color:{color}; font-size:0.8rem;'>{'✅' if active else '○'}<br><b>{s.upper()}</b></p>", unsafe_allow_html=True)
    st.progress(STAGES.index(current_stage) / (len(STAGES)-1))

    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b = st.columns([1.5, 1])

    with col_a:
        st.markdown('<div class="bento-card">', unsafe_allow_html=True)
        st.subheader("📌 Transaction Checklist")
        st.checkbox("Prequalification", value=True)
        st.checkbox("Contract Signed", value=(STAGES.index(current_stage) >= 1))
        st.checkbox("Appraisal Complete", value=(STAGES.index(current_stage) >= 2))
        st.checkbox("Closing Set", value=(STAGES.index(current_stage) >= 4))
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="bento-card">', unsafe_allow_html=True)
        st.subheader("🔐 Encrypted Vault")
        doc_dir = os.path.join(VAULT_BASE, "buyer_docs")
        user_docs = [f for f in os.listdir(doc_dir) if f.startswith(f"ENCR_{u_id}_")]
        if user_docs:
            for i, d in enumerate(user_docs):
                data = read_encrypted(os.path.join(doc_dir, d))
                if data: st.download_button(f"📥 DOWNLOAD: {d.split('_')[-1]}", data, key=f"b_{i}", use_container_width=True)
        else: st.info("Vault is currently empty.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="bento-card">', unsafe_allow_html=True)
        st.subheader("📤 Document Upload")
        b_up = st.file_uploader("Upload", label_visibility="collapsed")
        if st.button("Submit to Portal", use_container_width=True):
            if b_up:
                save_encrypted(os.path.join(VAULT_BASE, "admin_inbox", f"FROM_{u_id}_{b_up.name}"), b_up.getvalue())
                st.success("Securely Transmitted.")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="bento-card" style="background-color:#eff6ff;">', unsafe_allow_html=True)
        st.subheader("🤖 Support AI")
        st.text_input("Ask about your status...", placeholder="What's next?")
        st.markdown('</div>', unsafe_allow_html=True)

# ── 7. FOOTER ─────────────────────────────────────────────────────────────────
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown(f"""
    <div style="display: flex; justify-content: center; gap: 30px; opacity: 0.6; font-size: 11px; font-family: 'Oswald'; color: #1a3c6d;">
        <div style="display: flex; align-items: center;"><span class="green-pulse" style="height:6px; width:6px; margin-right:5px;"></span>SYSTEM: PRIMARY NODE</div>
        <div>STATUS: ENCRYPTED</div>
        <div style="font-weight: bold;">© 2026 UTAH LAND & PROPERTY</div>
    </div>
""", unsafe_allow_html=True)
