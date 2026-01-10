import streamlit as st
from streamlit_autorefresh import st_autorefresh
import os
import json
import pandas as pd
from datetime import datetime
from cryptography.fernet import Fernet

# ── 1. CONFIG & SECURE ENCRYPTION ─────────────────────────────────────────────
st.set_page_config(
    page_title="Utah Land & Property | Deal-Flow",
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

# ── 2. BRANDING & STYLING ─────────────────────────────────────────────────────
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&family=Oswald:wght@500;700&display=swap');
        .stApp { background-color: #ffffff !important; color: #1a1a1a !important; }
        
        /* Restore Original Header Colors */
        h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown {
            color: #1a3c6d !important; font-family: 'Inter', sans-serif;
        }
        
        /* Tab Navigation Styling */
        [data-testid="stHeader"] { display: none !important; }
        .stTabs [data-baseweb="tab-list"] { gap: 24px; }
        .stTabs [data-baseweb="tab"] {
            height: 50px; background-color: #f1f5f9; border-radius: 8px 8px 0 0;
            padding: 10px 20px; font-weight: 600;
        }
        .stTabs [aria-selected="true"] { background-color: #1a3c6d !important; color: white !important; }

        /* 2026 Bento Card Layouts */
        .bento-card {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            padding: 24px;
            border-radius: 16px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        }
        
        .trust-badge {
            background-color: #ecfdf5; color: #065f46;
            padding: 4px 12px; border-radius: 99px;
            font-size: 12px; font-weight: 600; border: 1px solid #10b981;
        }
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

# ── 4. ORIGINAL LOGIN FLOW (UTAH LAND & PROPERTY) ───────────────────────────────
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    _, col_mid, _ = st.columns([1, 1.5, 1])
    with col_mid:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align:center;'>UTAH LAND & PROPERTY</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center; font-size:1.2rem; margin-top:-15px;'>DIGITAL VAULT</h2>", unsafe_allow_html=True)
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
    st.stop()

# ── 5. DASHBOARD ──────────────────────────────────────────────────────────
role, u_id = st.session_state.user_role, st.session_state.user_id

st.sidebar.markdown(f"**Operator:** {u_id.upper()}")
st.sidebar.markdown(f"**Role:** {role}")
if st.sidebar.button("Terminal Logout"):
    st.session_state.authenticated = False
    st.rerun()

if role == "Admin":
    st.title("Admin Deal-Flow Command")
    t1, t2, t3, t4 = st.tabs(["Pipeline (CRM)", "Distribution (POS)", "Total eClose", "Audit"])

    with t1:
        st.subheader("TotalExpert Pipeline Intelligence")
        buyers = [u for u in USER_DB if USER_DB[u]['role'] == 'Buyer']
        for buyer in buyers:
            col1, col2, col3 = st.columns([1, 2, 1])
            col1.write(f"**{buyer}**")
            current = get_pipeline(buyer)
            idx = STAGES.index(current) if current in STAGES else 0
            stage = col2.selectbox("Deal Stage", STAGES, key=f"pipe_{buyer}", index=idx)
            if col3.button("Update", key=f"btn_{buyer}"):
                update_pipeline(buyer, stage)
                st.toast(f"Updated {buyer}")

    with t2:
        st.subheader("SNapp Document Distribution")
        target = st.selectbox("Select Target Account", options=list(USER_DB.keys()))
        note = st.text_input("Note for Buyer")
        files = st.file_uploader("Upload Assets", accept_multiple_files=True)
        if st.button("Encrypt & Transmit") and files:
            for f in files:
                path = os.path.join(VAULT_BASE, "buyer_docs", f"ENCR_{target}_{f.name}")
                save_encrypted(path, f.getvalue(), note)
            st.success("Assets Delivered.")

    with t3:
        st.subheader("DocMagic eClose Status")
        inbox = os.path.join(VAULT_BASE, "admin_inbox")
        if os.path.exists(inbox):
            for b_file in os.listdir(inbox):
                st.write(f"📩 {b_file}")
                data = read_encrypted(os.path.join(inbox, b_file))
                if data: st.download_button("Review", data, file_name=b_file, key=b_file)

    with t4:
        audit_path = os.path.join(VAULT_BASE, "general", "audit_log.csv")
        if os.path.exists(audit_path):
            st.dataframe(pd.read_csv(audit_path).sort_values(by="Timestamp", ascending=False), use_container_width=True)

elif role == "Buyer":
    # ── 2026 INTERACTIVE TRANSACTION HUB ──────────────────────────────────────
    st.markdown("<h1>Utah Land & Property</h1>", unsafe_allow_html=True)
    st.markdown(f"### SNapp Home Portal | {u_id.upper()}")
    
    # 2026 Pizza Tracker UI
    current_stage = get_pipeline(u_id)
    cols = st.columns(len(STAGES))
    for i, s in enumerate(STAGES):
        active = STAGES.index(current_stage) >= i
        color = "#1a3c6d" if active else "#cbd5e1"
        cols[i].markdown(f"<p style='text-align:center; color:{color}; font-size:0.8rem;'>{'✅' if active else '○'}<br><b>{s}</b></p>", unsafe_allow_html=True)
    st.progress(STAGES.index(current_stage) / (len(STAGES)-1))

    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b = st.columns([1.5, 1])

    with col_a:
        # BENTO BOX: TASK CHECKLIST
        st.markdown('<div class="bento-card">', unsafe_allow_html=True)
        st.subheader("📌 Dynamic Checklist")
        st.checkbox("Prequalification: Store pre-approval letter", value=True)
        st.checkbox("Offer & Contract: E-sign purchase agreement", value=True)
        st.checkbox("Inspections & Appraisals", value=(STAGES.index(current_stage) >= 2))
        st.checkbox("Closing Prep: Verify wire instructions", value=(STAGES.index(current_stage) >= 4))
        st.markdown('</div>', unsafe_allow_html=True)

        # BENTO BOX: SECURE VAULT
        st.markdown('<div class="bento-card">', unsafe_allow_html=True)
        st.subheader("🔐 Secure Document Vault")
        doc_dir = os.path.join(VAULT_BASE, "buyer_docs")
        user_docs = [f for f in os.listdir(doc_dir) if f.startswith(f"ENCR_{u_id}_")]
        if user_docs:
            for i, d in enumerate(user_docs):
                data = read_encrypted(os.path.join(doc_dir, d))
                if data: st.download_button(f"📥 {d.replace(f'ENCR_{u_id}_', '')}", data, key=f"b_{i}")
        else: st.info("No documents shared in vault.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        # BENTO BOX: POS UPLOAD
        st.markdown('<div class="bento-card">', unsafe_allow_html=True)
        st.subheader("📤 SNapp Upload (POS)")
        b_up = st.file_uploader("Upload docs", label_visibility="collapsed")
        if st.button("Submit to Admin", use_container_width=True):
            if b_up:
                save_encrypted(os.path.join(VAULT_BASE, "admin_inbox", f"FROM_{u_id}_{b_up.name}"), b_up.getvalue())
                st.success("Transmitted.")
        st.markdown('</div>', unsafe_allow_html=True)

        # BENTO BOX: AI SUPPORT
        st.markdown('<div class="bento-card" style="background-color:#eff6ff;">', unsafe_allow_html=True)
        st.subheader("🤖 Conversational AI")
        st.text_input("Ask about your loan status...", placeholder="What's next?")
        st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    st.subheader("Market Intelligence (MBS Highway)")
    st.info("Live Update: Rate lock recommendations updated daily.")
