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
    ENCR_KEY = b'6_Wb7R-5N5_W_h_Z9F-4Qp3o9-G7_X_z1H-8I_w_9k0=' 
else:
    ENCR_KEY = st.secrets["secret_key"].encode()

fernet = Fernet(ENCR_KEY)

# ── 2. BRANDING & STYLING (GLOBAL) ──────────────────────────────────────────
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&family=Oswald:wght@500;700&display=swap');
        .stApp { background-color: #f8f9fa !important; }
        header, footer, [data-testid="stHeader"] { display: none !important; }
        .viewport-top-container { display: flex; flex-direction: column; justify-content: center; align-items: center; min-height: 40vh; padding-top: 50px; text-align: center; width: 100%; }
        .brand-title { font-family: 'Inter', sans-serif !important; font-size: clamp(38px, 8vw, 78px) !important; font-weight: 900 !important; color: #1a3c6d !important; letter-spacing: -1.5px !important; margin-bottom: 0px !important; line-height: 1.0 !important; }
        .brand-subtitle { font-family: 'Oswald', sans-serif !important; font-size: clamp(1rem, 3vw, 1.35rem) !important; color: #6b7280 !important; letter-spacing: 3px !important; font-weight: 500 !important; margin-top: 10px !important; margin-bottom: 1.5rem !important; }
        .framework-text { color: #4b5563 !important; font-size: 1.05rem !important; max-width: 800px !important; margin: 0 auto 2rem !important; line-height: 1.7 !important; font-family: 'Inter', sans-serif !important; }
        .pulse-lock { height: 12px; width: 12px; background: #10b981; border-radius: 50%; display: inline-block; margin-right: 12px; box-shadow: 0 0 12px rgba(16,185,129,0.5); animation: pulse 2s infinite; }
        @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(16,185,129,0.7); } 70% { box-shadow: 0 0 0 12px rgba(16,185,129,0); } 100% { box-shadow: 0 0 0 0 rgba(16,185,129,0); } }
        .access-text { font-family: 'Oswald', sans-serif !important; font-size: 0.9rem !important; color: #1a3c6d !important; font-weight: 700 !important; letter-spacing: 2px !important; }
        .recent-file-card { background: white; padding: 10px; border-radius: 8px; border: 1px solid #ddd; margin-bottom: 10px; text-align: left; }
    </style>
""", unsafe_allow_html=True)

# ── 3. CORE LOGIC ────────────────────────────────────────────────────────────
DISCLOSURE_FILE = "vault/general/deal_structure.txt"
AUDIT_FILE = "vault/general/audit_log.csv"

for folder in ["vault/general", "vault/buyer_docs", "vault/property_images"]:
    os.makedirs(folder, exist_ok=True)

def logger(user, action, details):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = pd.DataFrame([[timestamp, user, action, str(details)]], columns=["Timestamp", "User", "Action", "Details"])
    log_entry.to_csv(AUDIT_FILE, mode='a', header=not os.path.exists(AUDIT_FILE), index=False)

def save_encrypted(file_path, data):
    encrypted_data = fernet.encrypt(data)
    with open(file_path, "wb") as f: f.write(encrypted_data)

def read_encrypted(file_path):
    with open(file_path, "rb") as f: return fernet.decrypt(f.read())

def load_disclosure():
    if os.path.exists(DISCLOSURE_FILE):
        with open(DISCLOSURE_FILE, "r") as f: return f.read()
    return "Standard Disclosure: Secure Underwriting in Progress."

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# ── 4. THE UI FLOW ───────────────────────────────────────────────────────────
if not st.session_state.authenticated:
    st.markdown("""
        <div class="viewport-top-container">
            <div class="brand-title">Utah Land & Property</div>
            <div class="brand-subtitle">Strategic Asset Protection Framework</div>
            <div class="framework-text"><strong>Privacy Creation Preservation • Creative Land & Real Estate Deal Structure</strong></div>
            <div style="margin-bottom: 2rem;"><span class="pulse-lock"></span><span class="access-text">SECURE CLIENT PORTAL ENCRYPTED ACCESS ONLY</span></div>
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
                logger(user_id, "Login", "Success")
                st.rerun()
            else: st.error("Access Denied")

else:
    # ── 5. AUTHENTICATED DASHBOARD ──────────────────────────────────────────
    role = st.session_state.user_role
    user_id = st.session_state.user_id

    st.title(f"{role} Portal")
    st.warning(f"🔔 **Deal Structure:** {load_disclosure()}")
    
    if st.sidebar.button("Secure Logout"):
        st.session_state.authenticated = False
        st.rerun()

    # --- SHARED ACTIVITY VIEW ---
    st.subheader("Latest Activity")
    all_files = []
    for root, dirs, files in os.walk("vault"):
        for f in files:
            if not f.startswith('.'):
                path = os.path.join(root, f)
                all_files.append((f, os.path.getmtime(path), root.split('/')[-1]))
    all_files.sort(key=lambda x: x[1], reverse=True)
    if all_files:
        feed_cols = st.columns(3)
        for i, (fname, ftime, ftype) in enumerate(all_files[:3]):
            dt = datetime.fromtimestamp(ftime).strftime('%Y-%m-%d %H:%M')
            feed_cols[i].markdown(f'<div class="recent-file-card"><strong>{fname[:20]}...</strong><br><small>{ftype.title()} | {dt}</small></div>', unsafe_allow_html=True)

    # --- ROLE LOGIC ---
    if role == "Admin":
        t1, t2, t3 = st.tabs(["Push Disclosure", "Assign Files", "System Audit"])
        with t1:
            new_disc = st.text_area("Update Deal Structure Text", value=load_disclosure())
            if st.button("Update Everyone"):
                with open(DISCLOSURE_FILE, "w") as f: f.write(new_disc)
                st.success("Disclosure updated.")
        with t2:
            target = st.text_input("Target User ID")
            up_files = st.file_uploader("Upload Docs for Buyer", accept_multiple_files=True)
            if st.button("Encrypt & Assign") and up_files and target:
                for f in up_files:
                    save_encrypted(os.path.join("vault/buyer_docs", f"ENCR_{target}_{f.name}"), f.getbuffer())
                st.success("Files assigned.")
        with t3:
            if os.path.exists(AUDIT_FILE): st.dataframe(pd.read_csv(AUDIT_FILE).tail(10))

    elif role == "Buyer":
        with st.expander("📊 Underwriting Pre-Screen", expanded=True):
            inc = st.number_input("Monthly Income", value=5000)
            debt = st.number_input("Monthly Debt", value=1500)
            if st.button("Log Analysis"):
                logger(user_id, "Underwriting", f"DTI: {(debt/inc)*100:.1f}%")
                st.success("Logged.")
        
        st.subheader("Your Documents")
        docs = [f for f in os.listdir("vault/buyer_docs") if user_id in f]
        if docs:
            for d in docs:
                data = read_encrypted(os.path.join("vault/buyer_docs", d))
                st.download_button(f"📄 Download {d.replace('ENCR_'+user_id+'_', '')}", data, file_name=d)
        else:
            st.info("No documents released yet.")
