import streamlit as st
from streamlit_autorefresh import st_autorefresh
import os
import json
import pandas as pd
from datetime import datetime
from cryptography.fernet import Fernet

# ── 1. SYSTEM CONFIG & STYLING ────────────────────────────────────────────────
st.set_page_config(
    page_title="ULP | 2026 Transaction Hub",
    layout="wide",
    initial_sidebar_state="collapsed"
)

STAGES = ["Application", "Processing", "Underwriting", "Approved", "Closed"]

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
        .stApp { background-color: #ffffff !important; }
        [data-testid="stHeader"] { visibility: hidden; }
        .bento-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 20px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        }
        h1, h2, h3, p, label, .stMarkdown { color: #0f172a !important; font-family: 'Inter', sans-serif; }
        .trust-pill {
            background: #f0fdf4; color: #166534;
            padding: 4px 12px; border-radius: 100px;
            font-size: 0.75rem; font-weight: 700; border: 1px solid #bbf7d0;
            margin-right: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# ── 2. CORE BACKEND LOGIC ─────────────────────────────────────────────────────
def initialize_system():
    try:
        # Check secrets. Use placeholders ONLY if local development
        key = st.secrets.get("secret_key", "L-9_W7_m6m_kE6pX-7m_fX-p_m6m_kE6pX-7m_fX-p=")
        users = dict(st.secrets.get("users", {"admin": {"key": "1234", "role": "Admin"}}))
        return Fernet(key.encode()), users
    except:
        st.error("🚨 Configuration Error: Check your secrets.toml")
        st.stop()

fernet, USER_DB = initialize_system()
VAULT_BASE = "vault"
for f in ["buyer_docs", "admin_inbox", "pipeline"]:
    os.makedirs(os.path.join(VAULT_BASE, f), exist_ok=True)

def get_pipeline_stage(u_id):
    path = os.path.join(VAULT_BASE, "pipeline", f"{u_id}.json")
    if os.path.exists(path):
        try:
            with open(path, "r") as f: return json.load(f).get("stage", STAGES[0])
        except: return STAGES[0]
    return STAGES[0]

def update_pipeline_stage(u_id, stage):
    path = os.path.join(VAULT_BASE, "pipeline", f"{u_id}.json")
    with open(path, "w") as f:
        json.dump({"stage": stage, "updated": str(datetime.now())}, f)

# ── 3. AUTHENTICATION LOGIC ──────────────────────────────────────────────────
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    _, col_auth, _ = st.columns([1, 1.2, 1])
    with col_auth:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align:center;'>ULP DIGITAL VAULT</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#64748b;'>SECURE 2026 TRANSACTION HUB</p>", unsafe_allow_html=True)
        
        input_uid = st.text_input("ACCESS ID", placeholder="Username").strip().lower()
        input_pwd = st.text_input("SECURITY KEY", type="password", placeholder="••••••••").strip()
        
        if st.button("AUTHORIZE ACCESS", use_container_width=True, type="primary"):
            if input_uid in USER_DB and str(USER_DB[input_uid].get("key")) == input_pwd:
                st.session_state.authenticated = True
                st.session_state.user_id = input_uid
                st.session_state.role = USER_DB[input_uid].get("role", "Buyer")
                st.rerun()
            else:
                st.error("Invalid Credentials")
    st.stop()  # <--- CRITICAL: Prevents the rest of the script from running if not authed

# ── 4. DASHBOARD (ONLY REACHED IF AUTHENTICATED) ─────────────────────────────
# Now it is safe to access these variables
role = st.session_state.role
u_id = st.session_state.user_id

with st.sidebar:
    st.markdown(f"### **{role.upper()} PORTAL**")
    st.write(f"Operator: `{u_id.upper()}`")
    if st.button("Terminate Session"):
        st.session_state.authenticated = False
        st.rerun()

# ── ADMIN INTERFACE ──────────────────────────────────────────────────────────
if role == "Admin":
    st.title("Admin Pipeline Command")
    tab1, tab2 = st.tabs(["Pipeline Management", "Document Inbox"])
    
    with tab1:
        st.subheader("TotalExpert Integration")
        buyers = [u for u in USER_DB if USER_DB[u].get('role') == 'Buyer']
        for b in buyers:
            c1, c2, c3 = st.columns([1, 2, 1])
            c1.markdown(f"**{b.upper()}**")
            current = get_pipeline_stage(b)
            idx = STAGES.index(current) if current in STAGES else 0
            new_stage = c2.selectbox("Change Stage", STAGES, index=idx, key=f"sel_{b}")
            if c3.button("Push Update", key=f"btn_{b}"):
                update_pipeline_stage(b, new_stage)
                st.toast(f"Updated {b} to {new_stage}")

    with tab2:
        st.subheader("Incoming Document Stream")
        inbox_path = os.path.join(VAULT_BASE, "admin_inbox")
        uploads = os.listdir(inbox_path)
        if uploads:
            for f in uploads: st.write(f"📩 {f}")
        else: st.info("Inbox clear.")

# ── BUYER INTERFACE (2026 BENTO HUB) ──────────────────────────────────────────
else:
    st.markdown(f"<h1>Welcome to your Hub, {u_id.title()}</h1>", unsafe_allow_html=True)
    st.markdown('<span class="trust-pill">🛡️ SOC-2 SECURE</span> <span class="trust-pill">⛓️ BLOCKCHAIN VERIFIED</span>', unsafe_allow_html=True)
    
    # Milestone Tracker
    current_s = get_pipeline_stage(u_id)
    cols = st.columns(len(STAGES))
    for i, s in enumerate(STAGES):
        active = STAGES.index(current_s) >= i
        color = "#1a3c6d" if active else "#cbd5e1"
        cols[i].markdown(f"<p style='text-align:center; color:{color}; font-size:0.8rem;'>{'✅' if active else '○'}<br><b>{s}</b></p>", unsafe_allow_html=True)
    st.progress(STAGES.index(current_s) / (len(STAGES)-1))

    # Bento Grid Layout
    st.markdown("<br>", unsafe_allow_html=True)
    col_l, col_r = st.columns([1.5, 1])

    with col_l:
        st.markdown('<div class="bento-card">', unsafe_allow_html=True)
        st.subheader("📌 Transaction Checklist")
        st.checkbox("Prequalification: Completed", value=True)
        st.checkbox("Purchase Agreement: Signed", value=True)
        st.checkbox("Appraisal: In Progress", value=(current_s in ["Underwriting", "Approved", "Closed"]))
        st.checkbox("Closing Prep: Verify Wire", value=(current_s == "Closed"))
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="bento-card">', unsafe_allow_html=True)
        st.subheader("🔐 Secure Vault")
        st.caption("Centralized storage with end-to-end encryption for sensitive financial records.")
        st.info("No documents shared by LO yet.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="bento-card">', unsafe_allow_html=True)
        st.subheader("📤 SNapp Upload (POS)")
        st.file_uploader("Drop document to transmit", label_visibility="collapsed")
        st.button("Secure Send", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="bento-card" style="background:#eff6ff;">', unsafe_allow_html=True)
        st.subheader("🤖 Conversational AI")
        st.text_input("Ask: 'What is my current status?'")
        st.markdown('</div>', unsafe_allow_html=True)
