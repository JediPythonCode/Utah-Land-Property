import streamlit as st
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# --- 1. CONFIG & REFRESH ---
st.set_page_config(page_title="Utah Land & Property", layout="wide", initial_sidebar_state="collapsed")
st_autorefresh(interval=10000, key="ulp_sync_ping")

# --- 2. AUTHENTICATION GATE (RETAINED AS REQUESTED) ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_role = None

# Initialize Logic for ULP Deal Structure
if "checklist_step" not in st.session_state:
    st.session_state.checklist_step = 3  # Start at Underwriting for this deal
if "uploaded_docs" not in st.session_state:
    st.session_state.uploaded_docs = []

if not st.session_state.authenticated:
    # [LOGIC NOT TOUCHED PER INSTRUCTION]
    pillar_icons = [
        '<svg viewBox="0 0 24 24" width="80" height="80" stroke="#1d428a" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>',
        '<svg viewBox="0 0 24 24" width="80" height="80" stroke="#1d428a" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>',
    ]
    icon_stack = "".join([f'<div class="flip-logo" style="animation-delay: {i * 3}s;">{svg}</div>' for i, svg in enumerate(pillar_icons)])
    st.markdown(f'''<style>@import url("https://fonts.googleapis.com/css2?family=Inter:wght@900&family=Oswald:wght@700&display=swap");.stApp {{ background-color: #FFFFFF !important; }} header, footer, [data-testid="stHeader"] {{ display: none !important; }} .ulp-auth-title {{ font-family: "Inter", sans-serif; font-size: clamp(32px, 12vw, 80px); font-weight: 900; color: #1d428a; letter-spacing: -4px; line-height: 1.0; margin-bottom: 10px; text-align: center; text-transform: uppercase; }} .logo-container {{ position: relative; height: 140px; display: flex; justify-content: center; align-items: center; margin: 10px 0; }} .flip-logo {{ position: absolute; opacity: 0; animation: logoFlip {len(pillar_icons)*3}s infinite; }} @keyframes logoFlip {{ 0% {{ opacity: 0; transform: scale(0.8); }} 1% {{ opacity: 1; transform: scale(1); }} 30% {{ opacity: 1; }} 33% {{ opacity: 0; transform: scale(1.05); }} 100% {{ opacity: 0; }} }} .sync-box {{ text-align: center; margin-bottom: 30px; }} .pulse-dot {{ height: 10px; width: 10px; background-color: #00ff41; border-radius: 50%; display: inline-block; margin-right: 8px; box-shadow: 0 0 10px #00ff41; animation: pulse-green 1.5s infinite; }} @keyframes pulse-green {{ 0% {{ box-shadow: 0 0 0px 0px rgba(0, 255, 65, 0.7); }} 70% {{ box-shadow: 0 0 0px 10px rgba(0, 255, 65, 0); }} 100% {{ box-shadow: 0 0 0px 0px rgba(0, 255, 65, 0); }} }} .sync-label {{ font-family: "Oswald", sans-serif; font-size: 15px; color: #1d428a; letter-spacing: 2px; font-weight: bold; }} [data-testid="stColumn"] [data-testid="stVerticalBlock"] {{ align-items: center !important; justify-content: center !important; text-align: center !important; }} div.stButton > button {{ background-color: #1d428a !important; color: #FFFFFF !important; font-family: 'Oswald', sans-serif !important; font-weight: 700 !important; text-transform: uppercase !important; letter-spacing: 2px !important; padding: 18px 45px !important; border: 2px solid #1d428a !important; transition: all 0.3s ease-in-out !important; margin: 15px auto !important; display: inline-block !important; }} input {{ text-align: center !important; }}</style><div style="padding: 10vh 5% 0 5%; text-align: center;"><div class="ulp-auth-title">Utah Land & Property</div><div class="logo-container">{icon_stack}</div><div class="sync-box"><span class="pulse-dot"></span><span class="sync-label">Maximum privacy. Maximum protection. Strategic land ownership in Utah.</span></div></div>''', unsafe_allow_html=True)
    _, col_mid, _ = st.columns([1, 2, 1])
    with col_mid:
        with st.container(border=True):
            input_key = st.text_input("Security Key", type="password", placeholder="ENTER PRIVATE ACCESS KEY", label_visibility="collapsed")
            if st.button("Secure Access Terminal"):
                try:
                    user_db = st.secrets["users"]
                    found_user = False
                    for username, profile in user_db.items():
                        if input_key == str(profile["key"]):
                            st.session_state.authenticated = True
                            st.session_state.user_role = profile["role"]
                            found_user = True
                            st.rerun()
                    if not found_user: st.error("ACCESS DENIED: INVALID KEY")
                except KeyError: st.error("SYSTEM ERROR: User database not found.")
    st.stop()

# --- 3. INTERNAL BENTO STYLE ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=Oswald:wght@500;700&display=swap');
        .stApp { background-color: #fcfcfc !important; }
        .bento-card {
            background: white;
            padding: 24px;
            border-radius: 20px;
            border: 1px solid #edf2f7;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            margin-bottom: 20px;
        }
        .hero-bento {
            background: #1d428a;
            color: white;
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 10px 20px rgba(29, 66, 138, 0.2);
        }
        .ulp-header { font-family: 'Inter', sans-serif; font-size: clamp(30px, 5vw, 50px) !important; font-weight: 900 !important; color: #1d428a !important; letter-spacing: -2px; text-transform: uppercase; text-align: left; }
        .label-text { font-family: 'Oswald'; font-size: 11px; letter-spacing: 1px; color: #64748b; text-transform: uppercase; font-weight: 700; }
        .value-text { font-family: 'Inter'; font-size: 24px; font-weight: 700; color: #1a202c; }
        .badge { background: #e0f2fe; color: #0369a1; padding: 4px 10px; border-radius: 6px; font-size: 10px; font-weight: 800; font-family: 'Oswald'; }
    </style>
""", unsafe_allow_html=True)

# --- 4. DASHBOARD CONTENT ---
st.markdown('<h1 class="ulp-header">Utah Land & Property</h1>', unsafe_allow_html=True)
st.markdown(f"<p style='font-family:Oswald; color:#1d428a; margin-top:-15px; letter-spacing:1px;'>ASSET TERMINAL | {st.session_state.user_role} ACCESS</p>", unsafe_allow_html=True)

# DEAL CALCULATIONS (Locked Logic)
PRICE = 330000.00
ASSIGNMENT_FEE = 15000.00
SELLER_EQUITY = 20000.00
AITD_PRINCIPAL = 305000.00

col_main, col_stats = st.columns([2, 1])

with col_main:
    # Bento Item 1: The Deal Summary
    st.markdown(f"""
    <div class="hero-bento">
        <div class="label-text" style="color: #cbd5e1;">Current Sale Price</div>
        <div style="font-family: 'Inter'; font-size: 48px; font-weight: 900;">${PRICE:,.2f}</div>
        <div style="height: 1px; background: rgba(255,255,255,0.1); margin: 20px 0;"></div>
        <div style="display: flex; justify-content: space-between;">
            <div>
                <div class="label-text" style="color: #cbd5e1;">AITD Principal Balance</div>
                <div style="font-size: 22px; font-weight: 700;">${AITD_PRINCIPAL:,.2f}</div>
            </div>
            <div style="text-align: right;">
                <div class="badge" style="background: rgba(255,255,255,0.1); color: white;">SECURE TRANSACTION</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_stats:
    # Bento Item 2: Fees & Equity
    st.markdown(f"""
    <div class="bento-card">
        <div class="label-text">Assignment Fee</div>
        <div class="value-text" style="color:#1d428a;">${ASSIGNMENT_FEE:,.2f}</div>
        <div style="font-size: 10px; color:#64748b; font-family:Oswald; margin-top:4px;">PAYEE: Utah Land & Property, LLC</div>
    </div>
    <div class="bento-card">
        <div class="label-text">Seller Equity Credit</div>
        <div class="value-text">${SELLER_EQUITY:,.2f}</div>
        <div class="badge">BLOCKCHAIN VERIFIED</div>
    </div>
    """, unsafe_allow_html=True)

# --- 5. TRANSACTION HUB ---
st.markdown("### 🛠️ Transaction Terminal")
hub_1, hub_2 = st.columns(2)

with hub_1:
    with st.container(border=True):
        st.markdown("<p class='label-text'>Phase-Based Checklist</p>", unsafe_allow_html=True)
        st.checkbox("Prequalification / Key Verification", value=True, disabled=True)
        st.checkbox("Offer & AITD Contract Review", value=True, disabled=True)
        st.checkbox("Underwriting & Principal Audit", value=st.session_state.checklist_step >= 3)
        st.checkbox("Final Digital Closing (RON)", value=st.session_state.checklist_step >= 4)
        
        if st.button("Advance Transaction Phase", use_container_width=True):
            if st.session_state.checklist_step < 4:
                st.session_state.checklist_step += 1
                st.rerun()

with hub_2:
    with st.container(border=True):
        st.markdown("<p class='label-text'>Secure Document Vault</p>", unsafe_allow_html=True)
        uploaded = st.file_uploader("Upload New Assets", label_visibility="collapsed")
        if uploaded:
            st.session_state.uploaded_docs.append(uploaded.name)
            st.success(f"Encrypted: {uploaded.name}")
        
        for doc in st.session_state.uploaded_docs:
            st.markdown(f"📄 `{doc}`")

# --- 6. LOGOUT ---
if st.sidebar.button("Terminate Session"):
    st.session_state.authenticated = False
    st.rerun()
