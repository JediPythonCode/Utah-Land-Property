import streamlit as st
from streamlit_autorefresh import st_autorefresh
import os
import glob
from datetime import datetime
from PIL import Image

# ── 1. CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Utah Land & Property", layout="wide", initial_sidebar_state="collapsed")
st_autorefresh(interval=600000, key="ulp_refresh")

# Ensure vault directories exist
for folder in ["vault/general", "vault/buyer_docs", "vault/property_images"]:
    os.makedirs(folder, exist_ok=True)

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_role" not in st.session_state:
    st.session_state.user_role = None

# ── 2. AUTHENTICATION GATE (CENTERED & STYLIZED) ───────────────────────────
if not st.session_state.authenticated:
    if "access_keys" not in st.secrets:
        st.error("🚨 Configuration Missing: Please add [access_keys] to Streamlit Secrets.")
        st.stop()

    # Re-introducing the Custom Typography and Centering
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&family=Oswald:wght@500;700&display=swap');
        
        .stApp { background-color: #ffffff !important; }
        header, footer, [data-testid="stHeader"] { visibility: hidden !important; }
        
        /* The container that handles vertical centering */
        .main-hero {
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            min-height: 70vh; text-align: center; width: 100%; padding: 20px;
        }

        .brand-title { font-family: 'Inter', sans-serif !important; font-size: clamp(38px, 8vw, 78px) !important; font-weight: 900 !important; color: #1a3c6d !important; letter-spacing: -1.5px !important; margin-bottom: 0px !important; line-height: 1.0 !important; }
        .brand-subtitle { font-family: 'Oswald', sans-serif !important; font-size: clamp(1rem, 3vw, 1.35rem) !important; color: #6b7280 !important; letter-spacing: 3px !important; font-weight: 500 !important; margin-top: 10px !important; margin-bottom: 1.5rem !important; }
        .framework-text { color: #4b5563 !important; font-size: 1.1rem !important; max-width: 850px !important; margin: 0 auto 2rem !important; line-height: 1.7 !important; font-family: 'Inter', sans-serif !important; }
        .pulse-lock { height: 12px; width: 12px; background: #10b981; border-radius: 50%; display: inline-block; margin-right: 12px; box-shadow: 0 0 12px rgba(16,185,129,0.5); animation: pulse 2s infinite; vertical-align: middle; }
        @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(16,185,129,0.7); } 70% { box-shadow: 0 0 0 12px rgba(16,185,129,0); } 100% { box-shadow: 0 0 0 0 rgba(16,185,129,0); } }
        .access-text { font-family: 'Oswald', sans-serif !important; font-size: 0.95rem !important; color: #1a3c6d !important; font-weight: 700 !important; letter-spacing: 2px !important; vertical-align: middle; }
        
        /* Input tightening */
        .stTextInput > div > div > input { text-align: center; }
    </style>
    """, unsafe_allow_html=True)

    # Hero Construction
    st.write('<div class="main-hero">', unsafe_allow_html=True)
    st.markdown('<div class="brand-title">Utah Land & Property</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-subtitle">Strategic Asset Protection Framework</div>', unsafe_allow_html=True)
    st.markdown('<div class="framework-text"><strong>Privacy Creation Preservation • Creative Land & Real Estate Deal Structure</strong></div>', unsafe_allow_html=True)
    st.markdown('<div style="margin-bottom: 2.5rem;"><span class="pulse-lock"></span><span class="access-text">SECURE CLIENT PORTAL ENCRYPTED ACCESS ONLY</span></div>', unsafe_allow_html=True)

    _, col_mid, _ = st.columns([1, 1.4, 1])
    with col_mid:
        pwd = st.text_input("Key", type="password", placeholder="Enter Access Key", label_visibility="collapsed")
        if st.button("Authorize Portal Access", use_container_width=True, type="primary"):
            access_map = st.secrets["access_keys"]
            if pwd in access_map:
                st.session_state.authenticated = True
                st.session_state.user_role = access_map[pwd]
                st.rerun()
            else:
                st.error("Invalid Security Key")
    st.write('</div>', unsafe_allow_html=True)

# ── 3. PROTECTED CONTENT ──────────────────────────────────────────────────
else:
    role = st.session_state.user_role
    
    # Dashboard Styles
    st.markdown("""
        <style>
            .block-container { text-align: center; padding-top: 2rem; background-color: #ffffff; }
            .stButton > button { display: block; margin: 0 auto; width: 220px; }
            [data-testid="stFileUploader"] { width: 100%; max-width: 500px; margin: 0 auto; }
            .activity-card { border: 1px solid #eee; padding: 15px; border-radius: 10px; background: #fafafa; }
        </style>
    """, unsafe_allow_html=True)

    st.title(f"{role} Management Dashboard")
    if st.button("Secure Logout", type="secondary"):
        st.session_state.authenticated = False
        st.rerun()

    st.markdown("---")

    # --- 3a. RECENT ACTIVITY (Top Feed for all) ---
    st.subheader("Latest System Activity")
    activity = []
    for root, _, files in os.walk("vault"):
        for f in files:
            if not f.startswith('.'):
                fp = os.path.join(root, f)
                activity.append((f, os.path.getmtime(fp), root.split(os.sep)[-1]))
    
    activity.sort(key=lambda x: x[1], reverse=True)
    if activity:
        act_cols = st.columns(3)
        for i, (name, _, cat) in enumerate(activity[:3]):
            act_cols[i].markdown(f"""
            <div class="activity-card">
                <strong>{name}</strong><br>
                <span style="color:#666; font-size:0.8rem;">{cat.replace('_',' ').title()}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No files in vault.")

    # --- 3b. PROPERTY VISUALS (Crash-Proof) ---
    st.markdown("---")
    st.subheader("Property Visuals")
    raw_images = glob.glob("vault/property_images/*")
    
    if raw_images:
        img_cols = st.columns(4)
        count = 0
        for p in raw_images:
            try:
                # Validate the image file actually works before trying to show it
                with Image.open(p) as validated:
                    img_cols[count % 4].image(validated, use_container_width=True)
                    count += 1
            except:
                continue
    else:
        st.info("Waiting for property assets to be uploaded.")

    # --- 3c. ROLE ACTIONS ---
    st.markdown("---")
    if role == "Buyer":
        st.subheader("Signature Documents")
        docs = [f for f in os.listdir("vault/buyer_docs") if not f.startswith('.')]
        if docs:
            for d in docs:
                with open(f"vault/buyer_docs/{d}", "rb") as fobj:
                    st.download_button(f"📄 Download: {d}", fobj, file_name=d)
        else:
            st.success("No pending documents for signature.")
    else:
        st.subheader("Vault Management")
        c1, c2 = st.columns(2)
        target = c1.radio("Destination", ["General Vault", "Buyer's Signature Folder"], horizontal=True)
        if role in ["Admin", "Agent"]:
            kind = c2.radio("Asset Class", ["Document", "Property Image"], horizontal=True)
        else:
            kind = "Document"

        up = st.file_uploader("Select Files", accept_multiple_files=True)
        if up:
            for f in up:
                folder = "vault/property_images" if kind == "Property Image" else ("vault/buyer_docs" if target == "Buyer's Signature Folder" else "vault/general")
                with open(os.path.join(folder, f.name), "wb") as save_f:
                    save_f.write(f.getbuffer())
            st.success("Assets Saved.")
            st.rerun()

    if role == "Admin":
        with st.expander("System File Audit"):
            st.json(glob.glob("vault/**/*", recursive=True))

    st.markdown(f"<p style='color:#ccc; font-size:0.7rem; margin-top:50px;'>SESSION: {role.upper()} AUTHENTICATED</p>", unsafe_allow_html=True)
