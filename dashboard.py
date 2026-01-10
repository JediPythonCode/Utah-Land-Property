import streamlit as st
import json
import os
import glob
import textwrap
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# --- 1. CONFIG & REFRESH ---
st.set_page_config(page_title="Utah Land & Property", layout="wide", initial_sidebar_state="collapsed")
st_autorefresh(interval=10000, key="ulp_sync_ping")

# --- 2. AUTHENTICATION GATE (EXACT ARCHITECTURAL MIMIC) ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    # Mimicking the flipping engine but using strategic wealth icons instead of logos
    pillar_icons = ["🛡️", "⚖️", "🔒", "🏔️", "📜", "💼"]
    icon_stack = "".join([f'<div class="flip-logo" style="animation-delay: {i * 2}s; font-size: 70px;">{icon}</div>' for i, icon in enumerate(pillar_icons)])

    st.markdown(f'''
    <style>
        @import url("https://fonts.googleapis.com/css2?family=Inter:wght@900&family=Oswald:wght@700&display=swap");
        .stApp {{ background-color: #FFFFFF !important; }}
        header, footer, [data-testid="stHeader"] {{ display: none !important; }}
        .nba-title-auth {{ font-family: "Inter", sans-serif; font-size: clamp(32px, 12vw, 80px); font-weight: 900; color: #1d428a; letter-spacing: -2px; line-height: 1.0; margin-bottom: 10px; text-align: center; text-transform: uppercase; }}
        .logo-container {{ position: relative; height: 140px; display: flex; justify-content: center; align-items: center; margin: 10px 0; }}
        .flip-logo {{ position: absolute; opacity: 0; animation: logoFlip {len(pillar_icons)*2}s infinite; }}
        @keyframes logoFlip {{ 0% {{ opacity: 0; transform: scale(0.8); }} 5% {{ opacity: 1; transform: scale(1); }} 15% {{ opacity: 1; }} 20% {{ opacity: 0; transform: scale(1.05); }} 100% {{ opacity: 0; }} }}
        .sync-box {{ text-align: center; margin-bottom: 30px; }}
        .pulse-dot {{ height: 10px; width: 10px; background-color: #00ff41; border-radius: 50%; display: inline-block; margin-right: 8px; box-shadow: 0 0 10px #00ff41; animation: pulse-green 1.5s infinite; }}
        @keyframes pulse-green {{ 0% {{ box-shadow: 0 0 0px 0px rgba(0, 255, 65, 0.7); }} 70% {{ box-shadow: 0 0 0px 10px rgba(0, 255, 65, 0); }} 100% {{ box-shadow: 0 0 0px 0px rgba(0, 255, 65, 0); }} }}
        .sync-label {{ font-family: "Oswald", sans-serif; font-size: 15px; color: #1d428a; letter-spacing: 2px; font-weight: bold; }}
    </style>
    <div style="padding: 10vh 5% 0 5%; text-align: center;">
        <div class="nba-title-auth">Utah Land & Property</div>
        <div class="logo-container">{icon_stack}</div>
        <div class="sync-box"><span class="pulse-dot"></span><span class="sync-label">SECURE STRATEGIC TERMINAL</span></div>
    </div>
    ''', unsafe_allow_html=True)

    _, col_mid, _ = st.columns([1, 4, 1])
    with col_mid:
        with st.container(border=True):
            pwd = st.text_input("Key", type="password", placeholder="ENTER PRIVATE ACCESS KEY", label_visibility="collapsed")
            if st.button("AUTHENTICATE TERMINAL", use_container_width=True):
                if pwd in [st.secrets["PASSWORDS"]["ADMIN"], st.secrets["PASSWORDS"]["PARTNER"]]:
                    st.session_state.authenticated = True
                    st.rerun()
                else: st.error("ACCESS DENIED")
    st.stop()

# --- 3. THEME & ADVANCED CSS (EXACT REPLICA) ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@900&family=Oswald:wght@700&display=swap');
        .stApp { background-color: #FFFFFF !important; }
        header[data-testid="stHeader"] { visibility: hidden; display: none; }
        .block-container { padding-top: 1rem !important; }
        
        /* HEADER REPLICA */
        .nba-title { font-family: 'Inter', sans-serif; font-size: clamp(40px, 12vw, 85px) !important; font-weight: 900 !important; color: #1d428a !important; letter-spacing: -4px; line-height: 0.85; margin-bottom: 5px; text-align: center; text-transform: uppercase; }
        
        /* GOLD CARD REPLICA */
        .gold-card { 
            background-color: #FDD017 !important; 
            background-image: url("https://www.transparenttextures.com/patterns/carbon-fibre.png") !important; 
            border-top: 6px solid #1a1a1a !important; 
            border-radius: 0px 20px 0px 20px !important; 
            padding: 25px !important; text-align: center !important; 
            display: flex !important; flex-direction: column !important; align-items: center !important; 
            margin-bottom: 10px !important; min-height: 380px !important; 
            box-shadow: 0 12px 25px rgba(0,0,0,0.3) !important;
        }
        
        .signal-badge { background: #1a1a1a; color: #00ff41; padding: 2px 12px; border-radius: 4px; font-family: 'Oswald', sans-serif; font-size: 10px; letter-spacing: 2px; margin-bottom: 10px; border: 1px solid #00ff41; }
        .m-title-white { color: #ffffff !important; font-family: 'Inter', sans-serif !important; font-weight: 900 !important; font-size: 24px !important; text-transform: uppercase !important; margin: 15px 0 !important; text-shadow: 2px 2px 4px rgba(0,0,0,0.5) !important; }
        .label-white { font-family: 'Oswald', sans-serif !important; font-size: 14px !important; color: #ffffff !important; letter-spacing: 2px !important; font-weight: 900 !important; }
        .value-white { font-family: 'Oswald', sans-serif !important; font-size: 22px !important; font-weight: 700 !important; color: #ffffff !important; }
        .target-box-dark { background: #111111 !important; border-radius: 8px; padding: 20px; width: 100%; margin-top: auto; border: 1px solid #333; }
        .target-white-value { font-family: 'Oswald', sans-serif !important; font-size: 20px !important; font-weight: 900 !important; color: #ffffff !important; text-transform: uppercase !important; }
        
        /* GOLD GRADIENT HEADER REPLICA */
        .intel-header { background: linear-gradient(to right, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c) !important; -webkit-background-clip: text !important; -webkit-text-fill-color: transparent !important; font-family: 'Inter', sans-serif !important; font-weight: 900 !important; font-size: clamp(35px, 12vw, 65px) !important; text-align: center !important; text-transform: uppercase; }
        
        .sync-container { text-align: center; margin-bottom: 20px; }
        .green-pulse { height: 10px; width: 10px; background-color: #00ff41; border-radius: 50%; display: inline-block; margin-right: 8px; box-shadow: 0 0 10px #00ff41; animation: pulse-green 1.5s infinite; }
    </style>
""", unsafe_allow_html=True)

# --- 4. DATA LOGIC ---
assets = [
    {"name": "Summit Layered Trust", "protection": "MAXIMUM", "status": "VERIFIED", "vehicle": "Anonymous LLC"},
    {"name": "Red Rock Land Trust", "protection": "REDUNDANT", "status": "SECURED", "vehicle": "Land Trust"},
    {"name": "Wasatch Holdings", "protection": "MAXIMUM", "status": "SYNCED", "vehicle": "Layered Trust"}
]

# --- 5. HEADER (EXACT REPLICA) ---
st.markdown(f'''<div style="text-align: center;"><h1 class="nba-title">Utah Land & Property</h1><div class="sync-container"><span class="green-pulse"></span><span style="font-family:Oswald; color:#1d428a; letter-spacing:1px;">STATION SYNC: {datetime.now().strftime("%H:%M:%S")}</span></div></div>''', unsafe_allow_html=True)

# --- 6. PHILOSOPHY FRAMEWORK ---
st.markdown("""
    <div style="border-radius:15px; border:2px solid #1d428a; background-color: white; padding: 30px; color: #1d428a; font-family: 'Inter';">
        <h3 style="font-weight: 900; text-transform: uppercase;">Strategic Framework Overview</h3>
        <p style="font-size: 17px; line-height: 1.6;"><b>Utah Land & Property</b> serves as a sophisticated strategic framework — dedicated to helping discerning individuals and families preserve and grow wealth through expertly structured land ownership in Utah. At its core, the approach integrates robust asset protection, maximum privacy, and creative financing techniques.</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("""<div style="text-align:center; padding: 40px 0;"><h1 class="intel-header">Asset Intelligence</h1><div style="color:#111; font-family:Oswald; letter-spacing:10px; font-size:16px; font-weight:900; margin-top:5px;">OMNI-STACK ACTIVE</div></div>""", unsafe_allow_html=True)



# --- 7. INTEL CARDS ---
cols = st.columns(3)
for i, asset in enumerate(assets):
    with cols[i % 3]:
        st.markdown(f"""
            <div class="gold-card">
                <div class="signal-badge">OMNI-SYNC ACTIVE</div>
                <div style="font-size: 50px;">🏔️</div>
                <span class="m-title-white" style="font-size:20px !important;">{asset['name']}</span>
                <div class="label-white">PROTECTION LEVEL</div>
                <div class="value-white">{asset['protection']}</div>
                <div class="label-white">VEHICLE</div>
                <div class="value-white" style="font-size:15px; color:#1a1a1a !important;">{asset['vehicle']}</div>
                <div class="target-box-dark">
                    <div style="font-family:Oswald; font-size:10px; color:#00ff41; font-weight:bold; letter-spacing:1px;">SYNC STATUS</div>
                    <div class="target-white-value">{asset['status']}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.button("OPEN LEDGER", key=f"btn_{i}", use_container_width=True)

# --- 8. PRODUCTION FOOTER ---
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown(f"""
    <div style="display: flex; justify-content: center; gap: 30px; opacity: 0.8; font-size: 11px; font-family: 'Oswald'; color: #1d428a;">
        <div style="display: flex; align-items: center;"><span class="green-pulse" style="height:6px; width:6px; margin-right:5px;"></span>NODE: UTAH-STRATEGIC-PRIMARY</div>
        <div>STATUS: ENCRYPTED & SYNCED</div>
        <div style="font-weight: bold;">© 2026 UTAH LAND & PROPERTY | TRANSACTION TERMINAL</div>
    </div>
""", unsafe_allow_html=True)
