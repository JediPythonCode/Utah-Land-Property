import streamlit as st
import base64
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# --- 1. CONFIG & REFRESH ---
st.set_page_config(page_title="Utah Land & Property", layout="wide", initial_sidebar_state="collapsed")
st_autorefresh(interval=10000, key="ulp_sync_ping")

# --- 2. DATA PERSISTENCE ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_role = None

if "current_deal" not in st.session_state:
    st.session_state.current_deal = {
        "deal_id": "DEAL-PRIMARY",
        "price": 330000.00,
        "seller_equity": 20000.00,
        "assignment_fee": 15000.00,
        "vault": [],
        "notes": []
    }

# --- 3. AUTH SCREEN (FIXED ALIGNMENT) ---
if not st.session_state.authenticated:
    pillar_icons = [
        '<svg viewBox="0 0 24 24" width="80" height="80" stroke="#1d428a" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>',
        '<svg viewBox="0 0 24 24" width="80" height="80" stroke="#1d428a" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>',
    ]
    icon_stack = "".join([f'<div class="flip-logo" style="animation-delay: {i * 3}s;">{svg}</div>' for i, svg in enumerate(pillar_icons)])
    
    st.markdown(f'''
        <style>
        @import url("https://fonts.googleapis.com/css2?family=Inter:wght@900&family=Oswald:wght@700&display=swap");
        .stApp {{ background-color: #FFFFFF !important; }}
        [data-testid="stHeader"] {{ display: none !important; }}
        
        .auth-container {{
            max-width: 600px;
            margin: 0 auto;
            padding-top: 10vh;
            text-align: center;
        }}
        
        .ulp-auth-title {{ font-family: "Inter", sans-serif; font-size: clamp(30px, 7vw, 70px); font-weight: 900; color: #1d428a; letter-spacing: -3px; line-height: 1.0; margin-bottom: 5px; text-transform: uppercase; }}
        .logo-container {{ position: relative; height: 120px; display: flex; justify-content: center; align-items: center; margin: 15px 0; }}
        .flip-logo {{ position: absolute; opacity: 0; animation: logoFlip {len(pillar_icons)*3}s infinite; }}
        @keyframes logoFlip {{ 0% {{ opacity: 0; transform: scale(0.8); }} 1% {{ opacity: 1; transform: scale(1); }} 30% {{ opacity: 1; }} 33% {{ opacity: 0; transform: scale(1.05); }} 100% {{ opacity: 0; }} }}
        
        .sync-box {{ margin-bottom: 25px; }}
        .pulse-dot {{ height: 8px; width: 8px; background-color: #00ff41; border-radius: 50%; display: inline-block; margin-right: 8px; box-shadow: 0 0 10px #00ff41; animation: pulse-green 1.5s infinite; }}
        @keyframes pulse-green {{ 0% {{ box-shadow: 0 0 0px 0px rgba(0, 255, 65, 0.7); }} 70% {{ box-shadow: 0 0 0px 10px rgba(0, 255, 65, 0); }} 100% {{ box-shadow: 0 0 0px 0px rgba(0, 255, 65, 0); }} }}
        .sync-label {{ font-family: "Oswald", sans-serif; font-size: 14px; color: #1d428a; letter-spacing: 1.5px; font-weight: bold; text-transform: uppercase; }}
        
        /* Input & Button Alignment */
        div[data-testid="stTextInput"] > div {{ border: none !important; }}
        div[data-testid="stTextInput"] input {{
            text-align: center !important;
            border: 2px solid #1d428a !important;
            border-radius: 4px !important;
            font-size: 18px !important;
            color: #1d428a !important;
        }}
        div.stButton > button {{
            background-color: #1d428a !important;
            color: #FFFFFF !important;
            width: 100%;
            border-radius: 4px !important;
            font-family: 'Oswald', sans-serif !important;
            letter-spacing: 1px !important;
            border: none !important;
            padding: 10px 0 !important;
        }}
        </style>
        <div class="auth-container">
            <div class="ulp-auth-title">Utah Land & Property</div>
            <div class="logo-container">{icon_stack}</div>
            <div class="sync-box">
                <span class="pulse-dot"></span>
                <span class="sync-label">Secure Access Terminal Active</span>
            </div>
        </div>
    ''', unsafe_allow_html=True)
    
    _, col_mid, _ = st.columns([1, 1, 1])
    with col_mid:
        input_key = st.text_input("Key", type="password", placeholder="ENTER SECURITY KEY", label_visibility="collapsed")
        if st.button("AUTHORIZE ACCESS"):
            try:
                user_db = st.secrets["users"]
                auth_success = False
                for u, p in user_db.items():
                    if input_key == str(p["key"]):
                        st.session_state.authenticated = True
                        st.session_state.user_role = p["role"]
                        auth_success = True
                        st.rerun()
                if not auth_success:
                    st.error("INVALID KEY")
            except: st.error("DATABASE CONNECTION ERROR")
    st.stop()

# --- 4. DASHBOARD STYLING ---
st.markdown("""
    <style>
        .stApp { background-color: #ffffff; }
        .hero-bento { background: #1d428a; color: white; padding: 30px; border-radius: 8px; }
        .bento-card { background: #f8fafc; padding: 20px; border-radius: 8px; border: 1px solid #e2e8f0; }
        .label { font-family: 'Oswald'; font-size: 12px; letter-spacing: 1px; color: #64748b; text-transform: uppercase; }
        .hero-label { font-family: 'Oswald'; font-size: 12px; letter-spacing: 1px; color: #cbd5e1; text-transform: uppercase; }
    </style>
""", unsafe_allow_html=True)

# --- 5. LOGIC & DISPLAY ---
D = st.session_state.current_deal
# CORRECTED MATH: Principal = Sales Price - Seller Equity
AITD_PRINCIPAL = D["price"] - D["seller_equity"]

st.title("UTAH LAND & PROPERTY")

c1, c2 = st.columns([2, 1])
with c1:
    st.markdown(f"""
        <div class="hero-bento">
            <div class="hero-label">AITD Principal Balance</div>
            <div style="font-size: 64px; font-weight: 900;">${AITD_PRINCIPAL:,.2f}</div>
            <hr style="opacity: 0.2; margin: 20px 0;">
            <div style="display: flex; justify-content: space-between;">
                <div><div class="hero-label">Original Price</div><div style="font-size: 20px;">${D['price']:,.2f}</div></div>
                <div style="text-align: right;"><div class="hero-label">Seller Equity</div><div style="font-size: 20px;">${D['seller_equity']:,.2f}</div></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
        <div class="bento-card">
            <div class="label">ULP Assignment Fee</div>
            <div style="font-size: 32px; font-weight: 700; color: #1d428a;">${D['assignment_fee']:,.2f}</div>
            <p style="font-size: 11px; margin-top: 10px; color: #64748b;">Assignment fee for services rendered by Utah Land & Property, LLC.</p>
        </div>
    """, unsafe_allow_html=True)

if st.sidebar.button("LOGOUT"):
    st.session_state.authenticated = False
    st.rerun()
