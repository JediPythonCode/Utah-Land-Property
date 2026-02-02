import streamlit as st
import base64
from streamlit_autorefresh import st_autorefresh
import io

# --- 1. CONFIG & STYLING ---
st.set_page_config(page_title="Utah Land & Property | Sovereign Portal", layout="wide", initial_sidebar_state="collapsed")
st_autorefresh(interval=30000, key="ulp_sync_ping")

# --- 2. PREMIUM CSS (THE "WOW" FACTOR) ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=Oswald:wght@300;700&display=swap');
        
        /* Base Theme */
        .stApp {
            background-color: #020617 !important;
            color: #f8fafc;
        }

        /* Cinematic Background */
        .stApp::before {
            content: "";
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: radial-gradient(circle at 20% 30%, rgba(30, 58, 138, 0.15) 0%, transparent 50%),
                        radial-gradient(circle at 80% 70%, rgba(67, 56, 202, 0.1) 0%, transparent 50%);
            z-index: -1;
        }

        /* Typography */
        .hero-title {
            font-family: 'Inter', sans-serif;
            font-size: clamp(40px, 10vw, 100px);
            font-weight: 900;
            line-height: 0.85;
            letter-spacing: -0.05em;
            text-align: center;
            background: linear-gradient(to right, #ffffff, #64748b);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-style: italic;
            margin-bottom: 10px;
        }

        .hero-subtitle {
            font-family: 'Oswald', sans-serif;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 0.5em;
            text-transform: uppercase;
            text-align: center;
            color: #3b82f6;
            margin-bottom: 50px;
        }

        /* Glassmorphism Cards */
        .glass-card {
            background: rgba(15, 23, 42, 0.6);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 24px;
            padding: 30px;
            margin-bottom: 20px;
            transition: all 0.3s ease;
        }
        
        .glass-card:hover {
            border-color: rgba(59, 130, 246, 0.5);
            background: rgba(15, 23, 42, 0.8);
        }

        /* Stats & Labels */
        .stat-label {
            font-family: 'Oswald', sans-serif;
            font-size: 10px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.2em;
            color: #64748b;
        }

        .stat-value {
            font-family: 'Inter', sans-serif;
            font-size: 42px;
            font-weight: 900;
            letter-spacing: -0.02em;
            color: #ffffff;
        }

        .equity-value {
            color: #3b82f6;
        }

        /* Form Styling */
        div.stButton > button {
            background: #ffffff !important;
            color: #020617 !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 900 !important;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            border-radius: 12px !important;
            border: none !important;
            height: 55px !important;
            width: 100%;
            transition: all 0.2s ease !important;
        }

        div.stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.4);
        }

        /* Inputs */
        .stTextInput input {
            background-color: rgba(0,0,0,0.4) !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            color: white !important;
            border-radius: 12px !important;
            text-align: center;
        }

        /* Hide Streamlit Branding */
        header, footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "deal" not in st.session_state:
    st.session_state.deal = {
        "address": "4402 SOUTH WASATCH BLVD",
        "price": 330000.0,
        "equity": 20000.0,
        "fee": 15000.0,
        "vault": []
    }

D = st.session_state.deal

# --- 4. AUTHENTICATION (LOGIN PAGE) ---
if not st.session_state.authenticated:
    st.markdown('<div style="height: 15vh;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">UTAH LAND<br>& PROPERTY</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Sovereign Asset Protection • Private Acquisition</div>', unsafe_allow_html=True)
    
    _, col_mid, _ = st.columns([1, 0.4, 1])
    with col_mid:
        access_key = st.text_input("AUTHORIZATION KEY", type="password", placeholder="••••••••", label_visibility="collapsed")
        if st.button("INITIALIZE SESSION"):
            if access_key.upper() in ["ADMIN2026", "CLIENT"]:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("ACCESS DENIED")
    st.stop()

# --- 5. DASHBOARD ---
# Header
st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 20px 0;">
        <div>
            <div class="stat-label">System Terminal</div>
            <div style="font-weight: 900; font-style: italic; letter-spacing: -1px;">ULP ACTIVE SESSION</div>
        </div>
        <div style="text-align: right;">
            <div class="stat-label">Asset Location</div>
            <div style="font-weight: 700;">SALT LAKE CITY, UT</div>
        </div>
    </div>
    <hr style="opacity: 0.1; margin-bottom: 40px;">
""", unsafe_allow_html=True)

col_main, col_side = st.columns([2, 1], gap="large")

with col_main:
    st.markdown('<div class="hero-title" style="text-align: left; font-size: 60px;">ASSET BRIEFING</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="color: #64748b; font-weight: 700; margin-bottom: 30px;">{D["address"]}</div>', unsafe_allow_html=True)

    # Financial Matrix
    st.markdown(f"""
        <div class="glass-card">
            <div class="stat-label">Purchase Consideration</div>
            <div class="stat-value">${D["price"]:,.2f}</div>
        </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
            <div class="glass-card">
                <div class="stat-label">Required Down (Equity)</div>
                <div class="stat-value equity-value">${D["equity"]:,.0f}</div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
            <div class="glass-card">
                <div class="stat-label">Assignment Fee</div>
                <div class="stat-value">${D["fee"]:,.0f}</div>
            </div>
        """, unsafe_allow_html=True)

    # Logic Balance
    st.markdown(f"""
        <div style="background: #3b82f6; padding: 40px; border-radius: 24px; color: white; margin-top: 20px;">
            <div class="stat-label" style="color: rgba(255,255,255,0.6)">Equity Buyer Balance</div>
            <div class="stat-value" style="font-size: 60px;">${(D["price"] - D["equity"]):,.2f}</div>
        </div>
    """, unsafe_allow_html=True)

with col_side:
    st.markdown('<div class="stat-label" style="margin-bottom: 20px;">Vault Onboarding</div>', unsafe_allow_html=True)
    
    docs = ["Government ID", "Proof of Funds", "Bank Statements", "Signed Agreement"]
    for doc in docs:
        st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 15px; background: rgba(255,255,255,0.03); padding: 15px; border-radius: 12px; margin-bottom: 10px; border: 1px solid rgba(255,255,255,0.05);">
                <div style="color: #3b82f6;">◈</div>
                <div style="font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;">{doc}</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="glass-card" style="padding: 20px;">', unsafe_allow_html=True)
        st.file_uploader("Upload to Vault", label_visibility="collapsed")
        st.button("ENCRYPT & UPLOAD")
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("TERMINATE SESSION"):
        st.session_state.authenticated = False
        st.rerun()
