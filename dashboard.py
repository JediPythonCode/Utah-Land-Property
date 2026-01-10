import streamlit as st
from streamlit_autorefresh import st_autorefresh
import os
import glob
from datetime import datetime

# ── 1. CONFIG & PERSISTENCE ────────────────────────────────────────────────
st.set_page_config(
    page_title="Utah Land & Property",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st_autorefresh(interval=600000, key="ulp_refresh")

# Ensure vault directories exist
for folder in ["vault/general", "vault/buyer_docs", "vault/property_images"]:
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_role" not in st.session_state:
    st.session_state.user_role = None

# ── 2. AUTHENTICATION GATE (RECENTERED & RESTORED) ──────────────────────────
if not st.session_state.authenticated:
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&family=Oswald:wght@500;700&display=swap');
        
        .stApp { background-color: #f8f9fa !important; }
        header, footer, [data-testid="stHeader"] { display: none !important; }
        
        .viewport-top-container {
            margin-top: -10vh; 
            text-align: center;
            width: 100%;
        }

        .brand-title {
            font-family: 'Inter', sans-serif !important;
            font-size: clamp(42px, 10vw, 78px) !important;
            font-weight: 900 !important;
            color: #1a3c6d !important;
            letter-spacing: -1.5px !important;
            margin-bottom: 0px !important;
            line-height: 1.0 !important;
        }
        .brand-subtitle {
            font-family: 'Oswald', sans-serif !important;
            font-size: 1.35rem !important;
            color: #6b7280 !important;
            letter-spacing: 3px !important;
            font-weight: 500 !important;
            margin-top: 5px !important;
            margin-bottom: 2rem !important;
        }
        .framework-text {
            color: #4b5563 !important;
            font-size: 1.05rem !important;
            max-width: 700px !important;
            margin: 0 auto 2.5rem !important;
            line-height: 1.7 !important;
            font-family: 'Inter', sans-serif !important;
        }
        
        .pulse-lock {
            height: 12px; width: 12px;
            background: #10b981;
            border-radius: 50%;
            display: inline-block;
            margin-right: 12px;
            box-shadow: 0 0 12px rgba(16,185,129,0.5);
            animation: pulse 2s infinite;
            vertical-align: middle;
        }
        @keyframes pulse {
            0%   { box-shadow: 0 0 0 0 rgba(16,185,129,0.7); }
            70%  { box-shadow: 0 0 0 12px rgba(16,185,129,0); }
            100% { box-shadow: 0 0 0 0 rgba(16,185,129,0); }
        }
        .access-text {
            font-family: 'Oswald', sans-serif !important;
            font-size: 1.1rem !important;
            color: #1a3c6d !important;
            font-weight: 700 !important;
            letter-spacing: 2px !important;
            vertical-align: middle;
        }
    </style>
    
    <div class="viewport-top-container">
        <div class="brand-title">Utah Land & Property</div>
        <div class="brand-subtitle">Strategic Asset Protection Framework</div>
        
        <div class="framework-text">
            Privacy Creation Preservation • Creative Land & Real Estate Deal Structure
            <br><br>
            <strong>Secure Client Portal</strong> — Encrypted access only.
        </div>

        <div style="margin-bottom: 2rem;">
            <span class="pulse-lock"></span>
            <span class="access-text">CLIENT SECURE ACCESS</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Login Input Column
    _, col_mid, _ = st.columns([1, 1.4, 1])
    with col_mid:
        pwd = st.text_input("Key", type="password", placeholder="Enter Access Key", label_visibility="collapsed")
        if st.button("Access Portal", use_container_width=True, type="primary"):
            keys_dict = st.secrets.get("access_keys", {})
            if pwd in keys_dict:
                st.session_state.authenticated = True
                st.session_state.user_role = keys_dict[pwd]
                st.rerun()
            else:
                st.error("Invalid Security Key")

# ── 3. PROTECTED PORTAL CONTENT ──────────────────────────────────────────────
else:
    role = st.session_state.user_role
    
    # Header & Logout
    st.sidebar.title(f"🔐 {role} Session")
    if st.sidebar.button("Secure Logout"):
        st.session_state.authenticated = False
        st.rerun()

    # --- 3a. PROPERTY GALLERY (Above All Content) ---
    st.title(f"{role} Dashboard")
    st.subheader("Property Visuals")
    
    images = glob.glob("vault/property_images/*")
    if images:
        cols = st.columns(4)
        for idx, img_path in enumerate(images):
            cols[idx % 4].image(img_path, use_container_width=True)
    else:
        st.info("No property images uploaded yet.")

    st.markdown("---")

    # --- 3b. ACTION AREA: BUYER SIGNATURES ---
    if role == "Buyer":
        st.subheader("Action Required: Documents for Signature")
        buyer_docs = os.listdir("vault/buyer_docs")
        if buyer_docs:
            for f_name in buyer_docs:
                with open(f"vault/buyer_docs/{f_name}", "rb") as f_obj:
                    st.download_button(f"📄 Download & Sign: {f_name}", f_obj, file_name=f_name)
        else:
            st.success("No pending documents for signature.")

    # --- 3c. ACTION AREA: MANAGEMENT (Admin, Agent, etc.) ---
    else:
        st.subheader("Document Upload & Archival")
        
        # UI for routing files
        col_dest, col_type = st.columns(2)
        with col_dest:
            target = st.radio("Destination Folder", ["General Vault", "Buyer's Signature Folder"], horizontal=True)
        with col_type:
            if role in ["Admin", "Agent"]:
                upload_kind = st.radio("Asset Type", ["Document", "Property Image"], horizontal=True)
            else:
                upload_kind = "Document"

        uploaded_files = st.file_uploader("Securely upload assets (PDF, JPG, PNG, DOCX)", accept_multiple_files=True)

        if uploaded_files:
            for file in uploaded_files:
                # Determine folder destination
                if upload_kind == "Property Image":
                    save_path = "vault/property_images"
                elif target == "Buyer's Signature Folder":
                    save_path = "vault/buyer_docs"
                else:
                    save_path = "vault/general"
                
                # Write to disk
                with open(os.path.join(save_path, file.name), "wb") as f:
                    f.write(file.getbuffer())
            
            st.success(f"Successfully archived {len(uploaded_files)} assets.")
            st.rerun()

    # --- 3d. ADMIN MASTER VIEW ---
    if role == "Admin":
        with st.expander("Admin Master File View"):
            st.write("All files currently in encrypted storage:")
            st.json(glob.glob("vault/**/*", recursive=True))

    st.markdown(f"**Role Permission:** As an **{role}**, you have encrypted write-access to the property data-room.")
