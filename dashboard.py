import streamlit as st
from streamlit_autorefresh import st_autorefresh
import os
import glob
from datetime import datetime
from PIL import Image

# ── 1. CONFIG & DIRECTORIES ────────────────────────────────────────────────
st.set_page_config(page_title="Utah Land & Property", layout="wide", initial_sidebar_state="collapsed")
st_autorefresh(interval=600000, key="ulp_refresh")

# Ensure directories exist
for folder in ["vault/general", "vault/buyer_docs", "vault/property_images"]:
    if not os.path.exists(folder):
        os.makedirs(folder)

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_role" not in st.session_state:
    st.session_state.user_role = None

# ── 2. AUTHENTICATION GATE (NO DROPDOWN) ───────────────────────────────────
if not st.session_state.authenticated:
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@900&family=Oswald:wght@500;700&display=swap');
        .stApp { background-color: #f8f9fa !important; }
        header, footer, [data-testid="stHeader"] { display: none !important; }
        .viewport-top-container { margin-top: -5vh; text-align: center; width: 100%; }
        .brand-title { font-family: 'Inter', sans-serif; font-size: 70px; font-weight: 900; color: #1a3c6d; line-height: 1.0; }
        .brand-subtitle { font-family: 'Oswald', sans-serif; letter-spacing: 3px; color: #6b7280; margin-bottom: 2rem; }
    </style>
    <div class="viewport-top-container">
        <div class="brand-title">Utah Land & Property</div>
        <div class="brand-subtitle">Strategic Asset Protection Framework</div>
    </div>
    """, unsafe_allow_html=True)

    _, col_mid, _ = st.columns([1, 1.2, 1])
    with col_mid:
        st.write("###")
        pwd = st.text_input("Private Access Key", type="password", placeholder="Enter Encrypted Key")
        
        if st.button("Authorize Access", use_container_width=True, type="primary"):
            # Checks if the key exists in the secrets dictionary
            keys_dict = st.secrets["access_keys"] # Returns {key: role}
            if pwd in keys_dict:
                st.session_state.authenticated = True
                st.session_state.user_role = keys_dict[pwd]
                st.rerun()
            else:
                st.error("Access Denied: Invalid Private Key.")

# ── 3. PROTECTED PORTAL CONTENT ──────────────────────────────────────────────
else:
    role = st.session_state.user_role
    
    # --- HEADER & LOGOUT ---
    col_a, col_b = st.columns([0.8, 0.2])
    with col_a:
        st.title(f"{role} Portal")
    with col_b:
        if st.button("Secure Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

    # --- SECTION: PROPERTY VISUALS (Visible to All) ---
    st.subheader("Property Gallery")
    img_files = glob.glob("vault/property_images/*")
    if img_files:
        # Display images in a grid
        cols = st.columns(3)
        for idx, img_path in enumerate(img_files):
            cols[idx % 3].image(img_path, use_container_width=True)
    else:
        st.info("No property images uploaded yet.")

    st.markdown("---")

    # --- SECTION: DOCUMENT ACCESS (Role Based) ---
    st.subheader("Asset Vault")

    if role == "Buyer":
        st.write("#### Documents Requiring Your Signature")
        buyer_files = os.listdir("vault/buyer_docs")
        if buyer_files:
            for f in buyer_files:
                with open(f"vault/buyer_docs/{f}", "rb") as file:
                    st.download_button(f"📄 Download & Sign: {f}", file, file_name=f)
        else:
            st.success("You are all caught up. No pending documents.")

    elif role in ["Admin", "Agent", "Escrow", "Title", "Servicer"]:
        # Upload Section
        st.write(f"#### {role} Management: Upload Documentation")
        
        # Admin & Agent can upload property images
        if role in ["Admin", "Agent"]:
            img_upload = st.file_uploader("Upload Property Photos", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
            if img_upload:
                for img in img_upload:
                    with open(f"vault/property_images/{img.name}", "wb") as f:
                        f.write(img.getbuffer())
                st.success("Gallery Updated.")

        # Specific Buyer Doc Upload (Targeted visibility)
        st.write("---")
        target = st.radio("Target Destination:", ["General Vault", "Buyer's Signature Folder"])
        docs = st.file_uploader("Upload Legal/Financial Docs", accept_multiple_files=True)
        
        if docs:
            folder = "vault/buyer_docs" if target == "Buyer's Signature Folder" else "vault/general"
            for d in docs:
                with open(f"{folder}/{d.name}", "wb") as f:
                    f.write(d.getbuffer())
            st.success(f"Archived to {target}")

    # --- ADMIN VIEW ALL ---
    if role == "Admin":
        with st.expander("Master File List (Admin Only)"):
            all_files = glob.glob("vault/**/*", recursive=True)
            st.write(all_files)
