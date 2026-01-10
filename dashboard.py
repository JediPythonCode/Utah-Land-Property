import streamlit as st
import st_autorefresh
import json
import os
import glob
import textwrap
from datetime import datetime
from streamlit_autorefresh

# ── 1. CONFIG & AUTO-REFRESH ───────────────────────────────────────────────
st.set_page_config(
    page_title="Utah Land & Property",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Gentle refresh (every 10 min) — useful if showing dynamic file list
st_autorefresh(interval=600000, key="ulp_refresh")

# ── 2. AUTHENTICATION GATE ──────────────────────────────────────────────────
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    # Minimal, elegant lock screen with privacy focus
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&family=Oswald:wght@500;700&display=swap');

        .stApp { background-color: #f8f9fa !important; }
        header, footer, [data-testid="stHeader"] { display: none !important; }

        .brand-title {
            font-family: 'Inter', sans-serif;
            font-size: clamp(42px, 10vw, 78px);
            font-weight: 900;
            color: #1a3c6d;
            letter-spacing: -1.5px;
            text-align: center;
            margin: 0.4em 0 0.1em;
        }
        .brand-subtitle {
            font-family: 'Oswald', sans-serif;
            font-size: 1.35rem;
            color: #6b7280;
            text-align: center;
            letter-spacing: 3px;
            font-weight: 500;
            margin-bottom: 2.5rem;
        }
        .privacy-notice {
            text-align: center;
            color: #4b5563;
            font-size: 0.95rem;
            max-width: 640px;
            margin: 0 auto 2.5rem;
            line-height: 1.6;
        }
        .lock-container {
            max-width: 480px;
            margin: 0 auto;
            padding: 2.5rem 1.5rem;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 35px rgba(0,0,0,0.08);
            border: 1px solid #e5e7eb;
        }
        .pulse-lock {
            height: 12px;
            width: 12px;
            background: #10b981;
            border-radius: 50%;
            display: inline-block;
            margin-right: 10px;
            box-shadow: 0 0 12px rgba(16,185,129,0.5);
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%   { box-shadow: 0 0 0 0 rgba(16,185,129,0.7); }
            70%  { box-shadow: 0 0 0 12px rgba(16,185,129,0); }
            100% { box-shadow: 0 0 0 0 rgba(16,185,129,0); }
        }
    </style>

    <div style="padding: 12vh 5% 4vh;">
        <div class="brand-title">Utah Land & Property</div>
        <div class="brand-subtitle">Strategic Asset Framework</div>
        <div class="privacy-notice">
            Asset Protection • Privacy Preservation • Creative Land Financing Solutions
            <br><br>
            <strong>Secure Client Portal</strong> — Encrypted access only.
        </div>

        <div class="lock-container">
            <div style="text-align:center; margin-bottom:1.8rem;">
                <span class="pulse-lock"></span>
                <span style="font-family:Oswald; color:#1a3c6d; font-weight:700; letter-spacing:1.5px;">
                    CLIENT SECURE ACCESS
                </span>
            </div>
    """, unsafe_allow_html=True)

    pwd = st.text_input("Access Key", type="password", placeholder="Enter your private key", label_visibility="collapsed")

    if st.button("Access Secure Area", use_container_width=True, type="primary"):
        # You can extend this with user roles later (admin / client / partner)
        if pwd in [st.secrets.get("PASSWORDS", {}).get("CLIENT", "default123"),
                   st.secrets.get("PASSWORDS", {}).get("ADMIN", "admin999")]:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Invalid key — access denied.")

    st.markdown("</div></div>", unsafe_allow_html=True)
    st.stop()

# ── 3. MAIN APP — AUTHENTICATED ─────────────────────────────────────────────
# Modern professional theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&family=Oswald:wght@500;700&display=swap');

    .stApp { background-color: #f8f9fa !important; }
    .main-title {
        font-family: 'Inter', sans-serif;
        font-size: clamp(38px, 8vw, 68px);
        font-weight: 900;
        color: #1a3c6d;
        letter-spacing: -1.8px;
        text-align: center;
        line-height: 0.92;
        margin: 0.4em 0 0.1em;
    }
    .framework-tag {
        font-family: 'Oswald', sans-serif;
        color: #d97706;
        font-size: 1.4rem;
        letter-spacing: 4px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-family: 'Inter', sans-serif;
        color: #1e293b;
        font-weight: 800;
        font-size: 2.1rem;
        margin: 2.5rem 0 1rem;
        border-left: 5px solid #d97706;
        padding-left: 1rem;
    }
    .card {
        background: white;
        border-radius: 12px;
        padding: 1.8rem;
        box-shadow: 0 6px 20px rgba(0,0,0,0.07);
        border: 1px solid #e5e7eb;
        margin-bottom: 1.6rem;
    }
    .status-dot {
        height: 10px; width: 10px; background: #10b981; border-radius: 50%;
        display: inline-block; margin-right: 8px;
        box-shadow: 0 0 10px rgba(16,185,129,0.4);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown(f"""
<div style="text-align:center; padding: 1.5rem 0 2.5rem;">
    <div class="main-title">Utah Land & Property</div>
    <div class="framework-tag">ASSET PROTECTION • PRIVACY • CREATIVE FINANCING</div>
    <div style="color:#64748b; font-size:0.95rem;">
        <span class="status-dot"></span>SECURE CLIENT AREA • LAST SYNC: {datetime.now().strftime('%Y-%m-%d %H:%M')}
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ── WELCOME / OVERVIEW ──────────────────────────────────────────────────────
st.markdown('<div class="section-header">Welcome to Your Secure Portal</div>', unsafe_allow_html=True)

with st.container():
    st.info("""
    Utah Land & Property serves as a **strategic framework** — not merely a conventional company.

    We specialize in the sophisticated intersection of:
    • **Asset Protection** through carefully structured land holding vehicles
    • **Privacy** maximization using Utah-friendly legal structures
    • **Creative Financing** techniques tailored to real estate & land investments

    All documents & communications within this portal are encrypted and intended for authorized clients only.
    """)

# ── DOCUMENT / FILE HOSTING AREA ────────────────────────────────────────────
st.markdown('<div class="section-header">Available Documents & Resources</div>', unsafe_allow_html=True)

doc_files = glob.glob("*.pdf") + glob.glob("*.docx") + glob.glob("*.xlsx")

if doc_files:
    st.markdown(f"**{len(doc_files)} secure file(s) available**")

    for file_path in sorted(doc_files, key=os.path.getctime, reverse=True):
        file_name = os.path.basename(file_path)

        col1, col2 = st.columns([5, 2])
        with col1:
            st.markdown(f"**{file_name}**  •  Updated {datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%b %d, %Y')}")
        with col2:
            with open(file_path, "rb") as f:
                st.download_button(
                    label="Download",
                    data=f,
                    file_name=file_name,
                    mime="application/octet-stream",
                    use_container_width=True,
                    key=f"dl_{file_name}"
                )
else:
    st.warning("No documents currently available in the secure folder.")

# ── QUICK LINKS / NEXT STEPS ────────────────────────────────────────────────
st.markdown('<div class="section-header">Next Steps & Support</div>', unsafe_allow_html=True)

cols = st.columns(3)

with cols[0]:
    with st.container(border=True):
        st.markdown("**Request New Structure**")
        st.caption("Land Trust • LLC Holding • DAPT integration")
        st.button("Submit Request", use_container_width=True, disabled=True)

with cols[1]:
    with st.container(border=True):
        st.markdown("**Schedule Strategy Review**")
        st.caption("Privacy & asset protection audit")
        st.button("Book Session", use_container_width=True, disabled=True)

with cols[2]:
    with st.container(border=True):
        st.markdown("**Upload Your Documents**")
        st.caption("Secure file drop for review")
        st.button("Upload", use_container_width=True, disabled=True)

st.markdown("---")

# Footer
st.markdown("""
<div style="text-align:center; color:#64748b; font-size:0.85rem; padding:3rem 0 1.5rem;">
    <strong>Utah Land & Property</strong>  |  Strategic Framework for Privacy & Protection  
    © 2026 • All communications encrypted • For authorized clients only
</div>
""", unsafe_allow_html=True)
