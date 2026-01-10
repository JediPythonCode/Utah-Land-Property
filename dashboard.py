import streamlit as st
from streamlit_autorefresh import st_autorefresh
import os
import glob
from datetime import datetime

# ── 1. CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Utah Land & Property", layout="wide", initial_sidebar_state="collapsed")
st_autorefresh(interval=600000, key="ulp_refresh")

# Folder Persistence
for folder in ["vault/general", "vault/buyer_docs", "vault/property_images"]:
    os.makedirs(folder, exist_ok=True)

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_role" not in st.session_state:
    st.session_state.user_role = None

# ── 2. AUTHENTICATION GATE (RECENTERED & TIGHTENED) ────────────────────────
if not st.session_state.authenticated:
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&family=Oswald:wght@500;700&display=swap');
        .stApp { background-color: #f8f9fa !important; }
        header, footer, [data-testid="stHeader"] { display: none !important; }
        .login-container {
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            height: 90vh; text-align: center; width: 100%; padding: 10px;
        }
        .brand-title { font-family: 'Inter', sans-serif !important; font-size: clamp(34px, 7vw, 72px) !important; font-weight: 900 !important; color: #1a3c6d; letter-spacing: -1.5px; line-height: 1; margin: 0; }
        .brand-subtitle { font-family: 'Oswald', sans-serif !important; font-size: clamp(0.9rem, 2.5vw, 1.2rem) !important; color: #6b7280; letter-spacing: 3px; font-weight: 500; margin: 10px 0 20px 0; }
        .framework-text { color: #4b5563; font-size: 1rem; max-width: 750px; margin: 0 auto 30px auto; line-height: 1.6; font-family: 'Inter', sans-serif; }
        .pulse-lock { height: 10px; width: 10px; background: #10b981; border-radius: 50%; display: inline-block; margin-right: 10px; box-shadow: 0 0 10px rgba(16,185,129,0.5); animation: pulse 2s infinite; vertical-align: middle; }
        @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(16,185,129,0.7); } 70% { box-shadow: 0 0 0 10px rgba(16,185,129,0); } 100% { box-shadow: 0 0 0 0 rgba(16,185,129,0); } }
        .access-text { font-family: 'Oswald', sans-serif !important; font-size: 0.85rem; color: #1a3c6d; font-weight: 700; letter-spacing: 2px; vertical-align: middle; }
    </style>
    """, unsafe_allow_html=True)

    # Wrap the entire login UI in a centered div
    st.write('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<div class="brand-title">Utah Land & Property</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-subtitle">Strategic Asset Protection Framework</div>', unsafe_allow_html=True)
    st.markdown('<div class="framework-text"><strong>Privacy Creation Preservation • Creative Land & Real Estate Deal Structure</strong></div>', unsafe_allow_html=True)
    st.markdown('<div style="margin-bottom: 25px;"><span class="pulse-lock"></span><span class="access-text">SECURE CLIENT PORTAL ENCRYPTED ACCESS ONLY</span></div>', unsafe_allow_html=True)

    _, col_mid, _ = st.columns([1, 1.4, 1])
    with col_mid:
        pwd = st.text_input("Key", type="password", placeholder="Enter Access Key", label_visibility="collapsed")
        if st.button("Access Portal", use_container_width=True, type="primary"):
            access_map = st.secrets.get("access_keys", {})
            if pwd in access_map:
                st.session_state.authenticated = True
                st.session_state.user_role = access_map[pwd]
                st.rerun()
            else:
                st.error("Access Denied")
    st.write('</div>', unsafe_allow_html=True)

# ── 3. PROTECTED CONTENT ──────────────────────────────────────────────────
else:
    role = st.session_state.user_role
    st.markdown("<style>.block-container { text-align: center; padding-top: 1rem; } .stButton>button {margin: 0 auto; width: 180px;} [data-testid='stFileUploader'] {max-width: 450px; margin: 0 auto;}</style>", unsafe_allow_html=True)

    st.title(f"{role} Portal")
    if st.button("Logout", type="secondary"):
        st.session_state.authenticated = False
        st.rerun()

    st.markdown("---")

    # --- 3a. LIVE ACTIVITY FEED (VISIBLE TO ALL) ---
    st.subheader("Global Activity Feed")
    all_files = []
    for root, _, files in os.walk("vault"):
        for f in files:
            if not f.startswith('.'):
                path = os.path.join(root, f)
                all_files.append((f, os.path.getmtime(path), root.split(os.sep)[-1]))
    
    all_files.sort(key=lambda x: x[1], reverse=True)
    if all_files:
        fcols = st.columns(3)
        for i, (name, _, cat) in enumerate(all_files[:3]):
            fcols[i].info(f"🆕 **{name}**\n\n*{cat.replace('_',' ').title()}*")
    else:
        st.info("No activity recorded yet.")

    # --- 3b. PROPERTY VISUALS ---
    st.markdown("---")
    st.subheader("Property Images")
    imgs = [f for f in glob.glob("vault/property_images/*") if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
    if imgs:
        icols = st.columns(min(len(imgs), 4))
        for idx, p in enumerate(imgs):
            icols[idx % 4].image(p, use_container_width=True)
    else:
        st.info("No images uploaded.")

    # --- 3c. ROLE ACTIONS ---
    st.markdown("---")
    if role == "Buyer":
        st.subheader("Action Required: Your Documents")
        bdocs = os.listdir("vault/buyer_docs")
        if bdocs:
            for d in bdocs:
                with open(f"vault/buyer_docs/{d}", "rb") as fobj:
                    st.download_button(f"📄 Download: {d}", fobj, file_name=d)
        else:
            st.success("No pending documents.")
    else:
        st.subheader("Archival Management")
        c1, c2 = st.columns(2)
        with c1:
            dest = st.radio("Destination", ["General Vault", "Buyer's Signature Folder"], horizontal=True)
        with c2:
            kind = st.radio("Type", ["Document", "Property Image"], horizontal=True) if role in ["Admin", "Agent"] else "Document"
        
        up = st.file_uploader("Upload Assets", accept_multiple_files=True)
        if up:
            for f in up:
                folder = "vault/property_images" if kind == "Property Image" else ("vault/buyer_docs" if dest == "Buyer's Signature Folder" else "vault/general")
                with open(os.path.join(folder, f.name), "wb") as fsave:
                    fsave.write(f.getbuffer())
            st.success("Archived.")
            st.rerun()

    if role == "Admin":
        with st.expander("System Audit"):
            st.write(glob.glob("vault/**/*", recursive=True))
