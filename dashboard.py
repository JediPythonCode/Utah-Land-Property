import streamlit as st
import json
import os
import glob
import textwrap
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# --- 1. CONFIG & REFRESH ---
st.set_page_config(page_title="Utah Land & Property", layout="wide", initial_sidebar_state="collapsed")
st_autorefresh(interval=10000, key="ulp_live_ping")

# --- 2. AUTHENTICATION GATE ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    # Mimicking the flipping logo stack with Utah-themed landscape/architecture placeholders
    # In the original, these were NBA IDs; here we maintain the visual flip rhythm
    asset_ids = ["1", "2", "3", "4", "5"] 
    logo_stack = "".join([f'<div class="flip-logo" style="animation-delay: {i * 4}s; font-size: 80px;">🏔️</div>' for i in range(len(asset_ids))])

    st.markdown(f'''
    <style>
        @import url("https://fonts.googleapis.com/css2?family=Inter:wght@900&family=Oswald:wght@700&display=swap");
        .stApp {{ background-color: #FFFFFF !important; }}
        header, footer, [data-testid="stHeader"] {{ display: none !important; }}
        .nba-title-auth {{ font-family: "Inter", sans-serif; font-size: clamp(32px, 12vw, 80px); font-weight: 900; color: #1d428a; letter-spacing: -2px; line-height: 1.0; margin-bottom: 10px; text-align: center; text-transform: uppercase; }}
        .logo-container {{ position: relative; height: 140px; display: flex; justify-content: center; align-items: center; margin: 10px 0; }}
        .flip-logo {{ position: absolute; height: 110px; width: auto; opacity: 0; animation: logoFlip {len(asset_ids)*4}s infinite; }}
        @keyframes logoFlip {{ 0% {{ opacity: 0; transform: scale(0.8); }} 1% {{ opacity: 1; transform: scale(1); }} 18% {{ opacity: 1; }} 20% {{ opacity: 0; transform: scale(1.05); }} 100% {{ opacity: 0; }} }}
        .sync-box {{ text-align: center; margin-bottom: 30px; }}
        .pulse-dot {{ height: 10px; width: 10px; background-color: #00ff41; border-radius: 50%; display: inline-block; margin-right: 8px; box-shadow: 0 0 10px #00ff41; animation: pulse-green 1.5s infinite; }}
        @keyframes pulse-green {{ 0% {{ box-shadow: 0 0 0px 0px rgba(0, 255, 65, 0.7); }} 70% {{ box-shadow: 0 0 0px 10px rgba(0, 255, 65, 0); }} 100% {{ box-shadow: 0 0 0px 0px rgba(0, 255, 65, 0); }} }}
        .sync-label {{ font-family: "Oswald", sans-serif; font-size: 15px; color: #1d428a; letter-spacing: 2px; font-weight: bold; }}
    </style>
    <div style="padding: 10vh 5% 0 5%; text-align: center;">
        <div class="nba-title-auth">Utah Land & Property</div>
        <div class="logo-container">{logo_stack}</div>
        <div class="sync-box"><span class="pulse-dot"></span><span class="sync-label">ASSET PROTECTION FRAMEWORK</span></div>
    </div>
    ''', unsafe_allow_html=True)

    _, col_mid, _ = st.columns([1, 5, 1])
    with col_mid:
        with st.container(border=True):
            pwd = st.text_input("Key", type="password", placeholder="ENTER PRIVATE ACCESS KEY", label_visibility="collapsed")
            if st.button("AUTHENTICATE", use_container_width=True):
                # Using standard access logic for a single private terminal
                if pwd == st.secrets["PASSWORDS"]["ADMIN"]:
                    st.session_state.authenticated = True
                    st.rerun()
                else: st.error("ACCESS DENIED")
    st.stop()

# --- 3. THEME & ADVANCED CSS ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@900&family=Oswald:wght@700&display=swap');
        .stApp { background-color: #FFFFFF !important; }
        header[data-testid="stHeader"] { visibility: hidden; display: none; }
        .block-container { padding-top: 1rem !important; }
        .nba-title { font-family: 'Inter', sans-serif; font-size: clamp(40px, 10vw, 85px) !important; font-weight: 900 !important; color: #1d428a !important; letter-spacing: -4px; line-height: 0.85; margin-bottom: 5px; text-align: center; text-transform: uppercase; }
        
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
        .m-title-white { color: #ffffff !important; font-family: 'Inter', sans-serif !important; font-weight: 900 !important; font-size: 20px !important; text-transform: uppercase !important; margin: 15px 0 !important; text-shadow: 2px 2px 4px rgba(0,0,0,0.5) !important; }
        .label-white { font-family: 'Oswald', sans-serif !important; font-size: 12px !important; color: #ffffff !important; letter-spacing: 2px !important; font-weight: 900 !important; }
        .value-white { font-family: 'Oswald', sans-serif !important; font-size: 20px !important; font-weight: 700 !important; color: #ffffff !important; }
        .target-box-dark { background: #111111 !important; border-radius: 8px; padding: 15px; width: 100%; margin-top: auto; border: 1px solid #333; }
        .target-white-value { font-family: 'Oswald', sans-serif !important; font-size: 18px !important; font-weight: 900 !important; color: #ffffff !important; text-transform: uppercase !important; }
        .intel-header { background: linear-gradient(to right, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c) !important; -webkit-background-clip: text !important; -webkit-text-fill-color: transparent !important; font-family: 'Inter', sans-serif !important; font-weight: 900 !important; font-size: clamp(30px, 10vw, 65px) !important; text-align: center !important; text-transform: uppercase; }
        
        .sync-container { text-align: center; margin-bottom: 20px; }
        .green-pulse { height: 10px; width: 10px; background-color: #00ff41; border-radius: 50%; display: inline-block; margin-right: 8px; box-shadow: 0 0 10px #00ff41; animation: pulse-green 1.5s infinite; }
        @keyframes pulse-green { 0% { box-shadow: 0 0 0px 0px rgba(0, 255, 65, 0.7); } 70% { box-shadow: 0 0 0px 10px rgba(0, 255, 65, 0); } 100% { box-shadow: 0 0 0px 0px rgba(0, 255, 65, 0); } }
        .sync-text { font-family: 'Oswald', sans-serif; font-size: 14px; color: #1d428a; letter-spacing: 1px; }
    </style>
""", unsafe_allow_html=True)

# --- 4. HEADER ---
st.markdown(f'''<div style="text-align: center;"><h1 class="nba-title">Utah Land & Property</h1><div class="sync-container"><span class="green-pulse"></span><span class="sync-text">STRATEGIC NODE ACTIVE: {datetime.now().strftime("%H:%M:%S")}</span></div></div>''', unsafe_allow_html=True)

# --- 5. STRATEGIC OVERVIEW (REPLACING NBA STORIES) ---
st.markdown("""
    <div style="height:400px; overflow-y:auto; border-radius:15px; border:2px solid #1d428a; background-color: #f8fafc; padding: 40px; font-family: 'Inter', sans-serif; color: #1a3c6d;">
        <h2 style="font-weight: 900; text-transform: uppercase; letter-spacing: -1px;">Framework Philosophy</h2>
        <p style="font-size: 18px; line-height: 1.6;">Utah Land & Property serves as a sophisticated strategic framework — dedicated to helping discerning individuals and families preserve and grow wealth through expertly structured land ownership in Utah. At its core, the approach integrates robust asset protection, maximum privacy, and creative financing techniques.</p>
        <p style="font-size: 18px; line-height: 1.6;">Leveraging Utah's favorable legal environment, strong property rights tradition, and stunning natural landscapes to create enduring value. Whether you're safeguarding generational wealth or deploying capital via layered trusts and anonymous LLC holdings, this terminal provides the discretion needed in today's complex world.</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("""<div style="text-align:center; padding: 40px 0;"><h1 class="intel-header">Asset Intelligence</h1><div style="color:#111; font-family:Oswald; letter-spacing:10px; font-size:16px; font-weight:900; margin-top:5px;">OMNI-STACK ACTIVE</div></div>""", unsafe_allow_html=True)

# --- 6. DATA LOADING (Mirroring the JSON structure) ---
@st.cache_data(ttl=60)
def load_vault_data():
    # Placeholder for property holdings/trust data
    return {
        "holdings": [
            {"id": "UT-001", "name": "Summit layered Trust", "protection": "MAXIMUM", "vehicle": "Anonymous LLC", "status": "SECURED"},
            {"id": "UT-002", "name": "Red Rock Land Trust", "protection": "HIGH", "vehicle": "Land Trust", "status": "ACTIVE"},
            {"id": "UT-003", "name": "Wasatch Holding", "protection": "MAXIMUM", "vehicle": "Layered Trust", "status": "VERIFIED"}
        ]
    }

holdings = load_vault_data().get("holdings", [])

# --- 7. INTEL CARDS ---
if holdings:
    cols = st.columns(3)
    for i, asset in enumerate(holdings):
        with cols[i % 3]:
            card_html = textwrap.dedent(f"""
                <div class="gold-card">
                    <div class="signal-badge">STRATEGIC HOLDING</div>
                    <div style="font-size: 50px;">🏗️</div>
                    <span class="m-title-white">{asset['name']}</span>
                    <div class="label-white">PROTECTION LEVEL</div>
                    <div class="value-white">{asset['protection']}</div>
                    <div class="label-white">STRUCTURE</div>
                    <div class="value-white" style="font-size:15px; color:#1a1a1a !important;">{asset['vehicle']}</div>
                    <div class="target-box-dark">
                        <div style="font-family:Oswald; font-size:10px; color:#00ff41; font-weight:bold; letter-spacing:1px;">ASSET STATUS</div>
                        <div class="target-white-value">{asset['status']}</div>
                    </div>
                </div>
            """)
            st.markdown(card_html, unsafe_allow_html=True)
            st.button("ACCESS LEDGER", key=f"btn_{asset['id']}", use_container_width=True)

# --- 8. EXTERNAL TERMINAL ---
st.markdown("---")
st.markdown("<h5 style='text-align: center; color: #1d428a; letter-spacing: 2px; font-family: Oswald;'>INTELLIGENCE RESOURCES</h5>", unsafe_allow_html=True)
link_cols = st.columns(4)
link_cols[0].link_button("⚖️ Utah Property Rights", "https://propertyrights.utah.gov/", use_container_width=True)
link_cols[1].link_button("📜 Trust Statutes", "https://le.utah.gov/", use_container_width=True)
link_cols[2].link_button("🏢 LLC Division", "https://corporations.utah.gov/", use_container_width=True)
link_cols[3].link_button("🗺️ GIS Mapping", "https://trustlands.utah.gov/", use_container_width=True)

# --- 9. PRODUCTION FOOTER ---
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown(f"""
    <div style="display: flex; justify-content: center; gap: 30px; opacity: 0.8; font-size: 11px; font-family: 'Oswald'; color: #1d428a;">
        <div style="display: flex; align-items: center;"><span class="green-pulse" style="height:6px; width:6px; margin-right:5px;"></span>NODE: UTAH STRATEGIC</div>
        <div>STATUS: ENCRYPTED & SYNCED</div>
        <div style="font-weight: bold;">© 2026 UTAH LAND & PROPERTY | ASSET PROTECTION</div>
    </div>
""", unsafe_allow_html=True)
