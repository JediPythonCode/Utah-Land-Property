import streamlit as st
from streamlit_autorefresh import st_autorefresh
import os
import glob
import pandas as pd
from datetime import datetime
from cryptography.fernet import Fernet

# ── 1. HARDENED CONFIG & ENCRYPTION ──────────────────────────────────────────
st.set_page_config(page_title="Utah Land & Property", layout="wide", initial_sidebar_state="collapsed")
st_autorefresh(interval=600000, key="ulp_refresh")

# Initialize Encryption (Key should be stored in st.secrets for production)
if "secret_key" not in st.secrets:
    # For local testing only; in production, put a real key in secrets.toml
    ENCR_KEY = Fernet.generate_key() 
else:
    ENCR_KEY = st.secrets["secret_key"].encode()

fernet = Fernet(ENCR_KEY)

# Persistence Files
DISCLOSURE_FILE = "vault/general/deal_structure.txt"
AUDIT_FILE = "vault/general/audit_log.csv"

for folder in ["vault/general", "vault/buyer_docs", "vault/property_images"]:
    os.makedirs(folder, exist_ok=True)

# ── 2. SECURITY FUNCTIONS ─────────────────────────────────────────────────────
def logger(user, action, details):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = pd.DataFrame([[timestamp, user, action, details]], 
                             columns=["Timestamp", "User", "Action", "Details"])
    log_entry.to_csv(AUDIT_FILE, mode='a', header=not os.path.exists(AUDIT_FILE), index=False)

def save_encrypted(file_path, data):
    encrypted_data = fernet.encrypt(data)
    with open(file_path, "wb") as f:
        f.write(encrypted_data)

def read_encrypted(file_path):
    with open(file_path, "rb") as f:
        return fernet.decrypt(f.read())

def load_disclosure():
    if os.path.exists(DISCLOSURE_FILE):
        with open(DISCLOSURE_FILE, "r") as f: return f.read()
    return "Standard Disclosure: Secure Underwriting in Progress."

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_id = None
    st.session_state.user_role = None

# ── 3. AUTHENTICATION GATE (HARDENED) ─────────────────────────────────────────
if not st.session_state.authenticated:
    # ... [KEEP YOUR ORIGINAL CSS AND HERO HTML HERE] ...
    st.markdown("""<style>/* Your original CSS */</style>""", unsafe_allow_html=True)
    
    _, col_mid, _ = st.columns([1, 1.6, 1])
    with col_mid:
        # We now expect an individual User ID and a Security Key
        user_id = st.text_input("User ID", placeholder="Username", label_visibility="collapsed")
        pwd = st.text_input("Key", type="password", placeholder="Access Key", label_visibility="collapsed")
        
        if st.button("Access Portal", use_container_width=True, type="primary"):
            # Check against Individual User Keys in secrets
            users = st.secrets.get("users", {}) # Format: {"john_doe": {"key": "123", "role": "Buyer"}}
            if user_id in users and users[user_id]["key"] == pwd:
                st.session_state.authenticated = True
                st.session_state.user_id = user_id
                st.session_state.user_role = users[user_id]["role"]
                logger(user_id, "Login", "Authenticated Successfully")
                st.rerun()
            else:
                st.error("Invalid Credentials")

# ── 4. PROTECTED CONTENT ──────────────────────────────────────────────────────
else:
    role = st.session_state.user_role
    user_id = st.session_state.user_id
    
    # Active Disclosure Banner
    st.warning(f"🔔 **Deal Structure:** {load_disclosure()}")

    # --- BUYER LOGIC (HARDENED) ---
    if role == "Buyer":
        st.subheader("Step 1: Financial Underwriting")
        with st.expander("📊 Run Analysis", expanded=True):
            inc = st.number_input("Monthly Income ($)", min_value=1, value=5000)
            debt = st.number_input("Monthly Debt ($)", min_value=0, value=1500)
            dti = (debt / inc) * 100
            if st.button("Log Underwriting Data"):
                logger(user_id, "Underwriting", f"DTI Result: {dti:.1f}%")
                st.success("Analysis logged for Admin.")

        st.subheader("Step 2: Secure Document Upload")
        vet_file = st.file_uploader("Upload ID / Proof of Funds")
        if vet_file:
            # Files are now ENCRYPTED before saving
            file_name = f"ENCR_{user_id}_{vet_file.name}"
            save_encrypted(os.path.join("vault/general", file_name), vet_file.getbuffer())
            logger(user_id, "Upload", file_name)
            st.success("File encrypted and stored.")

        st.subheader("Step 3: Signature Vault")
        # Logic to show ONLY files that have user_id in the name
        docs = [f for f in os.listdir("vault/buyer_docs") if user_id in f]
        if docs:
            for d in docs:
                data = read_encrypted(os.path.join("vault/buyer_docs", d))
                st.download_button(f"📄 Download {d}", data, file_name=d.replace("ENCR_", ""))
        else:
            st.info("No documents released for your ID yet.")

    # --- ADMIN LOGIC (HARDENED) ---
    else:
        st.subheader("Management Dashboard")
        with st.expander("📝 Update Deal Structure"):
            new_note = st.text_area("Disclosure Text")
            if st.button("Push to All Users"):
                with open(DISCLOSURE_FILE, "w") as f: f.write(new_note)
                logger(user_id, "Update Disclosure", "Changed Deal Structure")
                st.rerun()

        with st.expander("🛡️ System Audit (RBAC)"):
            if os.path.exists(AUDIT_FILE):
                st.dataframe(pd.read_csv(AUDIT_FILE).tail(20), use_container_width=True)

        # Admin Uploader (Encrypts files)
        st.write("---")
        target_user = st.text_input("Assign to User ID (e.g., john_doe)")
        up_files = st.file_uploader("Upload for Buyer", accept_multiple_files=True)
        if up_files and target_user:
            for f in up_files:
                save_encrypted(os.path.join("vault/buyer_docs", f"ENCR_{target_user}_{f.name}"), f.getbuffer())
            st.success(f"Encrypted files assigned to {target_user}")

    if st.button("Logout"):
        logger(user_id, "Logout", "Session ended")
        st.session_state.authenticated = False
        st.rerun()
