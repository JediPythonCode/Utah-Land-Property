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

if "refresh_initialized" not in st.session_state:
    st_autorefresh(interval=600000, key="ulp_refresh")
    st.session_state.refresh_initialized = True

def initialize_system():
    try:
        key = st.secrets.get("secret_key")
        # Pull the users section
        users_data = st.secrets.get("users")

        if not key or users_data is None:
            st.error("🚨 SYSTEM ERROR: secrets.toml is missing 'secret_key' or '[users]'.")
            st.stop()
        
        # Convert to a standard dictionary to ensure stability
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

# ── 3. CORE LOGIC ────────────────────────────────────────────────────────────
VAULT_BASE = "vault"
for folder in ["general", "buyer_docs", "property_images", "metadata"]:
    os.makedirs(os.path.join(VAULT_BASE, folder), exist_ok=True)

def logger(user, action, details):
    try:
        AUDIT_FILE = os.path.join(VAULT_BASE, "general", "audit_log.csv")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = pd.DataFrame([[timestamp, user, action, str(details)]], columns=["Timestamp", "User", "Action", "Details"])
        log_entry.to_csv(AUDIT_FILE, mode='a', header=not os.path.exists(AUDIT_FILE), index=False)
    except: pass

def save_encrypted(file_path, data, description=""):
    encrypted_data = fernet.encrypt(data)
    with open(file_path, "wb") as f: f.write(encrypted_data)
    meta_path = os.path.join(VAULT_BASE, "metadata", os.path.basename(file_path) + ".json")
    with open(meta_path, "w") as f: json.dump({"description": description}, f)

def read_encrypted(file_path):
    try:
        with open(file_path, "rb") as f: return fernet.decrypt(f.read())
    except: return None

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# ── 4. UI FLOW (STRICT CREDENTIAL CHECK) ──────────────────────────────────────
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
        # Use .lower() and .strip() to prevent casing or spacing errors
        u_id_input = st.text_input("User ID", placeholder="Enter Username", label_visibility="collapsed").strip().lower()
        u_pwd_input = st.text_input("Key", type="password", placeholder="Enter Access Key", label_visibility="collapsed").strip()

        if st.button("Access Portal", use_container_width=True, type="primary"):
            # Check if the user exists in USER_DB
            if u_id_input in USER_DB:
                user_info = USER_DB[u_id_input]
                # Compare as strings to ensure numeric keys work
                if str(user_info.get("key")) == u_pwd_input:
                    st.session_state.authenticated = True
                    st.session_state.user_id = u_id_input
                    st.session_state.user_role = user_info.get("role", "Buyer")
                    logger(u_id_input, "Login", "Success")
                    st.rerun()
                else:
                    st.error("Access Denied: Incorrect Key")
                    logger(u_id_input, "Auth", "Failed Key")
            else:
                st.error("Access Denied: Invalid User ID")
                # Optional: Uncomment the line below to debug what the app sees
                # st.write(f"DEBUG: App sees these IDs: {list(USER_DB.keys())}")

else:
    # ── 5. DASHBOARD ─────────────────────────────────────────────────────────
    role = st.session_state.user_role
    user_id = st.session_state.user_id
    st.title(f"{role} Portal")

    if st.sidebar.button("Secure Logout"):
        st.session_state.authenticated = False
        st.rerun()

    if role == "Admin":
        st.subheader("Admin Controls")
        target = st.text_input("Target User ID (e.g., buyer1)")
        up_files = st.file_uploader("Upload Documents", accept_multiple_files=True)
        if st.button("Secure & Assign") and up_files and target:
            for f in up_files:
                path = os.path.join(VAULT_BASE, "buyer_docs", f"ENCR_{target}_{f.name}")
                save_encrypted(path, f.getbuffer(), "Assigned by Admin")
            st.success("Files encrypted and assigned.")

    elif role == "Buyer":
        st.subheader("Your Secure Documents")
        doc_dir = os.path.join(VAULT_BASE, "buyer_docs")
        docs = [f for f in os.listdir(doc_dir) if user_id in f]
        if not docs:
            st.info("No documents currently assigned to your ID.")
        for i, d in enumerate(docs):
            data = read_encrypted(os.path.join(doc_dir, d))
            st.download_button(f"Download {d.replace('ENCR_'+user_id+'_', '')}", data, file_name=d, key=f"dl_{i}")
