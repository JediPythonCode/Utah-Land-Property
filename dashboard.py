import streamlit as st
from streamlit_autorefresh import st_autorefresh
import os
import glob
from datetime import datetime

# ── 1. CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Utah Land & Property",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st_autorefresh(interval=600000, key="ulp_refresh")

# ── 2. AUTHENTICATION GATE ──────────────────────────────────────────────────
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&family=Oswald:wght@500;700&display=swap');
        
        .stApp { background-color: #f8f9fa !important; }
        header, footer, [data-testid="stHeader"] { display: none !important; }
        
        /* CENTERED MOBILE-FRIENDLY CONTAINER */
        .main-login-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 15vh 5% 0; /* Shifts everything to center-top */
            width: 100%;
        }

        .brand-title {
            font-family: 'Inter', sans-serif;
            font-size: clamp(32px, 8vw, 60px);
            font-weight: 900;
            color: #1a3c6d;
            letter-spacing: -1.5px;
            margin-bottom: 5px;
        }
        .brand-subtitle {
            font-family: 'Oswald', sans-serif;
            font-size: clamp(0.9rem, 2.5vw, 1.1rem);
            color: #6b7280;
            letter-spacing: 2px;
            font-weight: 500;
            margin-bottom: 3rem;
        }
        
        /* GREEN STROBE INDICATOR */
        .pulse-lock {
            height: 10px;
            width: 10px;
            background: #10b981;
            border-radius: 50%;
            display: inline-block;
            margin-right: 12px;
            vertical-align: middle;
            box-shadow: 0 0 12px rgba(16,185,129,0.5);
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%   { box-shadow: 0 0 0 0 rgba(16,185,129,0.7); }
            70%  { box-shadow: 0 0 0 10px rgba(16,185,129,0); }
            100% { box-shadow: 0 0 0 0 rgba(16,185,129,0); }
        }

        .access-text {
            font-family: 'Oswald', sans-serif;
            font-size: 1.2rem; /* Decreased font size */
            color: #1a3c6d;
            font-weight: 700;
            letter-spacing: 1.5px;
            display: inline-block;
            vertical-align: middle;
        }

        .status-wrapper {
            margin-bottom: 1.5rem;
        }
    </style>
    
    <div class="main-login-container">
        <div class="brand-title">Utah Land & Property</div>
        <div class="brand-subtitle">Strategic Asset Framework</div>
        
        <div class="status-wrapper">
            <span class="pulse-lock"></span>
            <span class="access-text">CLIENT SECURE ACCESS</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Centered Input Box
    _, col_mid, _ = st.columns([1, 2, 1])
    with col_mid:
        pwd = st.text_input("Key", type="password", placeholder="Access Key", label_visibility="collapsed")
        if st.button("Access Portal", use_container_width=True, type="primary"):
            try:
                # Direct check from secrets
                if pwd in [st.secrets["PASSWORDS"]["CLIENT"], st.secrets["PASSWORDS"]["ADMIN"]]:
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Invalid Access Key")
            except:
                st.error("Configuration Error: Secrets not found.")
    st.stop()

# ── 3. MAIN DASHBOARD (AUTHENTICATED) ───────────────────────────────────────
with st.sidebar:
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()

st.markdown("""
<div style="margin-top: -80px; text-align:center; padding: 0 10px;">
    <h2 style="font-family:'Inter'; font-weight:900; color:#1a3c6d; font-size:clamp(28px, 6vw, 42px); margin-bottom:0;">Utah Land & Property</h2>
    <p style="font-family:'Oswald'; color:#d97706; letter-spacing:2px; font-weight:700; font-size:0.85rem;">ASSET PROTECTION • PRIVACY • FINANCING</p>
</div>
""", unsafe_allow_html=True)

# ── 4. MOBILE-FRIENDLY UPLOAD ──────────────────────────────────────────────
with st.expander("📤 Upload New Document", expanded=False):
    st.info("Supported: PDF, Images, Excel, Word")
    uploaded_file = st.file_uploader(
        "Secure Upload", 
        type=['pdf', 'docx', 'xlsx', 'jpg', 'png'],
        label_visibility="collapsed"
    )
    if uploaded_file:
        # Saving file locally in the vault
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("File added to vault.")
        st.rerun()

st.divider()

# ── 5. FILE LISTING ────────────────────────────────────────────────────────
st.markdown("### 📄 Secure Vault")
doc_types = ["*.pdf", "*.docx", "*.xlsx", "*.jpg", "*.png", "*.jpeg"]
doc_files = []
for t in doc_types:
    doc_files.extend(glob.glob(t))

if doc_files:
    # Sort by newest first
    for file_path in sorted(doc_files, key=os.path.getctime, reverse=True):
        with st.container(border=True):
            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown(f"**{file_path}**")
                st.caption(f"Sync: {datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d %H:%M')}")
            with c2:
                with open(file_path, "rb") as f:
                    st.download_button("Get", f, file_name=file_path, key=f"dl_{file_path}", use_container_width=True)
else:
    st.info("No documents found in vault.")
