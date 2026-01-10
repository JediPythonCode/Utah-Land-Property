import streamlit as st
from streamlit_autorefresh import st_autorefresh
import os
import json
import pandas as pd
from datetime import datetime
from cryptography.fernet import Fernet

# ── 1. CONFIG & SECURE ENCRYPTION ────────────────────────────────────────────
st.set_page_config(
    page_title="Utah Land & Property",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Prevents DuplicateElementKey error on rerun
if "refresh_initialized" not in st.session_state:
    st_autorefresh(interval=600000, key="ulp_refresh")
    st.session_state.refresh_initialized = True

def initialize_system():
    """Validates presence of key and initializes User Database."""
    try:
        key = st.secrets.get("secret_key")
        users = st.secrets.get("users")
        
        if not key or not users:
            st.error("🚨 SYSTEM ERROR: secrets.toml is missing 'secret_key' or 'users' section.")
            st.stop()
            
        return Fernet(key.encode()), users
    except Exception:
        st.error("🚨 SYSTEM CRITICAL: Could not read secrets.toml file.")
        st.stop()

# Global variables loaded once
fernet, USER_DB = initialize_system()

# ── 2. BRANDING & STYLING ──────────────────────────────────────────────────
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&family=Oswald:wght@500;700&display=swap');
        .stApp { background-color: #ffffff !important; color: #1a1a1a !important; }
        h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown {
            color: #1a3c6d !important; font-family: 'Inter', sans-serif; font-weight: 600;
        }
        .viewport-top-container { 
            display: flex; flex-direction: column; justify-content: center; 
            align-items: center; min-height: 25vh; padding: 20px; text-align: center; width: 100%; 
        }
        .brand-title { 
            font-family: 'Inter', sans-serif !important; font-size: clamp(32px, 10vw, 78px) !important; 
            font-weight: 900 !important; color: #1a3c6d !important; letter-spacing: -1.5px !important; 
            margin-bottom: 0px !important; line-height: 1.1;
        }
        .brand-subtitle { 
            font-family: 'Oswald', sans-serif !important; font-size: 1rem !important; 
            color: #6b7280 !important; letter-spacing: 2px !important; margin-top: 10px !important;
        }
        .pulse-lock { 
            height: 10px; width: 10px; background: #10b981; border-radius: 50%; 
            display: inline-block; margin-right: 8px; box-shadow: 0 0 10px rgba(16,185,129,0.5); 
            animation: pulse 2s infinite; 
        }
        @keyframes pulse { 
            0% { box-shadow: 0 0 0 0 rgba(16,185,129,0.7); } 
            70% { box-shadow: 0 0 0 10px rgba(16,185,129,0); } 
            100% { box-shadow: 0 0 0 0 rgba(16,185,129,0); } 
        }
        header, footer, [data-testid="stHeader"] { display: none !important; }
        @media (max-width: 640px) {
            .stButton button { width: 100% !important; height: 3rem; }
        }
    </style>
""", unsafe_allow_html=True)

# ── 3. CORE LOGIC ────────────────────────────────────────────────────────────
VAULT_BASE = "vault"
DISCLOSURE_FILE = os.path.join(VAULT_BASE, "general", "deal_structure.txt")
AUDIT_FILE = os.path.join(VAULT_BASE, "general", "audit_log.csv")

for folder in ["general", "buyer_docs", "property_images", "metadata"]:
    os.makedirs(os.path.join(VAULT_BASE, folder), exist_ok=True)

def logger(user, action, details):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = pd.DataFrame([[timestamp, user, action, str(details)]], columns=["Timestamp", "User", "Action", "Details"])
    log_entry.to_csv(AUDIT_FILE, mode='a', header=not os.path.exists(AUDIT_FILE), index=False)

def save_encrypted(file_path, data, description=""):
    encrypted_data = fernet.encrypt(data)
    with open(file_path, "wb") as f: f.write(encrypted_data)
    meta_path = os.path.join(VAULT_BASE, "metadata", os.path.basename(file_path) + ".json")
    with open(meta_path, "w") as f:
        json.dump({"description": description, "uploaded_at": datetime.now().isoformat()}, f)

def read_encrypted(file_path):
    try:
        with open(file_path, "rb") as f: return fernet.decrypt(f.read())
    except Exception: return None

def get_meta(file_path):
    meta_path = os.path.join(VAULT_BASE, "metadata", os.path.basename(file_path) + ".json")
    if os.path.exists(meta_path):
        with open(meta_path, "r") as f: return json.load(f).get("description", "No description provided.")
    return "No description provided."

def load_disclosure():
    if os.path.exists(DISCLOSURE_FILE):
        with open(DISCLOSURE_FILE, "r") as f: return f.read()
    return "Standard Disclosure: All deals subject to underwriting."

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# ── 4. THE UI FLOW ───────────────────────────────────────────────────────────
if not st.session_state.authenticated:
    st.markdown("""
        <div class="viewport-top-container">
            <div class="brand-title">Utah Land & Property</div>
            <div class="brand-subtitle">Strategic Asset Protection Framework</div>
            <div style="margin-top: 15px;">
                <span class="pulse-lock"></span>
                <span style="color:#1a3c6d; font-family:'Oswald'; font-size: 0.9rem; letter-spacing:1px;">SECURE CLIENT PORTAL</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    _, col_mid, _ = st.columns([1, 5, 1]) 
    with col_mid:
        u_id = st.text_input("User ID", placeholder="Username", label_visibility="collapsed")
        u_pwd = st.text_input("Key", type="password", placeholder="Access Key", label_visibility="collapsed")
        
        if st.button("Access Portal", use_container_width=True, type="primary"):
            # Use the global USER_DB loaded at the start
            if u_id in USER_DB:
                if str(USER_DB[u_id]["key"]) == u_pwd:
                    st.session_state.authenticated = True
                    st.session_state.user_id = u_id
                    st.session_state.user_role = USER_DB[u_id]["role"]
                    logger(u_id, "Login", "Success")
                    st.rerun()
                else:
                    st.error("Invalid Access Key")
                    logger(u_id, "Login Attempt", "Incorrect Password")
            else: 
                st.error("User ID Not Recognized")
                logger(u_id if u_id else "Unknown", "Login Attempt", "ID Not Found")

else:
    # ── 5. DASHBOARD ────────────────────────────────────────────────────────
    role = st.session_state.user_role
    user_id = st.session_state.user_id

    st.title(f"{role} Portal")
    st.info(f"🔔 **Status:** {load_disclosure()}")
    
    if st.sidebar.button("Secure Logout"):
        st.session_state.authenticated = False
        st.rerun()

    if role == "Admin":
        t1, t2, t3 = st.tabs(["Update Disclosure", "Upload & Assign", "Audit Logs"])
        with t1:
            new_disc = st.text_area("Live Portal Message", value=load_disclosure(), height=120)
            if st.button("Publish Update"):
                with open(DISCLOSURE_FILE, "w") as f: f.write(new_disc)
                st.rerun()
        with t2:
            target = st.text_input("Target User ID")
            file_desc = st.text_input("File Note")
            up_files = st.file_uploader("Choose Documents", accept_multiple_files=True)
            if st.button("Encrypt & Send") and up_files and target:
                for f in up_files:
                    path = os.path.join(VAULT_BASE, "buyer_docs", f"ENCR_{target}_{f.name}")
                    save_encrypted(path, f.getbuffer(), file_desc)
                st.success("Files assigned.")
        with t3:
            if os.path.exists(AUDIT_FILE):
                st.dataframe(pd.read_csv(AUDIT_FILE).tail(20), use_container_width=True)

    elif role == "Buyer":
        st.subheader("Your Secure Documents")
        doc_dir = os.path.join(VAULT_BASE, "buyer_docs")
        docs = [f for f in os.listdir(doc_dir) if user_id in f]
        if docs:
            for i, d in enumerate(docs):
                desc = get_meta(d)
                data = read_encrypted(os.path.join(doc_dir, d))
                with st.container():
                    st.markdown(f"**{d.split('_', 2)[-1]}**")
                    st.caption(f"Note: {desc}")
                    st.download_button("Download", data, file_name=d, key=f"dl_{i}")
                    st.markdown("---")
        else:
            st.info("No documents assigned.")

    # Property Visuals
    st.markdown("---")
    st.subheader("Property Visuals")
    img_dir = os.path.join(VAULT_BASE, "property_images")
    images = [f for f in os.listdir(img_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if images:
        cols = st.columns(2)
        for i, img in enumerate(images):
            cols[i % 2].image(os.path.join(img_dir, img), use_container_width=True)
