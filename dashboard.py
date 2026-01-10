import streamlit as st
from streamlit_autorefresh import st_autorefresh
import os
import json
import pandas as pd
from datetime import datetime
from cryptography.fernet import Fernet
from collections.abc import Mapping

# ── 1. CONFIG & SECURE ENCRYPTION ────────────────────────────────────────────
st.set_page_config(
    page_title="Utah Land & Property",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Auto-refresh to keep session alive
if "refresh_initialized" not in st.session_state:
    st_autorefresh(interval=600000, key="ulp_refresh")
    st.session_state.refresh_initialized = True

def initialize_system():
    """Initializes encryption and loads the user database from secrets."""
    try:
        key = st.secrets.get("secret_key")
        users_data = st.secrets.get("users")

        if not key or users_data is None:
            st.error("🚨 SYSTEM ERROR: secrets.toml is missing 'secret_key' or '[users]'.")
            st.stop()

        return Fernet(key.encode()), dict(users_data)
    except Exception as e:
        st.error(f"🚨 SYSTEM CRITICAL: Secrets unreachable. {e}")
        st.stop()

fernet, USER_DB = initialize_system()

# ── 2. BRANDING & STYLING ──────────────────────────────────────────────────
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&family=Oswald:wght@500;700&display=swap');
        .stApp { background-color: #ffffff !important; color: #1a1a1a !important; }
        h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown {
            color: #1a3c6d !important; font-family: 'Inter', sans-serif; font-weight: 600;
        }
        input, textarea, [data-baseweb="select"] {
            background-color: #f9fafb !important; color: #1a1a1a !important;
            border: 1px solid #d1d5db !important;
        }
        [data-testid="stFileUploader"] {
            background-color: #f3f4f6 !important;
            border: 2px dashed #1a3c6d !important;
            border-radius: 10px; padding: 10px;
        }
        header, footer, [data-testid="stHeader"] { display: none !important; }
        .viewport-top-container {
            display: flex; flex-direction: column; justify-content: center;
            align-items: center; min-height: 35vh; padding-top: 40px;
            text-align: center; width: 100%;
        }
        .brand-title {
            font-family: 'Inter', sans-serif !important; font-size: clamp(38px, 8vw, 78px) !important;
            font-weight: 900 !important; color: #1a3c6d !important; letter-spacing: -1.5px !important;
            margin-bottom: 0px !important; line-height: 1.0 !important;
        }
        .brand-subtitle {
            font-family: 'Oswald', sans-serif !important; font-size: 1.25rem !important;
            color: #6b7280 !important; letter-spacing: 3px !important; font-weight: 500 !important;
            margin-top: 10px !important; margin-bottom: 1.5rem !important;
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
    </style>
""", unsafe_allow_html=True)

# ── 3. CORE LOGIC (VAULT OPERATIONS) ─────────────────────────────────────────
VAULT_BASE = "vault"
AUDIT_FILE = os.path.join(VAULT_BASE, "general", "audit_log.csv")
DISCLOSURE_FILE = os.path.join(VAULT_BASE, "general", "deal_structure.txt")

for folder in ["general", "buyer_docs", "property_images", "metadata"]:
    os.makedirs(os.path.join(VAULT_BASE, folder), exist_ok=True)

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
    # Save Metadata (Zoho/Monday style notes)
    meta_path = os.path.join(VAULT_BASE, "metadata", os.path.basename(file_path) + ".json")
    with open(meta_path, "w") as f: 
        json.dump({"description": description, "timestamp": str(datetime.now())}, f)

def read_encrypted(file_path):
    try:
        with open(file_path, "rb") as f: return fernet.decrypt(f.read())
    except: return None

def get_meta(file_path):
    meta_path = os.path.join(VAULT_BASE, "metadata", os.path.basename(file_path) + ".json")
    if os.path.exists(meta_path):
        with open(meta_path, "r") as f:
            return json.load(f).get("description", "No additional notes.")
    return "No description available."

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# ── 4. UI FLOW (ROBUST LOGIN) ────────────────────────────────────────────────
if not st.session_state.authenticated:
    st.markdown("""
        <div class="viewport-top-container">
            <div class="brand-title">Utah Land & Property</div>
            <div class="brand-subtitle">Strategic Asset Protection Framework</div>
            <div style="margin-bottom: 2rem;">
                <span class="pulse-lock"></span>
                <span style="color:#1a3c6d; font-family:'Oswald'; letter-spacing:2px;">SECURE CLIENT PORTAL</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    _, col_mid, _ = st.columns([1, 1.6, 1])
    with col_mid:
        u_id_input = st.text_input("User ID", placeholder="Enter Username", label_visibility="collapsed").strip().lower()
        u_pwd_input = st.text_input("Key", type="password", placeholder="Enter Access Key", label_visibility="collapsed").strip()

        if st.button("Access Portal", use_container_width=True, type="primary"):
            if u_id_input in USER_DB:
                user_info = USER_DB[u_id_input]
                # str() comparison to handle numeric passwords like '28773151'
                if str(user_info.get("key")) == u_pwd_input:
                    st.session_state.authenticated = True
                    st.session_state.user_id = u_id_input
                    st.session_state.user_role = user_info.get("role", "Buyer")
                    logger(u_id_input, "Login", "Success")
                    st.rerun()
                else:
                    st.error("Access Denied: Incorrect Key")
            else:
                st.error("Access Denied: Invalid User ID")

else:
    # ── 5. DASHBOARD (RESTORING ZOHO/MONDAY FEATURES) ─────────────────────────
    role = st.session_state.user_role
    user_id = st.session_state.user_id
    
    st.sidebar.title("Navigation")
    if st.sidebar.button("Secure Logout"):
        st.session_state.authenticated = False
        st.rerun()

    st.title(f"{role} Portal")

    if role == "Admin":
        # Restoration of the multi-functional dashboard
        t1, t2, t3, t4 = st.tabs(["Push Disclosure", "Assign Files", "System Audit", "User Management"])
        
        with t1:
            st.subheader("Project Disclosure & Structure")
            current_disc = ""
            if os.path.exists(DISCLOSURE_FILE):
                with open(DISCLOSURE_FILE, "r") as f: current_disc = f.read()
            
            new_disc = st.text_area("Update Deal Structure / Disclosures", value=current_disc, height=300)
            if st.button("Broadcast Update"):
                with open(DISCLOSURE_FILE, "w") as f: f.write(new_disc)
                logger(user_id, "Update Disclosure", "Broadcasting new structure")
                st.success("Disclosure updated for all users.")

        with t2:
            st.subheader("Secure Document Distribution")
            col1, col2 = st.columns(2)
            with col1:
                target = st.selectbox("Assign to User", options=list(USER_DB.keys()))
                desc = st.text_input("Note / Status (e.g., 'Awaiting Signature')")
            with col2:
                up_files = st.file_uploader("Upload Docs", accept_multiple_files=True)
            
            if st.button("Secure & Assign") and up_files:
                for f in up_files:
                    path = os.path.join(VAULT_BASE, "buyer_docs", f"ENCR_{target}_{f.name}")
                    save_encrypted(path, f.getbuffer(), desc)
                logger(user_id, "Assign Files", f"Sent to {target}")
                st.success(f"Files encrypted and sent to {target}.")

        with t3:
            st.subheader("Audit Trail")
            if os.path.exists(AUDIT_FILE):
                df = pd.read_csv(AUDIT_FILE)
                st.dataframe(df.sort_values(by="Timestamp", ascending=False), use_container_width=True)
            else:
                st.info("No audit logs yet.")

        with t4:
            st.subheader("Authorized Users")
            st.table(pd.DataFrame.from_dict(USER_DB, orient='index')[['role']])

    elif role == "Buyer":
        # Restoration of the clean, actionable buyer view
        st.subheader("Strategic Assets & Documents")
        
        # Display the deal disclosure from Admin
        if os.path.exists(DISCLOSURE_FILE):
            with st.expander("📄 View Deal Structure & Disclosures", expanded=True):
                with open(DISCLOSURE_FILE, "r") as f:
                    st.markdown(f.read())

        st.divider()

        doc_dir = os.path.join(VAULT_BASE, "buyer_docs")
        docs = [f for f in os.listdir(doc_dir) if f.startswith(f"ENCR_{user_id}_")]
        
        if not docs:
            st.info("Your vault is currently empty. Assets will appear here once assigned.")
        
        for i, d in enumerate(docs):
            note = get_meta(d)
            data = read_encrypted(os.path.join(doc_dir, d))
            clean_name = d.replace(f"ENCR_{user_id}_", "")
            
            with st.container():
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.write(f"**{clean_name}**")
                    st.caption(f"Status/Note: {note}")
                with c2:
                    st.download_button("Download", data, file_name=clean_name, key=f"dl_{i}", use_container_width=True)
                st.markdown("---")
