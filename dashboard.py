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

if "refresh_initialized" not in st.session_state:
    st_autorefresh(interval=600000, key="ulp_refresh")
    st.session_state.refresh_initialized = True

def initialize_system():
    try:
        key = st.secrets.get("secret_key")
        users = st.secrets.get("users")
        if not key or not users:
            st.error("🚨 SYSTEM ERROR: secrets.toml missing 'secret_key' or 'users'.")
            st.stop()
        return Fernet(key.encode()), users
    except Exception:
        st.error("🚨 SYSTEM CRITICAL: Secrets file unreachable.")
        st.stop()

fernet, USER_DB = initialize_system()

# ── 2. BRANDING & STYLING (WITH MOBILE RESPONSIVENESS) ──────────────────────
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&family=Oswald:wght@500;700&display=swap');
        
        .stApp { background-color: #ffffff !important; color: #1a1a1a !important; }
        
        h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown {
            color: #1a3c6d !important; font-family: 'Inter', sans-serif; font-weight: 600;
        }

        /* Hide Streamlit elements for a clean portal look */
        header, footer, [data-testid="stHeader"] { display: none !important; }

        /* Branding Container */
        .viewport-top-container { 
            display: flex; flex-direction: column; justify-content: center; 
            align-items: center; min-height: 30vh; padding: 20px; 
            text-align: center; width: 100%; 
        }
        
        .brand-title { 
            font-family: 'Inter', sans-serif !important; 
            font-size: clamp(38px, 8vw, 78px) !important; 
            font-weight: 900 !important; color: #1a3c6d !important; 
            letter-spacing: -1.5px !important; margin-bottom: 0px !important; 
            line-height: 1.0 !important; 
        }
        
        .brand-subtitle { 
            font-family: 'Oswald', sans-serif !important; font-size: 1.25rem !important; 
            color: #6b7280 !important; letter-spacing: 3px !important; 
            margin-top: 10px !important; margin-bottom: 1rem !important; 
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

        /* MOBILE TWEAK: Ensure buttons and inputs are large enough for thumbs */
        @media (max-width: 768px) {
            .stButton button { 
                height: 3.5rem !important; 
                font-size: 1.1rem !important;
            }
            .stTextInput input {
                height: 3.5rem !important;
            }
            /* Override the [1, 1.6, 1] column desktop constraint on mobile */
            [data-testid="column"] {
                width: 100% !important;
                flex: 1 1 100% !important;
            }
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
        json.dump({"description": description}, f)

def read_encrypted(file_path):
    try:
        with open(file_path, "rb") as f: return fernet.decrypt(f.read())
    except: return None

def get_meta(file_path):
    meta_path = os.path.join(VAULT_BASE, "metadata", os.path.basename(file_path) + ".json")
    if os.path.exists(meta_path):
        with open(meta_path, "r") as f: return json.load(f).get("description", "")
    return ""

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# ── 4. UI FLOW (DESKTOP RATIO + MOBILE OVERRIDE) ─────────────────────────────
if not st.session_state.authenticated:
    st.markdown("""
        <div class="viewport-top-container">
            <div class="brand-title">Utah Land & Property</div>
            <div class="brand-subtitle">Strategic Asset Protection Framework</div>
            <div style="margin-bottom: 2rem;">
                <span class="pulse-lock"></span>
                <span style="color:#1a3c6d; font-family:'Oswald'; letter-spacing:2px; font-size:0.9rem;">SECURE CLIENT PORTAL</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Desktop layout: Center 1.6 width. Mobile CSS handles the override to 100% width.
    _, col_mid, _ = st.columns([1, 1.6, 1])
    with col_mid:
        u_id = st.text_input("User ID", placeholder="Username", label_visibility="collapsed")
        u_pwd = st.text_input("Key", type="password", placeholder="Access Key", label_visibility="collapsed")
        if st.button("Access Portal", use_container_width=True, type="primary"):
            if u_id in USER_DB and str(USER_DB[u_id]["key"]) == u_pwd:
                st.session_state.authenticated = True
                st.session_state.user_id = u_id
                st.session_state.user_role = USER_DB[u_id]["role"]
                logger(u_id, "Login", "Success")
                st.rerun()
            else:
                st.error("Access Denied")
                logger(u_id if u_id else "Unknown", "Auth", "Failed")

else:
    # ── 5. DASHBOARD ────────────────────────────────────────────────────────
    role = st.session_state.user_role
    user_id = st.session_state.user_id

    st.title(f"{role} Portal")
    
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()

    if role == "Admin":
        t1, t2 = st.tabs(["Assignment", "Audit"])
        with t1:
            target = st.text_input("Assign to User ID")
            desc = st.text_input("File Memo (Description)")
            up_files = st.file_uploader("Upload Secured Documents", accept_multiple_files=True)
            if st.button("Encrypt & Assign") and up_files and target:
                for f in up_files:
                    path = os.path.join(VAULT_BASE, "buyer_docs", f"ENCR_{target}_{f.name}")
                    save_encrypted(path, f.getbuffer(), desc)
                st.success("Documents secured and assigned.")

    elif role == "Buyer":
        st.subheader("Protected Documents")
        doc_dir = os.path.join(VAULT_BASE, "buyer_docs")
        docs = [f for f in os.listdir(doc_dir) if user_id in f]
        if not docs:
            st.info("No documents currently shared.")
        for i, d in enumerate(docs):
            note = get_meta(d)
            data = read_encrypted(os.path.join(doc_dir, d))
            with st.container():
                st.markdown(f"**📂 {d.split('_', 2)[-1]}**")
                if note: st.write(f"_{note}_")
                st.download_button("Download Secure File", data, file_name=d, key=f"dl_{i}", use_container_width=True)
                st.markdown("---")

    # Property Visuals
    img_dir = os.path.join(VAULT_BASE, "property_images")
    if os.path.exists(img_dir):
        images = [f for f in os.listdir(img_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if images:
            st.subheader("Asset Gallery")
            cols = st.columns(2)
            for i, img in enumerate(images):
                cols[i % 2].image(os.path.join(img_dir, img), use_container_width=True)
