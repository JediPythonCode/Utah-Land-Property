import streamlit as st
from streamlit_autorefresh import st_autorefresh
import os
import json
import pandas as pd
from datetime import datetime
from cryptography.fernet import Fernet
from collections.abc import Mapping

# ── 1. CONFIG & SECURE ENCRYPTION (LOS SOURCE OF TRUTH) ──────────────────────
st.set_page_config(
    page_title="Utah Land & Property | Deal-Flow",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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

# ── 2. BRANDING & STYLING (SNapp UI INSPIRATION) ──────────────────────────────
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&family=Oswald:wght@500;700&display=swap');
        .stApp { background-color: #ffffff !important; color: #1a1a1a !important; }
        h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown {
            color: #1a3c6d !important; font-family: 'Inter', sans-serif;
        }
        .metric-card {
            background: #f8fafc; border: 1px solid #e2e8f0; padding: 20px;
            border-radius: 12px; text-align: center;
        }
        [data-testid="stHeader"] { display: none !important; }
        .stTabs [data-baseweb="tab-list"] { gap: 24px; }
        .stTabs [data-baseweb="tab"] {
            height: 50px; background-color: #f1f5f9; border-radius: 8px 8px 0 0;
            padding: 10px 20px; font-weight: 600;
        }
        .stTabs [aria-selected="true"] { background-color: #1a3c6d !important; color: white !important; }
    </style>
""", unsafe_allow_html=True)

# ── 3. CORE LOGIC & VAULT ─────────────────────────────────────────────────────
VAULT_BASE = "vault"
FOLDERS = ["general", "buyer_docs", "admin_inbox", "metadata", "pipeline"]
for folder in FOLDERS:
    os.makedirs(os.path.join(VAULT_BASE, folder), exist_ok=True)

AUDIT_FILE = os.path.join(VAULT_BASE, "general", "audit_log.csv")
DISCLOSURE_FILE = os.path.join(VAULT_BASE, "general", "deal_structure.txt")

def logger(user, action, details):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = pd.DataFrame([[timestamp, user, action, str(details)]], 
                                columns=["Timestamp", "User", "Action", "Details"])
        log_entry.to_csv(AUDIT_FILE, mode='a', header=not os.path.exists(AUDIT_FILE), index=False)
    except: pass

def save_encrypted(file_path, data, description="", folder="buyer_docs"):
    encrypted_data = fernet.encrypt(data)
    with open(file_path, "wb") as f: f.write(encrypted_data)
    meta_name = os.path.basename(file_path) + ".json"
    meta_path = os.path.join(VAULT_BASE, "metadata", meta_name)
    with open(meta_path, "w") as f:
        json.dump({"description": description, "timestamp": str(datetime.now())}, f)

def read_encrypted(file_path):
    try:
        with open(file_path, "rb") as f: return fernet.decrypt(f.read())
    except: return None

def update_pipeline(u_id, stage):
    pipe_path = os.path.join(VAULT_BASE, "pipeline", f"{u_id}.json")
    with open(pipe_path, "w") as f:
        json.dump({"stage": stage, "updated": str(datetime.now())}, f)

def get_pipeline(u_id):
    pipe_path = os.path.join(VAULT_BASE, "pipeline", f"{u_id}.json")
    if os.path.exists(pipe_path):
        with open(pipe_path, "r") as f: return json.load(f).get("stage", "Initial Contact")
    return "Initial Contact"

# ── 4. UI FLOW (TOTALEXPERT INSPIRED AUTH) ────────────────────────────────────
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    _, col_mid, _ = st.columns([1, 1.5, 1])
    with col_mid:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align:center;'>ULP DIGITAL VAULT</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#64748b;'>SECURE POINT-OF-SALE INTERFACE</p>", unsafe_allow_html=True)
        
        u_id_input = st.text_input("ACCESS ID", placeholder="Username").strip().lower()
        u_pwd_input = st.text_input("SECURITY KEY", type="password", placeholder="••••••••").strip()
        
        if st.button("ENTER SECURE PORTAL", use_container_width=True, type="primary"):
            if u_id_input in USER_DB and str(USER_DB[u_id_input].get("key")) == u_pwd_input:
                st.session_state.authenticated = True
                st.session_state.user_id = u_id_input
                st.session_state.user_role = USER_DB[u_id_input].get("role", "Buyer")
                logger(u_id_input, "Auth", "Success")
                st.rerun()
            else:
                st.error("Authentication Failed")

else:
    # ── 5. DASHBOARD (TECH STACK INTEGRATION) ─────────────────────────────────
    role = st.session_state.user_role
    u_id = st.session_state.user_id

    st.sidebar.markdown(f"**Operator:** {u_id.upper()}")
    st.sidebar.markdown(f"**Role:** {role}")
    if st.sidebar.button("Termnal Logout"):
        st.session_state.authenticated = False
        st.rerun()

    if role == "Admin":
        st.title("Admin Deal-Flow Command")
        t1, t2, t3, t4 = st.tabs(["Pipeline (CRM)", "Distribution (POS)", "Total eClose", "Audit"])

        with t1:
            st.subheader("TotalExpert Pipeline Intelligence")
            for buyer in [u for u in USER_DB if USER_DB[u]['role'] == 'Buyer']:
                col1, col2, col3 = st.columns([1, 2, 1])
                col1.write(f"**{buyer}**")
                stage = col2.selectbox("Deal Stage", ["Application", "Processing", "Underwriting", "Approved", "Closed"], key=f"pipe_{buyer}", index=["Application", "Processing", "Underwriting", "Approved", "Closed"].index(get_pipeline(buyer)))
                if col3.button("Update", key=f"btn_{buyer}"):
                    update_pipeline(buyer, stage)
                    st.toast(f"Updated {buyer} to {stage}")

        with t2:
            st.subheader("SNapp Document Distribution")
            target = st.selectbox("Select Target Account", options=list(USER_DB.keys()))
            note = st.text_input("Note for Buyer (Visible in POS)")
            files = st.file_uploader("Upload Assets", accept_multiple_files=True)
            if st.button("Encrypt & Transmit") and files:
                for f in files:
                    path = os.path.join(VAULT_BASE, "buyer_docs", f"ENCR_{target}_{f.name}")
                    save_encrypted(path, f.getvalue(), note)
                st.success("Assets Delivered.")

        with t3:
            st.subheader("DocMagic eClose Status")
            st.info("Tracking hybrid and full eNote notarization progress.")
            # Admin can view documents buyers uploaded (POS logic)
            inbox_path = os.path.join(VAULT_BASE, "admin_inbox")
            buyer_uploads = os.listdir(inbox_path)
            if buyer_uploads:
                for b_file in buyer_uploads:
                    st.write(f"📩 **Incoming:** {b_file}")
                    st.download_button("Review Document", read_encrypted(os.path.join(inbox_path, b_file)), file_name=b_file, key=b_file)
            else:
                st.write("No pending documents in SNapp Inbox.")

        with t4:
            if os.path.exists(AUDIT_FILE):
                st.dataframe(pd.read_csv(AUDIT_FILE).sort_values(by="Timestamp", ascending=False), use_container_width=True)

    elif role == "Buyer":
        st.title("SNapp Home Portal")
        
        # CRM Style Status Tracker
        current_stage = get_pipeline(u_id)
        st.markdown(f"### Current Deal Status: `{current_stage}`")
        st.progress(["Application", "Processing", "Underwriting", "Approved", "Closed"].index(current_stage) / 4)

        col_a, col_b = st.columns([2, 1])
        
        with col_a:
            st.subheader("Secure Documents")
            doc_dir = os.path.join(VAULT_BASE, "buyer_docs")
            user_docs = [f for f in os.listdir(doc_dir) if f.startswith(f"ENCR_{u_id}_")]
            for i, d in enumerate(user_docs):
                clean_name = d.replace(f"ENCR_{u_id}_", "")
                data = read_encrypted(os.path.join(doc_dir, d))
                st.download_button(f"📥 Download {clean_name}", data, file_name=clean_name, key=f"b_dl_{i}")

        with col_b:
            st.subheader("SNapp Upload (POS)")
            st.caption("Securely scan/upload documents to your LO.")
            b_up = st.file_uploader("Upload required docs", accept_multiple_files=False)
            if st.button("Submit to Admin"):
                if b_up:
                    path = os.path.join(VAULT_BASE, "admin_inbox", f"FROM_{u_id}_{b_up.name}")
                    save_encrypted(path, b_up.getvalue(), "Buyer Uploaded")
                    st.success("Successfully Transmitted.")

        st.divider()
        st.subheader("Market Intelligence (MBS Highway)")
        st.info("Live Update: Rate lock recommendations and bid-over-ask insights are updated daily.")
