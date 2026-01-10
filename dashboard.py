import streamlit as st
import textwrap
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# --- 1. CONFIG & REFRESH ---
st.set_page_config(page_title="Utah Land & Property", layout="wide", initial_sidebar_state="collapsed")
st_autorefresh(interval=10000, key="ulp_sync_ping")

# --- 2. AUTHENTICATION GATE & BUTTON HOVER STYLING ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    pillars = ["🛡️", "⚖️", "🔒", "🏔️", "💼", "📜"]
    icon_stack = "".join([f'<div class="flip-logo" style="animation-delay: {i * 3}s; font-size: 80px;">{p}</div>' for i, p in enumerate(pillars)])

    st.markdown(f'''
    <style>
        @import url("https://fonts.googleapis.com/css2?family=Inter:wght@900&family=Oswald:wght@700&display=swap");
        .stApp {{ background-color: #FFFFFF !important; }}
        header, footer, [data-testid="stHeader"] {{ display: none !important; }}
        
        .ulp-auth-title {{ 
            font-family: "Inter", sans-serif; 
            font-size: clamp(32px, 12vw, 80px); 
            font-weight: 900; 
            color: #1d428a; 
            letter-spacing: -4px; 
            line-height: 1.0; 
            margin-bottom: 10px; 
            text-align: center; 
            text-transform: uppercase; 
        }}
        
        .logo-container {{ position: relative; height: 140px; display: flex; justify-content: center; align-items: center; margin: 10px 0; }}
        .flip-logo {{ position: absolute; opacity: 0; animation: logoFlip {len(pillars)*3}s infinite; }}
        @keyframes logoFlip {{ 0% {{ opacity: 0; transform: scale(0.8); }} 1% {{ opacity: 1; transform: scale(1); }} 15% {{ opacity: 1; }} 20% {{ opacity: 0; transform: scale(1.05); }} 100% {{ opacity: 0; }} }}
        
        .sync-box {{ text-align: center; margin-bottom: 30px; }}
        .pulse-dot {{ height: 10px; width: 10px; background-color: #00ff41; border-radius: 50%; display: inline-block; margin-right: 8px; box-shadow: 0 0 10px #00ff41; animation: pulse-green 1.5s infinite; }}
        @keyframes pulse-green {{ 0% {{ box-shadow: 0 0 0px 0px rgba(0, 255, 65, 0.7); }} 70% {{ box-shadow: 0 0 0px 10px rgba(0, 255, 65, 0); }} 100% {{ box-shadow: 0 0 0px 0px rgba(0, 255, 65, 0); }} }}
        .sync-label {{ font-family: "Oswald", sans-serif; font-size: 15px; color: #1d428a; letter-spacing: 2px; font-weight: bold; }}

        /* EXACT BUTTON HOVER: BLUE TO WHITE FLIP */
        div.stButton > button {{
            background-color: #1d428a !important;
            color: #FFFFFF !important;
            font-family: 'Oswald', sans-serif !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            letter-spacing: 2px !important;
            padding: 18px !important;
            border: 2px solid #1d428a !important;
            transition: all 0.3s ease-in-out !important;
            width: 100% !important;
        }}
        div.stButton > button:hover, div.stButton > button:active, div.stButton > button:focus {{
            background-color: #FFFFFF !important;
            color: #1d428a !important;
            border: 2px solid #1d428a !important;
        }}
    </style>
    
    <div style="padding: 10vh 5% 0 5%; text-align: center;">
        <div class="ulp-auth-title">Utah Land & Property</div>
        <div class="logo-container">{icon_stack}</div>
        <div class="sync-box"><span class="pulse-dot"></span><span class="sync-label">WEALTH PRESERVATION TERMINAL</span></div>
    </div>
    ''', unsafe_allow_html=True)

    _, col_mid, _ = st.columns([1, 4, 1])
    with col_mid:
        with st.container(border=True):
            pwd = st.text_input("Key", type="password", placeholder="ENTER PRIVATE ACCESS KEY", label_visibility="collapsed")
            if st.button("Access Secure Transaction Terminal"):
                # REINFORCED PASSWORD LOGIC
                try:
                    # Check if secrets exist to prevent KeyError
                    if "PASSWORDS" in st.secrets and "ADMIN" in st.secrets["PASSWORDS"]:
                        if pwd == st.secrets["PASSWORDS"]["ADMIN"]:
                            st.session_state.authenticated = True
                            st.rerun()
                        else:
                            st.error("ACCESS DENIED: INVALID SECURITY KEY")
                    else:
                        st.error("SYSTEM ERROR: Secrets file is missing [PASSWORDS] block.")
                except Exception as e:
                    st.error(f"SYSTEM ERROR: {str(e)}")
    st.stop()

# --- 3. INTERNAL DASHBOARD STYLE ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@900&family=Oswald:wght@700&display=swap');
        .stApp { background-color: #FFFFFF !important; }
        .ulp-header { font-family: 'Inter', sans-serif; font-size: clamp(40px, 12vw, 85px) !important; font-weight: 900 !important; color: #1d428a !important; letter-spacing: -4px; line-height: 0.85; margin-bottom: 5px; text-align: center; text-transform: uppercase; }
        .intel-header { background: linear-gradient(to right, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c) !important; -webkit-background-clip: text !important; -webkit-text-fill-color: transparent !important; font-family: 'Inter', sans-serif !important; font-weight: 900 !important; font-size: clamp(35px, 12vw, 65px) !important; text-align: center !important; text-transform: uppercase; }
        .gold-card { background-color: #FDD017 !important; background-image: url("https://www.transparenttextures.com/patterns/carbon-fibre.png") !important; border-top: 6px solid #1a1a1a !important; border-radius: 0px 20px 0px 20px !important; padding: 25px !important; text-align: center !important; margin-bottom: 15px; box-shadow: 0 12px 25px rgba(0,0,0,0.3) !important; }
        .m-title-white { color: #ffffff !important; font-family: 'Inter', sans-serif !important; font-weight: 900 !important; font-size: 24px !important; text-transform: uppercase !important; margin: 15px 0 !important; text-shadow: 2px 2px 4px rgba(0,0,0,0.5) !important; }
        .green-pulse { height: 10px; width: 10px; background-color: #00ff41; border-radius: 50%; display: inline-block; margin-right: 8px; box-shadow: 0 0 10px #00ff41; animation: pulse-green 1.5s infinite; }
    </style>
""", unsafe_allow_html=True)

# --- 4. DASHBOARD HEADER ---
st.markdown(f'''<div style="text-align: center;"><h1 class="ulp-header">Utah Land & Property</h1><div style="margin-bottom: 20px;"><span class="green-pulse"></span><span style="font-family: 'Oswald'; font-size: 14px; color: #1d428a; letter-spacing: 1px;">STRATEGIC SYNC: {datetime.now().strftime("%H:%M:%S")}</span></div></div>''', unsafe_allow_html=True)

# --- 5. ASSET INTEL SECTION ---
st.markdown("""<div style="text-align:center; padding: 40px 0;"><h1 class="intel-header">Asset Intelligence</h1><div style="color:#111; font-family:Oswald; letter-spacing:10px; font-size:16px; font-weight:900; margin-top:5px;">OMNI-STACK ACTIVE</div></div>""", unsafe_allow_html=True)



col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('''
        <div class="gold-card">
            <div style="background: #1a1a1a; color: #00ff41; padding: 2px 12px; border-radius: 4px; font-family: 'Oswald'; font-size: 10px; letter-spacing: 2px; margin-bottom: 10px; border: 1px solid #00ff41; display: inline-block;">SYNC ACTIVE</div>
            <div style="font-size: 50px;">🛡️</div>
            <span class="m-title-white">Summit Layered Trust</span>
            <div style="background: #111111; border-radius: 8px; padding: 20px; width: 100%; margin-top: 15px; border: 1px
