import streamlit as st
from streamlit_autorefresh import st_autorefresh
import os
import glob
from datetime import datetime

# ── 1. CONFIG & DIRECTORIES ────────────────────────────────────────────────
st.set_page_config(
    page_title="Utah Land & Property",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st_autorefresh(interval=600000, key="ulp_refresh")

# Initialize directories
for folder in ["vault/general", "vault/buyer_docs", "vault/property_images"]:
    if not os.path.exists(folder):
        os.makedirs(folder)

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_role" not in st.session_state:
    st.session_state.user_role = None

# ── 2. AUTHENTICATION GATE (RESTORED DESIGN) ────────────────────────────────
if not st.session_state.authenticated:
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&family=Oswald:wght@500;700&display=swap');
        
        .stApp { background-color: #f8f9fa !important; }
        header, footer, [data-testid="stHeader"] { display: none !important; }
        
        .viewport-top-container {
            margin-top: 5vh;
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

    # Login Input
    _, col_mid, _ = st.columns([1, 1.4, 1])
    with col_mid:
        pwd = st.text_input("Key", type="password", placeholder="Enter Private Access Key", label_visibility="collapsed")
        if st.button("Authorize Portal Access", use_container_width=True, type="primary"):
            keys_dict = st.secrets.get("access_keys", {})
            if pwd in keys_dict:
                st.session_state.authenticated = True
                st.session_state.user_role = keys_dict[pwd]
                st.rerun()
            else:
                st.error("Invalid Security Key")

# ── 3. PROTECTED CONTENT ──────────────────────────────────────────────────
else:
    role = st.session_state.user_role
    
    # Simple Navigation / Header
    col_title, col_logout = st.columns([0.8, 0.2])
    with col_title:
        st.title(f"{role} Dashboard")
    with col_logout:
        if st.sidebar.button("Secure Logout"):
            st.session_state.authenticated = False
            st.rerun()

    # --- PROPERTY GALLERY (Visuals Above) ---
    st.subheader("Property Images")
    img_list = glob.glob("vault/property_images/*")
    if img_list:
        cols = st.columns(3)
        for idx, img_p in enumerate(img_list):
            cols[idx % 3].image(img_p, use_container_width=True)
    else:
        st.info("No property images available.")

    st.markdown("---")

    # --- ROLE-SPECIFIC ACCESS ---
    if role == "Buyer":
        st.subheader("Action Required: Documents for Signature")
        buyer_docs = os.listdir("vault/buyer_docs")
        if buyer_docs:
            for f_name in buyer_docs:
                with open(f"vault/buyer_docs/{f_name}", "rb") as f_obj:
                    st.download_button(f"📄 Review & Sign: {f_name}", f_obj, file_name=f_name)
        else:
            st.success("No pending documents for signature.")

    else:
        # Admin, Agent, Escrow, Title, Servicer View
        st.subheader("Document Upload & Archival")
        
        # 1. Image Upload (Admin/Agent Only)
        if role in ["Admin", "Agent"]:
            with st.expander("Upload Property Images"):
                imgs = st.file_uploader("Upload photos for gallery", type=["jpg","png","jpeg"], accept_multiple_files=True)
                if imgs:
                    for img in imgs:
                        with open(f"vault/property_images/{img.name}", "wb") as f:
                            f.write(img.getbuffer())
                    st.rerun()

        # 2. General Document Upload
        st.markdown(f"> **Notice:** As an **{role}**, you have encrypted write-access to the property data-room.")
        
        target = st.radio("Destination Folder", ["General Vault", "Buyer's Signature Folder"], horizontal=True)
        docs = st.file_uploader("Securely upload assets (PDF, JPG, PNG, DOCX)", accept_multiple_files=True)

        if docs:
            dest = "vault/buyer_docs" if target == "Buyer's Signature Folder" else "vault/general"
            for d in docs:
                with open(os.path.join(dest, d.name), "wb") as f:
                    f.write(d.getbuffer())
            st.success(f"Successfully uploaded {len(docs)} files to {target}.")

    # 3. Master View for Admin
    if role == "Admin":
        with st.expander("View All Vault Files"):
            st.write("Current files in storage:")
            st.write(glob.glob("vault/**/*", recursive=True))
