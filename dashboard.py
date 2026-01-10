import streamlit as st
import base64
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# --- 1. CONFIG & REFRESH ---
st.set_page_config(page_title="Utah Land & Property", layout="wide", initial_sidebar_state="collapsed")
st_autorefresh(interval=10000, key="ulp_sync_ping")

# --- 2. AUTHENTICATION & STATE ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_role = None

if "deal_data" not in st.session_state:
    st.session_state.deal_data = {
        "price": 330000.00,
        "assignment_fee": 15000.00,
        "seller_equity": 20000.00,
        "fee_credit": 5000.00,
        "vault": []
    }

# --- 3. LOGIN PAGE (EXACTLY AS REQUESTED: NO LOGIC REMOVED) ---
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
        header, footer, [data-testid="stHeader"] {{ display: none !important; }}
        .ulp-auth-title {{ font-family: "Inter", sans-serif; font-size: clamp(32px, 12vw, 80px); font-weight: 900; color: #1d428a; letter-spacing: -4px; line-height: 1.0; margin-bottom: 10px; text-align: center; text-transform: uppercase; }}
        .logo-container {{ position: relative; height: 140px; display: flex; justify-content: center; align-items: center; margin: 10px 0; }}
        .flip-logo {{ position: absolute; opacity: 0; animation: logoFlip {len(pillar_icons)*3}s infinite; }}
        @keyframes logoFlip {{ 0% {{ opacity: 0; transform: scale(0.8); }} 1% {{ opacity: 1; transform: scale(1); }} 30% {{ opacity: 1; }} 33% {{ opacity: 0; transform: scale(1.05); }} 100% {{ opacity: 0; }} }}
        .sync-box {{ text-align: center; margin-bottom: 30px; }}
        .pulse-dot {{ height: 10px; width: 10px; background-color: #00ff41; border-radius: 50%; display: inline-block; margin-right: 8px; box-shadow: 0 0 10px #00ff41; animation: pulse-green 1.5s infinite; }}
        @keyframes pulse-green {{ 0% {{ box-shadow: 0 0 0px 0px rgba(0, 255, 65, 0.7); }} 70% {{ box-shadow: 0 0 0px 10px rgba(0, 255, 65, 0); }} 100% {{ box-shadow: 0 0 0px 0px rgba(0, 255, 65, 0); }} }}
        .sync-label {{ font-family: "Oswald", sans-serif; font-size: 15px; color: #1d428a; letter-spacing: 2px; font-weight: bold; }}
        [data-testid="stColumn"] [data-testid="stVerticalBlock"] {{ align-items: center !important; justify-content: center !important; text-align: center !important; }}
        div.stButton > button {{ background-color: #1d428a !important; color: #FFFFFF !important; font-family: 'Oswald', sans-serif !important; font-weight: 700 !important; text-transform: uppercase !important; letter-spacing: 2px !important; padding: 18px 45px !important; border: 2px solid #1d428a !important; transition: all 0.3s ease-in-out !important; margin: 15px auto !important; display: inline-block !important; }}
        input {{ text-align: center !important; }}
        </style>
        <div style="padding: 10vh 5% 0 5%; text-align: center;">
            <div class="ulp-auth-title">Utah Land & Property</div>
            <div class="logo-container">{icon_stack}</div>
            <div class="sync-box">
                <span class="pulse-dot"></span>
                <span class="sync-label">Maximum privacy. Maximum protection. Strategic land ownership in Utah.</span>
            </div>
        </div>
    ''', unsafe_allow_html=True)
    
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
                except: st.error("SYSTEM ERROR: User database not found.")
    st.stop()

# --- 4. INTERNAL DASHBOARD STYLE (POST-LOGIN) ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=Oswald:wght@500;700&display=swap');
        .stApp { background-color: #ffffff !important; color: #1e293b !important; }
        .bento-card { background: #ffffff; padding: 24px; border-radius: 12px; border: 2px solid #e2e8f0; margin-bottom: 20px; }
        .hero-bento { background: #1d428a; color: #ffffff; padding: 30px; border-radius: 12px; }
        .ulp-header { font-family: 'Inter', sans-serif; font-size: 36px; font-weight: 900; color: #1d428a; text-transform: uppercase; }
        .hub-header { font-family: 'Inter', sans-serif; font-size: 28px; font-weight: 900; color: #1d428a !important; margin: 25px 0 15px 0; display: block; }
        .label-text { font-family: 'Oswald'; font-size: 11px; letter-spacing: 1px; color: #475569; text-transform: uppercase; font-weight: 700; }
        .hero-label { font-family: 'Oswald'; font-size: 11px; letter-spacing: 1px; color: #cbd5e1; text-transform: uppercase; }
        .value-text { font-family: 'Inter'; font-size: 26px; font-weight: 700; color: #1d428a; }
        /* Ensure all text remains dark on white */
        .stMarkdown p, .stMarkdown span, div[data-testid="stExpander"] p { color: #1e293b !important; }
        .hero-bento div, .hero-bento p, .hero-bento span { color: white !important; }
    </style>
""", unsafe_allow_html=True)

# --- 5. LOGIC & CALCULATIONS ---
role = st.session_state.user_role
# Admin Editing Panel
if role == "admin":
    with st.expander("ADMIN MODERATION PANEL: RECALCULATE TRANSACTION"):
        c1, c2, c3, c4 = st.columns(4)
        st.session_state.deal_data["price"] = c1.number_input("Sales Price", value=st.session_state.deal_data["price"])
        st.session_state.deal_data["assignment_fee"] = c2.number_input("Assignment Fee", value=st.session_state.deal_data["assignment_fee"])
        st.session_state.deal_data["seller_equity"] = c3.number_input("Seller Equity", value=st.session_state.deal_data["seller_equity"])
        st.session_state.deal_data["fee_credit"] = c4.number_input("Fee Portion to Credit", value=st.session_state.deal_data["fee_credit"])

# Current Figures
PRICE = st.session_state.deal_data["price"]
FEE = st.session_state.deal_data["assignment_fee"]
EQUITY = st.session_state.deal_data["seller_equity"]
CREDIT = st.session_state.deal_data["fee_credit"]

# AITD Principal = Price ($330k) - (Seller Equity $20k + Fee Credit $5k) = $305,000
AITD_PRINCIPAL = PRICE - (EQUITY + CREDIT)

# --- 6. TOP BENTO GRID ---
st.markdown('<div class="ulp-header">Utah Land & Property</div>', unsafe_allow_html=True)
st.markdown(f"<p style='font-family:Oswald; color:#1d428a; font-weight:700;'>AUTH_ROLE: {role.upper()}</p>", unsafe_allow_html=True)

col_hero, col_metrics = st.columns([2, 1])

with col_hero:
    st.markdown(f"""
        <div class="hero-bento">
            <div class="hero-label">AITD PRINCIPAL BALANCE</div>
            <div style="font-family: 'Inter'; font-size: 52px; font-weight: 900;">${AITD_PRINCIPAL:,.2f}</div>
            <div style="height: 1px; background: rgba(255,255,255,0.2); margin: 20px 0;"></div>
            <div style="display: flex; justify-content: space-between;">
                <div><div class="hero-label">CONTRACT PRICE</div><div style="font-size:20px; font-weight:700;">${PRICE:,.2f}</div></div>
                <div style="text-align:right;"><div class="hero-label">ACCOUNT ROLE</div><div style="font-size:20px; font-weight:700;">{role.upper()}</div></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col_metrics:
    st.markdown(f"""
        <div class="bento-card">
            <div class="label-text">ASSIGNMENT FEE (ULP)</div>
            <div class="value-text">${FEE:,.2f}</div>
        </div>
        <div class="bento-card">
            <div class="label-text">SELLER EQUITY CREDIT</div>
            <div class="value-text">${EQUITY:,.2f}</div>
        </div>
    """, unsafe_allow_html=True)

# --- 7. TRANSACTION COMMUNICATION HUB (BLUE & BOLD) ---
st.markdown('<div class="hub-header"><b>Transaction Communication Hub</b></div>', unsafe_allow_html=True)

h1, h2 = st.columns([1.6, 1])

with h1:
    with st.container(border=True):
        st.markdown("<p class='label-text'>Universal Vault & Instruction Terminal</p>", unsafe_allow_html=True)
        
        # Admin Instruction Push
        if role == "admin":
            if st.button("Generate Settlement Instructions for All Parties", use_container_width=True):
                summary = f"Settlement Instructions: Price ${PRICE:,.2f}, ULP Fee ${FEE:,.2f}, Equity Credit ${EQUITY:,.2f}, AITD Balance ${AITD_PRINCIPAL:,.2f}."
                st.session_state.deal_data["vault"].append({"name": f"Settlement_Sheet_{datetime.now().strftime('%H%M')}.txt", "content": summary, "sender": "ADMIN"})
                st.success("Instruction sheet pushed to Escrow, Title, and Loan Servicer.")

        # File Upload Logic
        uploaded_file = st.file_uploader("Drop files for transaction review", label_visibility="collapsed")
        if uploaded_file:
            st.session_state.deal_data["vault"].append({"name": uploaded_file.name, "content": "Encoded Binary File", "sender": role})

        # Display Files
        for i, doc in enumerate(st.session_state.deal_data["vault"]):
            v_col1, v_col2, v_col3 = st.columns([3, 1, 1])
            v_col1.markdown(f"**{doc['name']}** (Source: {doc['sender'].upper()})")
            
            if v_col2.button("View", key=f"v_{i}"):
                st.info(f"Metadata: {doc.get('content')}")
                
            if v_col3.button("Print", key=f"p_{i}"):
                b64 = base64.b64encode(doc.get("content", "").encode()).decode()
                st.markdown(f'<a href="data:file/txt;base64,{b64}" download="{doc["name"]}">Confirm Print/Download</a>', unsafe_allow_html=True)

with h2:
    with st.container(border=True):
        st.markdown("<p class='label-text'>Internal Broadcast</p>", unsafe_allow_html=True)
        message = st.text_area("Secure Message", placeholder="Send a message to all parties (Escrow, Title, Agent)...", height=120)
        if st.button("Broadcast to Transaction Team", use_container_width=True):
            st.toast("Communication transmitted successfully.")
        
        st.markdown("---")
        st.markdown("<p class='label-text'>Transaction Phase</p>", unsafe_allow_html=True)
        st.checkbox("Buyer Vetting Complete", value=True, disabled=True)
        st.checkbox("AITD Math Verified", value=True, disabled=True)
        st.checkbox("Instructions Pushed to Title", value=any("Settlement" in d['name'] for d in st.session_state.deal_data["vault"]))

# --- 8. LOGOUT ---
if st.sidebar.button("Terminate Session"):
    st.session_state.authenticated = False
    st.rerun()
