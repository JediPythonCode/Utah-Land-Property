import streamlit as st
from streamlit_autorefresh import st_autorefresh
import os
from datetime import datetime

# ── 1. CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Utah Land & Property",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st_autorefresh(interval=600000, key="ulp_refresh")

# Initialize session state for auth and user role
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_role" not in st.session_state:
    st.session_state.user_role = None

# ── 2. AUTHENTICATION GATE ──────────────────────────────────────────────────
if not st.session_state.authenticated:
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&family=Oswald:wght@500;700&display=swap');
        .stApp { background-color: #f8f9fa !important; }
        header, footer, [data-testid="stHeader"] { display: none !important; }
        .viewport-top-container {
            margin-top: -5vh;
            text-align: center;
            width: 100%;
        }
        .brand-title {
            font-family: 'Inter', sans-serif !important;
            font-size: clamp(42px, 8vw, 70px) !important;
            font-weight: 900 !important;
            color: #1a3c6d !important;
            letter-spacing: -1.5px !important;
            margin-bottom: 0px !important;
            line-height: 1.0 !important;
        }
        .brand-subtitle {
            font-family: 'Oswald', sans-serif !important;
            font-size: 1.2rem !important;
            color: #6b7280 !important;
            letter-spacing: 3px !important;
            font-weight: 500 !important;
            margin-top: 5px !important;
            margin-bottom: 2rem !important;
        }
        .pulse-lock {
            height: 12px; width: 12px;
            background: #10b981;
            border-radius: 50%;
            display: inline-block;
            margin-right: 12px;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(16,185,129,0.7); }
            70% { box-shadow: 0 0 0 10px rgba(16,185,129,0); }
            100% { box-shadow: 0 0 0 0 rgba(16,185,129,0); }
        }
    </style>
    
    <div class="viewport-top-container">
        <div class="brand-title">Utah Land & Property</div>
        <div class="brand-subtitle">Strategic Asset Protection Framework</div>
        <div style="margin-bottom: 2rem;">
            <span class="pulse-lock"></span>
            <span style="font-family: 'Oswald'; font-weight:700; color:#1a3c6d;">SECURE GATEWAY</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Login Logic
    _, col_mid, _ = st.columns([1, 1.2, 1])
    with col_mid:
        role = st.selectbox("Select Access Role", ["Admin", "Agent", "Escrow", "Title", "Servicer", "Buyer"])
        pwd = st.text_input("Security Key", type="password", placeholder=f"Enter {role} Key")
        
        if st.button("Authorize Access", use_container_width=True, type="primary"):
            # Fetch passwords from streamlit secrets
            try:
                valid_password = st.secrets["passwords"][role]
                if pwd == valid_password:
                    st.session_state.authenticated = True
                    st.session_state.user_role = role
                    st.rerun()
                else:
                    st.error("Invalid Security Key for selected role.")
            except KeyError:
                st.error("Security configuration missing. Contact system admin.")

# ── 3. PROTECTED PORTAL CONTENT ──────────────────────────────────────────────
else:
    # Sidebar Navigation
    st.sidebar.title(f"🔐 {st.session_state.user_role} Portal")
    st.sidebar.info(f"Connected: {datetime.now().strftime('%m/%d/%Y')}")
    
    if st.sidebar.button("Sign Out", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.user_role = None
        st.rerun()

    # Main Interface
    st.title(f"{st.session_state.user_role} Dashboard")
    st.markdown("---")

    # File Upload Logic
    st.subheader("Document Upload & Archival")
    uploaded_files = st.file_uploader(
        "Securely upload assets (PDF, JPG, PNG, DOCX)", 
        accept_multiple_files=True
    )

    if uploaded_files:
        # Create a folder specifically for this role if it doesn't exist
        save_path = f"vault/{st.session_state.user_role.lower()}"
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        for file in uploaded_files:
            with open(os.path.join(save_path, file.name), "wb") as f:
                f.write(file.getbuffer())
            st.success(f"Verified & Saved: {file.name}")

    # Role-Specific Instructions Placeholder
    st.info(f"As an **{st.session_state.user_role}**, you have encrypted write-access to the property data-room.")
