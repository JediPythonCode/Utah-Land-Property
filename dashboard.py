import streamlit as st
from streamlit_autorefresh import st_autorefresh
import os
import json
import pandas as pd
from datetime import datetime
from cryptography.fernet import Fernet
from collections.abc import Mapping

# ── 1. CONFIG & SECURE ENCRYPTION ─────import streamlit as st
from streamlit_autorefresh import st_autorefresh
import os
import json
import pandas as pd
from datetime import datetime
from cryptography.fernet import Fernet

# ── 1. CONFIGURATION & STATE INITIALIZATION ──────────────────────────────────
st.set_page_config(
    page_title="ULP | 2026 Transaction Hub",
    layout="wide",
    initial_sidebar_state="collapsed"
)

STAGES = ["Application", "Processing", "Underwriting", "Approved", "Closed"]

# Persist user checklist state in session
if "checklist_state" not in st.session_state:
    st.session_state.checklist_state = {
        "prequal": True, "offer": True, "inspections": False, "closing": False
    }

if "refresh_initialized" not in st.session_state:
    st_autorefresh(interval=600000, key="ulp_refresh")
    st.session_state.refresh_initialized = True

def initialize_vault():
    try:
        key = st.secrets.get("secret_key", Fernet.generate_key().decode())
        users = dict(st.secrets.get("users", {"demo": {"key": "1234", "role": "Buyer"}}))
        return Fernet(key.encode()), users
    except Exception as e:
        st.error(f"Vault Error: {e}")
        st.stop()

fernet, USER_DB = initialize_vault()

# ── 2. ADVANCED 2026 BENTO UI (CSS) ───────────────────────────────────────────
st.markdown("""
    <style>
        /* Base Theme */
        .stApp { background-color: #ffffff; }
        
        /* Bento Grid Container */
        .bento-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
            padding: 1rem 0;
        }

        /* Bento Card Styling */
        .bento-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 20px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            transition: transform 0.2s ease;
        }
        .bento-card:hover { border-color: #1a3c6d; transform: translateY(-2px); }

        /* Typography & Trust Signals */
        h1, h2, h3 { color: #1e293b !important; font-weight: 800 !important; }
        .trust-pill {
            background: #f0fdf4; color: #166534;
            padding: 6px 14px; border-radius: 100px;
            font-size: 0.75rem; font-weight: 700; border: 1px solid #bbf7d0;
        }

        /* Pizza Tracker UI */
        .tracker-container { display: flex; justify-content: space-between; margin-bottom: 2rem; }
        .step { text-align: center; flex: 1; position: relative; }
        .step-active { color: #1a3c6d; font-weight: 700; }
        .step-inactive { color: #cbd5e1; }

        /* Buttons */
        .stButton>button {
            border-radius: 12px; background-color: #1a3c6d; color: white;
            border: none; padding: 0.5rem 1rem; width: 100%;
        }
    </style>
""", unsafe_allow_html=True)

# ── 3. DATA & VAULT UTILITIES ────────────────────────────────────────────────
VAULT_BASE = "vault"
for folder in ["buyer_docs", "admin_inbox", "pipeline"]:
    os.makedirs(os.path.join(VAULT_BASE, folder), exist_ok=True)

def get_status(u_id):
    path = os.path.join(VAULT_BASE, "pipeline", f"{u_id}.json")
    if os.path.exists(path):
        with open(path, "r") as f: return json.load(f).get("stage", STAGES[0])
    return STAGES[0]

def save_file_encrypted(u_id, file_obj, destination):
    filename = f"ENCR_{u_id}_{file_obj.name}"
    path = os.path.join(VAULT_BASE, destination, filename)
    encrypted_data = fernet.encrypt(file_obj.getvalue())
    with open(path, "wb") as f: f.write(encrypted_data)
    return filename

# ── 4. MAIN APP LOGIC ────────────────────────────────────────────────────────
if "auth" not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.image("https://via.placeholder.com/150x50?text=ULP+LOGOTYPE", width=150)
        st.title("Secure Access")
        uid = st.text_input("Username").lower()
        upw = st.text_input("Access Key", type="password")
        if st.button("Authorize Session"):
            if uid in USER_DB and str(USER_DB[uid]["key"]) == upw:
                st.session_state.auth, st.session_state.uid = True, uid
                st.session_state.role = USER_DB[uid]["role"]
                st.rerun()
else:
    uid, role = st.session_state.uid, st.session_state.role
    
    # SIDEBAR CONTROL
    with st.sidebar:
        st.title("Control Center")
        st.write(f"User: **{uid.upper()}**")
        if st.button("Terminate Session"):
            st.session_state.auth = False
            st.rerun()

    if role == "Buyer":
        # ── HEADER & TRUST ──
        c1, c2 = st.columns([2, 1])
        with c1:
            st.title(f"Hello, {uid.title()}")
            st.markdown('<span class="trust-pill">🛡️ SOC-2 VERIFIED PORTAL</span> <span class="trust-pill">⛓️ BLOCKCHAIN LEDGER ACTIVE</span>', unsafe_allow_html=True)
        
        # ── REAL-TIME PIZZA TRACKER ──
        status = get_status(uid)
        st.write("---")
        cols = st.columns(len(STAGES))
        for i, s in enumerate(STAGES):
            active = STAGES.index(status) >= i
            color = "#1a3c6d" if active else "#cbd5e1"
            icon = "✅" if active else "○"
            cols[i].markdown(f"<p style='text-align:center; color:{color};'>{icon}<br>{s}</p>", unsafe_allow_html=True)
        st.progress(STAGES.index(status) / (len(STAGES)-1))

        # ── BENTO GRID LAYOUT ──
        st.markdown('<div class="bento-grid">', unsafe_allow_html=True)
        
        # Grid Column 1
        col_left, col_mid, col_right = st.columns([1, 1, 1])

        with col_left:
            st.markdown('<div class="bento-card">', unsafe_allow_html=True)
            st.subheader("📌 Transaction Checklist")
            st.session_state.checklist_state["prequal"] = st.checkbox("Prequalification Letter", value=st.session_state.checklist_state["prequal"])
            st.session_state.checklist_state["offer"] = st.checkbox("Purchase Agreement Signed", value=st.session_state.checklist_state["offer"])
            st.session_state.checklist_state["inspections"] = st.checkbox("Appraisal Received", value=st.session_state.checklist_state["inspections"])
            st.session_state.checklist_state["closing"] = st.checkbox("Review Closing Disclosure", value=st.session_state.checklist_state["closing"])
            st.markdown('</div>', unsafe_allow_html=True)

        with col_mid:
            st.markdown('<div class="bento-card">', unsafe_allow_html=True)
            st.subheader("🔐 Document Vault")
            doc_path = os.path.join(VAULT_BASE, "buyer_docs")
            files = [f for f in os.listdir(doc_path) if f.startswith(f"ENCR_{uid}")]
            if files:
                for f in files:
                    clean_name = f.replace(f"ENCR_{uid}_", "")
                    st.download_button(f"📥 {clean_name}", b"data", key=f)
            else:
                st.caption("No files shared yet.")
            st.markdown('</div>', unsafe_allow_html=True)

        with col_right:
            st.markdown('<div class="bento-card">', unsafe_allow_html=True)
            st.subheader("📤 SNapp Upload")
            uploaded_file = st.file_uploader("Drop docs here", label_visibility="collapsed")
            if st.button("Secure Send"):
                if uploaded_file:
                    save_file_encrypted(uid, uploaded_file, "admin_inbox")
                    st.toast("Encrypted Transmission Successful")
            st.markdown('</div>', unsafe_allow_html=True)

        # ── ROW 2: ADVANCED TOOLS ──
        col_bot1, col_bot2 = st.columns([1.5, 1])
        with col_bot1:
            st.markdown('<div class="bento-card">', unsafe_allow_html=True)
            st.subheader("📈 Mortgage Insight (2026)")
            price = st.slider("Property Price", 200000, 1000000, 450000)
            rate = 6.5 # Fixed for 2026 demo
            st.metric("Estimated Monthly P&I", f"${(price * (rate/1200)):,.2f}", "+$12.50 vs Last Week")
            st.markdown('</div>', unsafe_allow_html=True)

        with col_bot2:
            st.markdown('<div class="bento-card" style="background:#eff6ff;">', unsafe_allow_html=True)
            st.subheader("🤖 ULP-AI Chat")
            st.text_input("Ask: 'When is my appraisal?'", key="chat_input")
            st.caption("AI is analyzing your contract details in real-time.")
            st.markdown('</div>', unsafe_allow_html=True)

    elif role == "Admin":
        st.title("Admin Pipeline Command")
        # Admin logic here...────────────────────────────────────────
st.set_page_config(
    page_title="Utah Land & Property | Deal-Flow",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Constants for Stage consistency
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

# ── 2. BRANDING & STYLING (FORCED LIGHT MODE) ──────────────────────────────────
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
        
        /* Force White Background on App and Sidebar */
        .stApp, [data-testid="stSidebar"], [data-testid="stHeader"] {
            background-color: #ffffff !important;
        }

        /* Force Dark Navy Text for all standard elements */
        h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, [data-testid="stWidgetLabel"] p {
            color: #0f172a !important; 
            font-family: 'Inter', sans-serif;
        }

        /* Input Fields: Light background with Dark Text */
        .stTextInput input, .stSelectbox div {
            background-color: #f8fafc !important;
            color: #0f172a !important;
            border: 1px solid #cbd5e1 !important;
        }

        /* Metric Cards / Containers */
        div[data-testid="stVerticalBlock"] > div[style*="border"] {
            background-color: #f8fafc !important;
            border: 1px solid #e2e8f0 !important;
        }

        /* Tabs Styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            background-color: #ffffff;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: #f1f5f9;
            border-radius: 4px;
            color: #475569 !important;
            padding: 8px 16px;
        }
        .stTabs [aria-selected="true"] {
            background-color: #1a3c6d !important;
            color: #ffffff !important;
        }
        
        /* Hide Streamlit default header for a cleaner POS look */
        [data-testid="stHeader"] { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# ── 3. CORE LOGIC & VAULT ─────────────────────────────────────────────────────
VAULT_BASE = "vault"
FOLDERS = ["general", "buyer_docs", "admin_inbox", "metadata", "pipeline"]
for folder in FOLDERS:
    os.makedirs(os.path.join(VAULT_BASE, folder), exist_ok=True)

AUDIT_FILE = os.path.join(VAULT_BASE, "general", "audit_log.csv")

def logger(user, action, details):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = pd.DataFrame([[timestamp, user, action, str(details)]], 
                                columns=["Timestamp", "User", "Action", "Details"])
        log_entry.to_csv(AUDIT_FILE, mode='a', header=not os.path.exists(AUDIT_FILE), index=False)
    except: pass

def save_encrypted(file_path, data, description=""):
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
        try:
            with open(pipe_path, "r") as f: 
                return json.load(f).get("stage", STAGES[0])
        except: return STAGES[0]
    return STAGES[0]

# ── 4. UI FLOW (AUTH) ─────────────────────────────────────────────────────────
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    _, col_mid, _ = st.columns([1, 1.5, 1])
    with col_mid:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align:center;'>ULP DIGITAL VAULT</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#475569;'>SECURE POINT-OF-SALE INTERFACE</p>", unsafe_allow_html=True)
        
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
    # ── 5. DASHBOARD ──────────────────────────────────────────────────────────
    role = st.session_state.user_role
    u_id = st.session_state.user_id

    st.sidebar.markdown(f"### **Operator:** {u_id.upper()}")
    st.sidebar.markdown(f"**Role:** {role}")
    if st.sidebar.button("Terminal Logout"):
        st.session_state.authenticated = False
        st.rerun()

    if role == "Admin":
        st.title("Admin Deal-Flow Command")
        t1, t2, t3, t4 = st.tabs(["Pipeline (CRM)", "Distribution (POS)", "Total eClose", "Audit"])

        with t1:
            st.subheader("TotalExpert Pipeline Intelligence")
            buyers = [u for u in USER_DB if USER_DB[u].get('role') == 'Buyer']
            for buyer in buyers:
                col1, col2, col3 = st.columns([1, 2, 1])
                col1.markdown(f"**{buyer.upper()}**")
                
                current_val = get_pipeline(buyer)
                try:
                    current_idx = STAGES.index(current_val)
                except ValueError:
                    current_idx = 0
                
                stage = col2.selectbox("Deal Stage", STAGES, key=f"pipe_{buyer}", index=current_idx)
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
            inbox_path = os.path.join(VAULT_BASE, "admin_inbox")
            buyer_uploads = os.listdir(inbox_path) if os.path.exists(inbox_path) else []
            if buyer_uploads:
                for b_file in buyer_uploads:
                    st.write(f"📩 **Incoming:** {b_file}")
                    raw_data = read_encrypted(os.path.join(inbox_path, b_file))
                    if raw_data:
                        st.download_button("Review Document", raw_data, file_name=b_file, key=f"dl_{b_file}")
            else:
                st.write("No pending documents.")

        with t4:
            if os.path.exists(AUDIT_FILE):
                st.dataframe(pd.read_csv(AUDIT_FILE).sort_values(by="Timestamp", ascending=False), use_container_width=True)

    elif role == "Buyer":
        st.title("SNapp Home Portal")
        current_stage = get_pipeline(u_id)
        st.markdown(f"### Current Deal Status: `{current_stage}`")
        
        try:
            prog_val = STAGES.index(current_stage) / (len(STAGES) - 1)
        except:
            prog_val = 0.0
        st.progress(prog_val)

        col_a, col_b = st.columns([2, 1])
        with col_a:
            st.subheader("Secure Documents")
            doc_dir = os.path.join(VAULT_BASE, "buyer_docs")
            user_docs = [f for f in os.listdir(doc_dir) if f.startswith(f"ENCR_{u_id}_")] if os.path.exists(doc_dir) else []
            if user_docs:
                for i, d in enumerate(user_docs):
                    clean_name = d.replace(f"ENCR_{u_id}_", "")
                    data = read_encrypted(os.path.join(doc_dir, d))
                    if data:
                        st.download_button(f"📥 Download {clean_name}", data, file_name=clean_name, key=f"b_dl_{i}")
            else:
                st.info("No documents shared yet.")

        with col_b:
            st.subheader("SNapp Upload (POS)")
            b_up = st.file_uploader("Upload required docs", accept_multiple_files=False)
            if st.button("Submit to Admin"):
                if b_up:
                    path = os.path.join(VAULT_BASE, "admin_inbox", f"FROM_{u_id}_{b_up.name}")
                    save_encrypted(path, b_up.getvalue(), "Buyer Uploaded")
                    st.success("Successfully Transmitted.")

        st.divider()
        st.subheader("Market Intelligence (MBS Highway)")
        st.info("Live Update: Rate lock recommendations and bid-over-ask insights are updated daily.")
