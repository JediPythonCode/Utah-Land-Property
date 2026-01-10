import streamlit as st
from streamlit_autorefresh import st_autorefresh
import os
import glob
from datetime import datetime
from PIL import Image

# ── 1. CORE SYSTEM CONFIG ──────────────────────────────────────────────────
st.set_page_config(page_title="Utah Land & Property", layout="wide")

# Emergency Secrets Check - If this fails, it won't be a white screen anymore
if "access_keys" not in st.secrets:
    st.error("🚨 CONFIGURATION ERROR: 'access_keys' not found in Secrets.")
    st.info("Please ensure your secrets.toml or Cloud Secrets contain the [access_keys] section.")
    st.stop()

# Auto-refresh every 10 mins
st_autorefresh(interval=600000, key="ulp_refresh")

# Build Vault Folders
for folder in ["vault/general", "vault/buyer_docs", "vault/property_images"]:
    os.makedirs(folder, exist_ok=True)

# Session State Init
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_role" not in st.session_state:
    st.session_state.user_role = None

# ── 2. THE LOGIN GATE (NUCLEAR STABILITY VERSION) ──────────────────────────
if not st.session_state.authenticated:
    # Minimal CSS to avoid rendering crashes
    st.markdown("""
        <style>
        .main { background-color: #f8f9fa; }
        .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #1a3c6d; color: white; }
        header, footer {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

    # Vertical Spacing to "center" without breaking the browser
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)
    
    # Hero Section using standard Streamlit Markdown (Safest Method)
    _, center_col, _ = st.columns([1, 2, 1])
    
    with center_col:
        st.markdown(f"<h1 style='text-align: center; color: #1a3c6d; font-family: sans-serif; font-size: 3rem;'>Utah Land & Property</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; letter-spacing: 3px; color: #6b7280;'>STRATEGIC ASSET PROTECTION FRAMEWORK</p>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("<p style='text-align: center;'><strong>Privacy Creation Preservation • Creative Land & Real Estate Deal Structure</strong></p>", unsafe_allow_html=True)
        
        # Combined line - No dash
        st.markdown("<p style='text-align: center; color: #10b981; font-weight: bold;'>🟢 SECURE CLIENT PORTAL ENCRYPTED ACCESS ONLY</p>", unsafe_allow_html=True)
        
        # Login Logic
        pwd = st.text_input("Access Key", type="password", placeholder="Enter Private Key", label_visibility="collapsed")
        if st.button("Authorize Access"):
            access_map = st.secrets["access_keys"]
            if pwd in access_map:
                st.session_state.authenticated = True
                st.session_state.user_role = access_map[pwd]
                st.rerun()
            else:
                st.error("Invalid Security Key")

# ── 3. THE DASHBOARD (PROTECTED) ───────────────────────────────────────────
else:
    role = st.session_state.user_role
    
    # Dashboard Header
    col_a, col_b = st.columns([0.8, 0.2])
    col_a.title(f"{role} Portal")
    if col_b.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()

    st.markdown("---")

    # --- 3a. RECENT ACTIVITY (NEWEST ON TOP) ---
    st.subheader("Latest System Activity")
    files_found = []
    for root, _, files in os.walk("vault"):
        for f in files:
            if not f.startswith('.'):
                fp = os.path.join(root, f)
                files_found.append((f, os.path.getmtime(fp), root.split(os.sep)[-1]))
    
    files_found.sort(key=lambda x: x[1], reverse=True)
    
    if files_found:
        act_cols = st.columns(3)
        for i, (name, _, cat) in enumerate(files_found[:3]):
            act_cols[i].success(f"**{name}**\n\nCategory: {cat.replace('_',' ').title()}")
    else:
        st.info("The vault is currently empty.")

    # --- 3b. PROPERTY VISUALS (CRASH-PROOF) ---
    st.markdown("---")
    st.subheader("Property Visuals")
    
    img_paths = glob.glob("vault/property_images/*")
    if img_paths:
        # Use columns for mobile-friendly stacking
        img_cols = st.columns(4)
        col_idx = 0
        for p in img_paths:
            try:
                # We open with PIL to VALIDATE it's an image. 
                # If it's a PDF/Text file, this will trigger the 'except' block.
                valid_img = Image.open(p)
                img_cols[col_idx % 4].image(valid_img, use_container_width=True)
                col_idx += 1
            except:
                # Silently ignore files that aren't valid images
                continue
    else:
        st.info("No images currently in vault.")

    # --- 3c. ROLE-BASED ACTIONS ---
    st.markdown("---")
    if role == "Buyer":
        st.subheader("Your Documents for Signature")
        docs = [f for f in os.listdir("vault/buyer_docs") if not f.startswith('.')]
        if docs:
            for d in docs:
                with open(f"vault/buyer_docs/{d}", "rb") as f_obj:
                    st.download_button(f"📄 Download & Sign: {d}", f_obj, file_name=d)
        else:
            st.success("All clear. No pending signatures.")
    
    else:
        st.subheader("Upload & Management")
        c1, c2 = st.columns(2)
        dest = c1.radio("Target Folder", ["General Vault", "Buyer's Signature Folder"], horizontal=True)
        
        # Only certain roles can upload to Property Images
        if role in ["Admin", "Agent"]:
            kind = c2.radio("Asset Class", ["Document", "Property Image"], horizontal=True)
        else:
            kind = "Document"
            c2.write(f"Class: {kind} (Restricted)")

        up_files = st.file_uploader("Drop files here", accept_multiple_files=True)
        if up_files:
            for f in up_files:
                if kind == "Property Image":
                    folder = "vault/property_images"
                elif dest == "Buyer's Signature Folder":
                    folder = "vault/buyer_docs"
                else:
                    folder = "vault/general"
                
                with open(os.path.join(folder, f.name), "wb") as save_f:
                    save_f.write(f.getbuffer())
            st.success("Uploaded.")
            st.rerun()

    # Admin Audit
    if role == "Admin":
        with st.expander("Master Vault Audit"):
            st.write(glob.glob("vault/**/*", recursive=True))
