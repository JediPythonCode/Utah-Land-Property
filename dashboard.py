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
    # All HTML/CSS in one block to prevent code leakage
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&family=Oswald:wght@500;700&display=swap');
        
        .stApp { background-color: #f8f9fa !important; }
        header, footer, [data-testid="stHeader"] { display: none !important; }
        
        .main-login-container {
            text-align: center;
            padding: 8vh 5% 0; /* Positioned high on page */
            width: 100%;
        }

        .brand-title {
            font-family: 'Inter', sans-serif;
            font-size: clamp(42px, 10vw, 78px); /* Keep large */
            font-weight: 900;
            color: #1a3c6d;
            letter-spacing: -1.5px;
            margin-bottom: 0;
        }
        .brand-subtitle {
            font-family: 'Oswald', sans-serif;
            font-size: 1.35rem;
            color: #6b7280;
            letter-spacing: 3px;
            font-weight: 500;
            margin-bottom: 1.5rem;
        }
        .privacy-notice {
            text-align: center;
            color: #4b5563;
            font-size: 1rem;
            max-width: 640px;
            margin: 0 auto 2.5rem;
            line-height: 1.6;
            font-family: 'Inter', sans-serif;
        }
        
        /* GREEN STROBE INDICATOR */
        .pulse-lock {
            height: 10px;
            width: 10px;
            background: #10b981;
            border-radius: 50%;
            display: inline-block;
            margin-right: 10px;
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
            font-size: 1.1rem; /* Decreased font size */
            color: #1a3c6d;
            font-weight: 700;
            letter-spacing: 1.5px;
            display: inline-block;
            vertical-align: middle;
        }
    </style>
    
    <div class="main-login-container">
        <div class="brand-title">Utah Land & Property</div>
        <div class="brand-subtitle">Strategic Asset Framework</div>
        
        <div class="privacy-notice">
            Asset Protection • Privacy Preservation • Creative Land Financing Solutions
            <br><br>
            <strong>Secure Client Portal</strong> — Encrypted access only.
        </div>

        <div style="margin-bottom: 2rem;">
            <span class="pulse-lock"></span>
            <span class="access-text">CLIENT SECURE ACCESS</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Input columns (Pure Streamlit to avoid leakage)
    _, col_mid, _ = st.columns([1, 1.5, 1])
    with col_mid:
        pwd = st.text_input("Key", type="password", placeholder="Access Key", label_visibility="collapsed")
        if st.button("Access Portal", use_container_width=True, type="primary"):
            try:
                if pwd in [st.secrets["PASSWORDS"]["CLIENT"], st.secrets["PASSWORDS"]["ADMIN"]]:
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Invalid Key")
            except:
                st.error("System Error: Secrets not configured.")
    st.stop()

# ── 3. MAIN APP (AUTHENTICATED) ─────────────────────────────────────────────
with st.sidebar:
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()

# Dashboard Header (Shifted Up)
st.markdown("""
<div style="margin-top: -80px; text-align:center;">
    <h1 style="font-family:'Inter'; font-weight:900; color:#1a3c6d; font-size:clamp(32px, 7vw, 54px); margin-bottom:0;">Utah Land & Property</h1>
    <p style="font-family:'Oswald'; color:#d97706; letter-spacing:3px; font-weight:700;">ASSET PROTECTION • PRIVACY • FINANCING</p>
</div>
""", unsafe_allow_html=True)

# ── 4. MOBILE UPLOAD ───────────────────────────────────────────────────────
with st.expander("📤 Secure Document Upload", expanded=False):
    uploaded_file = st.file_uploader("Upload to Vault", type=['pdf', 'docx', 'xlsx', 'jpg', 'png', 'jpeg'])
    if uploaded_file:
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("Document Encrypted & Vaulted.")
        st.rerun()

st.divider()

# ── 5. FILE VAULT ──────────────────────────────────────────────────────────
st.markdown("### 📄 Available Resources")
doc_files = []
for ext in ["*.pdf", "*.docx", "*.xlsx", "*.jpg", "*.png", "*.jpeg"]:
    doc_files.extend(glob.glob(ext))

if doc_files:
    for file_path in sorted(doc_files, key=os.path.getctime, reverse=True):
        with st.container(border=True):
            c1, c2 = st.columns([4, 1.2])
            with c1:
                st.markdown(f"**{file_path}**")
                st.caption(f"Sync: {datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d %H:%M')}")
            with c2:
                with open(file_path, "rb") as f:
                    st.download_button("Download", f, file_name=file_path, key=f"dl_{file_path}", use_container_width=True)
else:
    st.info("Vault is currently empty.")
