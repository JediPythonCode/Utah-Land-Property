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

# Fix for StreamlitDuplicateElementKey: Only initialize refresh once per session
if "refresh_initialized" not in st.session_state:
    st_autorefresh(interval=600000, key="ulp_refresh")
    st.session_state.refresh_initialized = True

def initialize_encryption():
    """Validates presence of key and initializes Fernet."""
    try:
        # App will ONLY run if 'secret_key' is in your secrets.toml
        key = st.secrets.get("secret_key")
        if not key:
            st.error("🚨 SYSTEM CRITICAL: Encryption Key Missing. Access Disabled.")
            st.stop()
        return Fernet(key.encode())
    except Exception:
        st.error("🚨 SYSTEM CRITICAL: Security Initialization Failed.")
        st.stop()

fernet = initialize_encryption()

# ── 2. BRANDING & STYLING (MOBILE OPTIMIZED) ────────────────────────────────
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&family=Oswald:wght@500;700&display=swap');
        
        .stApp { background-color: #ffffff !important; color: #1a1a1a !important; }
        
        h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown {
            color: #1a3c6d !important; font-family: 'Inter', sans-serif; font-weight: 600;
        }

        /* Responsive Branding Container */
        .viewport-top-container { 
            display: flex; flex-direction: column; justify-content: center; 
            align-items: center; min-height: 25vh; padding: 20px; 
            text-align: center; width: 100%; 
        }

        .brand-title { 
            font-family: 'Inter', sans-serif !important; 
            font-size: clamp(32px, 10vw, 78px) !important; 
            font-weight: 900 !important; color: #1a3c6d !important; 
            letter-spacing: -1.5px !important; margin-bottom: 0px !important; 
            line-height: 1.1;
        }

        .brand-subtitle { 
            font-family: 'Oswald', sans-serif !important; font-size: 1rem !important; 
            color: #6b7280 !important; letter-spacing: 2px !important; 
            margin-top: 10px !important;
        }

        .pulse-lock { 
            height: 10px; width: 10px; background: #10b981; border-radius: 50%; 
            display: inline-block; margin-right: 8px; 
            box-shadow: 0 0 10px rgba(16,185,129,0.5); animation: pulse 2s infinite; 
        }

        @keyframes pulse { 
            0% { box-shadow: 0 0 0 0 rgba(16,185,129,0.7); } 
            70% { box-shadow: 0 0 0 10px rgba(16,185,129,0); } 
            100% { box-shadow: 0 0 0 0 rgba(16,185,129,0); } 
        }

        .recent-file-card { 
            background: #ffffff; padding: 12px; border-radius: 8px; 
            border: 1px solid #e5e7eb; margin-bottom: 8px; 
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }

        header, footer, [data-testid="stHeader"] { display: none !important; }
        
        /* Mobile Target Improvements */
        @media (max-width: 640px) {
            .stButton button { width: 100% !important; height: 3rem; }
            .brand-subtitle { font-size: 0.8rem !important; }
        }
    </style>
""", unsafe_allow_html=True)

# ── 3. CORE LOGIC ────────────────────────────────────────────────────────────
VAULT_BASE = "vault"
DISCLOSURE_FILE = os.path.join(VAULT_BASE, "general", "deal_structure.txt")
AUDIT_FILE = os.path.join(VAULT_BASE, "general", "audit_log.csv")

# Create Directory structure
for folder in ["general", "buyer_docs", "property_images", "metadata"]:
    os.makedirs(os.path.join(VAULT_BASE, folder), exist_ok=True)

def logger(user, action, details):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = pd.DataFrame([[timestamp, user, action, str(details)]], columns=["Timestamp", "User", "Action", "Details"])
    log_entry.to_csv(AUDIT_FILE, mode='a', header=not os.path.exists(AUDIT_FILE), index=False)

def save_encrypted(file_path, data, description=""):
    """Encrypts file and saves optional description metadata."""
    encrypted_data = fernet.encrypt(data)
    with open(file_path, "wb") as f: 
        f.write(encrypted_data)
    
    # Save the description as a sidecar JSON file
    meta_path = os.path.join(VAULT_BASE, "metadata", os.path.basename(file_path) + ".json")
    with open(meta_path, "w") as f:
        json.dump({"description": description, "uploaded_at": datetime.now().isoformat()}, f)

def read_encrypted(file_path):
    try:
        with open(file_path, "rb") as f: 
            return fernet.decrypt(f.read())
    except Exception: 
        return None

def get_meta(file_path):
    meta_path = os.path.join(VAULT_BASE, "metadata", os.path.basename(file_path) + ".json")
    if os.path.exists(meta_path):
        try:
            with open(meta_path, "r") as f: 
                return json.load(f).get("description", "No description provided.")
        except: return "Metadata error."
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
    
    # Column configuration optimized for mobile-first tap targets
    _, col_mid, _ = st.columns([1, 5, 1]) 
    with col_mid:
        u_id = st.text_input("User ID", placeholder="Username", label_visibility="collapsed")
        u_pwd = st.text_input("Key", type="password", placeholder="Access Key", label_visibility="collapsed")
        if st.button("Access Portal", use_container_width=True, type="primary"):
            users = st.secrets.get("users", {})
            if u_id in users and str(users[u_id]["key"]) == u_pwd:
                st.session_state.authenticated = True
                st.session_state.user_id = u_id
                st.session_state.user_role = users[u_id]["role"]
                logger(u_id, "Login", "Success")
                st.rerun()
            else: 
                st.error("Access Denied")
                logger(u_id if u_id else "Anonymous", "Failed Login", "Invalid Creds")

else:
    # ── 5. DASHBOARD ────────────────────────────────────────────────────────
    role = st.session_state.user_role
    user_id = st.session_state.user_id

    st.title(f"{role} Portal")
    st.info(f"🔔 **Status:** {load_disclosure()}")
    
    if st.sidebar.button("Secure Logout"):
        st.session_state.authenticated = False
        st.rerun()

    # --- ROLE LOGIC ---
    if role == "Admin":
        t1, t2, t3 = st.tabs(["Update Disclosure", "Upload & Assign", "Audit Logs"])
        
        with t1:
            st.subheader("Global Disclosure Management")
            new_disc = st.text_area("Live Portal Message", value=load_disclosure(), height=120)
            if st.button("Publish Update"):
                with open(DISCLOSURE_FILE, "w") as f: f.write(new_disc)
                st.success("Disclosure Updated.")
                st.rerun()

        with t2:
            st.subheader("Secure File Assignment")
            target = st.text_input("Target User ID (matches User ID at login)")
            file_desc = st.text_input("File Note (What is this for?)")
            up_files = st.file_uploader("Choose Documents", accept_multiple_files=True)
            if st.button("Encrypt & Send") and up_files and target:
                for f in up_files:
                    path = os.path.join(VAULT_BASE, "buyer_docs", f"ENCR_{target}_{f.name}")
                    save_encrypted(path, f.getbuffer(), file_desc)
                st.success(f"Successfully assigned {len(up_files)} file(s) to {target}.")
                logger(user_id, "Admin Upload", f"To: {target}")

        with t3:
            st.subheader("System Activity")
            if os.path.exists(AUDIT_FILE):
                st.dataframe(pd.read_csv(AUDIT_FILE).tail(20), use_container_width=True)

    elif role == "Buyer":
        st.subheader("Your Secure Documents")
        doc_dir = os.path.join(VAULT_BASE, "buyer_docs")
        # List only files belonging to this specific User ID
        docs = [f for f in os.listdir(doc_dir) if user_id in f]
        
        if docs:
            for i, d in enumerate(docs):
                desc = get_meta(d)
                data = read_encrypted(os.path.join(doc_dir, d))
                with st.container():
                    col_file, col_dl = st.columns([3, 1])
                    with col_file:
                        st.markdown(f"**{d.split('_', 2)[-1]}**")
                        st.caption(f"Admin Note: {desc}")
                    with col_dl:
                        if data:
                            st.download_button(f"Download", data, file_name=d, key=f"dl_{i}")
                    st.markdown("---")
        else:
            st.info("No documents currently assigned to your account.")

    # Property Visuals Section - Optimized for Mobile
    st.markdown("---")
    st.subheader("Property Visuals")
    img_dir = os.path.join(VAULT_BASE, "property_images")
    images = [f for f in os.listdir(img_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if images:
        cols = st.columns(2) # 2 columns is best for mobile viewports
        for i, img in enumerate(images):
            cols[i % 2].image(os.path.join(img_dir, img), use_container_width=True)
