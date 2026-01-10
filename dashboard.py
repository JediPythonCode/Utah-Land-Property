import streamlit as st
from streamlit_autorefresh import st_autorefresh
import os
import glob
from datetime import datetime

# ── 1. CONFIG & REFRESH ────────────────────────────────────────────────────
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
    # Combined CSS and HTML in one block to prevent code leakage
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&family=Oswald:wght@500;700&display=swap');
        
        .stApp { background-color: #f8f9fa !important; }
        header, footer, [data-testid="stHeader"] { display: none !important; }
        
        .main-login-container {
            margin-top: -12vh; /* Shifts content up significantly */
            text-align: center;
            width: 100%;
        }

        .brand-title {
            font-family: 'Inter', sans-serif;
            font-size: clamp(42px, 10vw, 78px);
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
            margin-bottom: 2.5rem;
        }
        
        .access-text {
            font-family: 'Oswald', sans-serif;
            font-size: 2.2rem; 
            color: #1a3c6d;
            font-weight: 700;
            letter-spacing: 2px;
            margin-bottom: 1.5rem;
            display: block;
        }
    </style>
    
    <div class="main-login-container">
        <div class="brand-title">Utah Land & Property</div>
        <div class="brand-subtitle">Strategic Asset Framework</div>
        <span class="access-text">CLIENT SECURE ACCESS</span>
    </div>
    """, unsafe_allow_html=True)

    # Centering the input field using Streamlit columns
    _, col2, _ = st.columns([1, 1, 1])
    with col2:
        pwd = st.text_input("Access Key", type="password", placeholder="Enter private key", label_visibility="collapsed")
        if st.button("Access Secure Area", use_container_width=True, type="primary"):
            # Fetching from st.secrets only
            try:
                allowed_passwords = [
                    st.secrets["PASSWORDS"]["CLIENT"],
                    st.secrets["PASSWORDS"]["ADMIN"]
                ]
                if pwd in allowed_passwords:
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Invalid key — access denied.")
            except KeyError:
                st.error("System Error: Passwords not configured in Secrets.")
    st.stop()

# ── 3. MAIN APP (AUTHENTICATED) ─────────────────────────────────────────────
with st.sidebar:
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()

# Dashboard Header
st.markdown("""
<div style="margin-top: -90px; text-align:center;">
    <h1 style="font-family:'Inter'; font-weight:900; color:#1a3c6d; font-size:3.5rem; margin-bottom:0;">Utah Land & Property</h1>
    <p style="font-family:'Oswald'; color:#d97706; letter-spacing:4px; font-weight:700;">ASSET PROTECTION • PRIVACY • CREATIVE FINANCING</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ── 4. SECURE VAULT & FILE MANAGEMENT ───────────────────────────────────────
st.subheader("📁 Secure Vault Management")
uploaded_file = st.file_uploader("Upload new documents", type=['pdf', 'docx', 'xlsx', 'png', 'jpg'])

if uploaded_file is not None:
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"File '{uploaded_file.name}' vaulted.")
    st.rerun()

st.markdown("### 📄 Available Resources")
doc_files = glob.glob("*.pdf") + glob.glob("*.docx") + glob.glob("*.xlsx")

if doc_files:
    for file_path in sorted(doc_files, key=os.path.getctime, reverse=True):
        with st.container(border=True):
            c1, c2 = st.columns([4, 1])
            with c1:
                st.markdown(f"**{file_path}**")
                st.caption(f"Sync Date: {datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d')}")
            with c2:
                with open(file_path, "rb") as f:
                    st.download_button("Download", f, file_name=file_path, key=f"dl_{file_path}")
else:
    st.info("Vault is currently empty.")
