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

# Ensure vault directories exist
for folder in ["vault/general", "vault/buyer_docs", "vault/property_images"]:
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

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
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            min-height: 70vh; 
            text-align: center; 
            width: 100%; 
            padding: 20px;
        }

        .brand-title { font-family: 'Inter', sans-serif !important; font-size: clamp(38px, 8vw, 78px) !important; font-weight: 900 !important; color: #1a3c6d !important; letter-spacing: -1.5px !important; margin-bottom: 0px !important; line-height: 1.0 !important; }
        .brand-subtitle { font-family: 'Oswald', sans-serif !important; font-size: clamp(1rem, 3vw, 1.35rem) !important; color: #6b7280 !important; letter-spacing: 3px !important; font-weight: 500 !important; margin-top: 10px !important; margin-bottom: 2rem !important; }
        .framework-text { color: #4b5563 !important; font-size: 1.05rem !important; max-width: 800px !important; margin: 0 auto 2.5rem !important; line-height: 1.7 !important; font-family: 'Inter', sans-serif !important; }
        .pulse-lock { height: 12px; width: 12px; background: #10b981; border-radius: 50%; display: inline-block; margin-right: 12px; box-shadow: 0 0 12px rgba(16,185,129,0.5); animation: pulse 2s infinite; vertical-align: middle; }
        @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(16,185,129,0.7); } 70% { box-shadow: 0 0 0 12px rgba(16,185,129,0); } 100% { box-shadow: 0 0 0 0 rgba(16,185,129,0); } }
        .access-text { font-family: 'Oswald', sans-serif !important; font-size: 0.9rem !important; color: #1a3c6d !important; font-weight: 700 !important; letter-spacing: 2px !important; vertical-align: middle; }
        
        [data-testid="stVerticalBlock"] { align-items: center !important; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="viewport-top-container">', unsafe_allow_html=True)
    st.markdown('<div class="brand-title">Utah Land & Property</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-subtitle">Strategic Asset Protection Framework</div>', unsafe_allow_html=True)
    st.markdown('<div class="framework-text"><strong>Privacy Creation Preservation • Creative Land & Real Estate Deal Structure</strong></div>', unsafe_allow_html=True)
    st.markdown('<div style="margin-bottom: 2rem;"><span class="pulse-lock"></span><span class="access-text">SECURE CLIENT PORTAL ENCRYPTED ACCESS ONLY</span></div>', unsafe_allow_html=True)

    _, col_mid, _ = st.columns([1.2, 1, 1.2])
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
    st.markdown("</div>", unsafe_allow_html=True)

# ── 3. PROTECTED CONTENT ──────────────────────────────────────────────────
else:
    role = st.session_state.user_role
    st.markdown("""
        <style>
            .main .block-container { max-width: 900px; margin: 0 auto; text-align: center; padding-top: 3rem; }
            .stButton > button { margin: 0 auto !important; display: block; }
            [data-testid="stFileUploader"] { margin: 0 auto; }
            [data-testid="stHorizontalBlock"] { justify-content: center; }
            .recent-file-card { background: white; padding: 15px; border-radius: 8px; border: 1px solid #ddd; margin-bottom: 10px; font-family: 'Inter'; font-size: 0.9rem; text-align: left; }
        </style>
    """, unsafe_allow_html=True)

    st.title(f"{role} Dashboard")
    if st.button("Secure Logout"):
        st.session_state.authenticated = False
        st.rerun()

    st.markdown("---")
    st.subheader("Latest Property Activity")
    
    # Activity Feed Logic
    all_files = []
    for root, dirs, files in os.walk("vault"):
        for f in files:
            if not f.startswith('.'):
                path = os.path.join(root, f)
                all_files.append((f, os.path.getmtime(path), root.split('/')[-1]))
    all_files.sort(key=lambda x: x[1], reverse=True)

    if all_files:
        feed_cols = st.columns(3)
        for i, (fname, ftime, ftype) in enumerate(all_files[:3]):
            dt = datetime.fromtimestamp(ftime).strftime('%Y-%m-%d %H:%M')
            with feed_cols[i]:
                st.markdown(f"""<div class="recent-file-card"><strong>{fname}</strong><br><span style="color:#666; font-size:0.8rem;">Category: {ftype.title()}</span><br><span style="color:#999; font-size:0.7rem;">{dt}</span></div>""", unsafe_allow_html=True)
    else:
        st.info("No recent activity.")

    st.markdown("---")
    # Remaining dashboard logic continues here...
    st.markdown(f"<small>Authenticated as {role}</small>", unsafe_allow_html=True)
