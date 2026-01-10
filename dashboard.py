import streamlit as st
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
        "checklist_step": 3,
        "vault": [
            {"name": "Initial_Contract.pdf", "role": "admin", "time": "2026-01-08"},
            {"name": "ULP_Assignment_Agreement.pdf", "role": "admin", "time": "2026-01-09"}
        ]
    }

if not st.session_state.authenticated:
    # [YOUR ORIGINAL AUTH LOGIC REMAINS - NO CHANGES]
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

# --- 3. DASHBOARD STYLE (BLUE/GREY ON WHITE) ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=Oswald:wght@500;700&display=swap');
        .stApp { background-color: #ffffff !important; }
        .bento-card { background: #ffffff; padding: 24px; border-radius: 12px; border: 1px solid #e2e8f0; margin-bottom: 20px; }
        .hero-bento { background: #1d428a; color: #ffffff; padding: 30px; border-radius: 12px; }
        .ulp-header { font-family: 'Inter', sans-serif; font-size: 36px !important; font-weight: 900 !important; color: #1d428a !important; letter-spacing: -1px; text-transform: uppercase; }
        .label-text { font-family: 'Oswald'; font-size: 11px; letter-spacing: 1px; color: #64748b; text-transform: uppercase; font-weight: 700; }
        .value-text { font-family: 'Inter'; font-size: 24px; font-weight: 700; color: #1e293b; }
        .role-badge { background: #f8fafc; color: #1d428a; border: 1px solid #1d428a; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 900; font-family: 'Oswald'; }
    </style>
""", unsafe_allow_html=True)

# --- 4. DATA CALCULATION ---
role = st.session_state.user_role
PRICE = st.session_state.deal_data["price"]
FEE = st.session_state.deal_data["assignment_fee"]
EQUITY = st.session_state.deal_data["seller_equity"]
AITD_BAL = PRICE - (FEE + EQUITY)

# --- 5. HEADER & ADMIN PANEL ---
st.markdown('<h1 class="ulp-header">Utah Land & Property</h1>', unsafe_allow_html=True)
st.markdown(f"<p style='font-family:Oswald; color:#1d428a; margin-top:-15px;'>ASSET TERMINAL | <span class='role-badge'>{role.upper()} ACCESS</span></p>", unsafe_allow_html=True)

if role == "admin":
    with st.expander("DEAL MODERATION & INSTRUCTION PUSH"):
        c1, c2, c3 = st.columns(3)
        st.session_state.deal_data["price"] = c1.number_input("Sales Price", value=PRICE)
        st.session_state.deal_data["assignment_fee"] = c2.number_input("Assignment Fee", value=FEE)
        st.session_state.deal_data["seller_equity"] = c3.number_input("Seller Equity", value=EQUITY)
        
        if st.button("PUSH SETTLEMENT INSTRUCTIONS TO ALL PARTIES", use_container_width=True):
            instruction_name = f"Settlement_Instructions_{datetime.now().strftime('%m%d')}.pdf"
            st.session_state.deal_data["vault"].append({"name": instruction_name, "role": "SYSTEM-PUSH", "time": datetime.now().strftime("%Y-%m-%d")})
            st.success("Instructions successfully pushed to Escrow, Title, and Loan Servicer.")

# --- 6. CORE FINANCIALS (BENTO) ---
col_main, col_stats = st.columns([2, 1])
with col_main:
    st.markdown(f"""<div class="hero-bento"><div class="label-text" style="color: #cbd5e1;">AITD PRINCIPAL BALANCE</div><div style="font-family: 'Inter'; font-size: 52px; font-weight: 900; color: white;">${AITD_BAL:,.2f}</div><div style="height: 1px; background: rgba(255,255,255,0.2); margin: 20px 0;"></div><div style="display: flex; justify-content: space-between;"><div><div class="label-text" style="color: #cbd5e1;">CONTRACT PRICE</div><div style="font-weight:700;">${PRICE:,.2f}</div></div><div style="text-align:right;"><div class="label-text" style="color: #cbd5e1;">ROLE</div><div style="font-weight:700;">{role.upper()}</div></div></div></div>""", unsafe_allow_html=True)

with col_stats:
    st.markdown(f"""<div class="bento-card"><div class="label-text">ASSIGNMENT FEE (ULP)</div><div class="value-text" style="color:#1d428a;">${FEE:,.2f}</div></div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class="bento-card"><div class="label-text">SELLER EQUITY CREDIT</div><div class="value-text">${EQUITY:,.2f}</div></div>""", unsafe_allow_html=True)

# --- 7. UNIFIED DOCUMENT VAULT & COMMUNICATION ---
st.markdown("### Transaction Communication Hub")
vault_col, task_col = st.columns([1.5, 1])

with vault_col:
    with st.container(border=True):
        st.markdown("<p class='label-text'>Unified Document Vault</p>", unsafe_allow_html=True)
        uploaded = st.file_uploader("Upload Document", label_visibility="collapsed")
        if uploaded:
            st.session_state.deal_data["vault"].append({"name": uploaded.name, "role": role, "time": datetime.now().strftime("%Y-%m-%d")})
        
        # Displaying the list of files for download (Simulated)
        for item in st.session_state.deal_data["vault"]:
            st.markdown(f"""<div style='display:flex; justify-content:space-between; padding:8px; border-bottom:1px solid #f1f5f9;'><span style='font-family:monospace; font-size:12px; color:#475569;'>{item['name']}</span><span style='font-size:10px; color:#94a3b8;'>BY: {item['role'].upper()} | {item['time']}</span></div>""", unsafe_allow_html=True)

with task_col:
    with st.container(border=True):
        st.markdown("<p class='label-text'>Phase Tracking</p>", unsafe_allow_html=True)
        is_disabled = role not in ["admin", "agent", "escrow"]
        st.checkbox("Prequal Verified", value=True, disabled=True)
        st.checkbox("Math Recalculated", value=True, disabled=True)
        st.checkbox("Instructions Pushed", value=any("Settlement_Instructions" in d['name'] for d in st.session_state.deal_data["vault"]), disabled=True)
        st.checkbox("Escrow Closing", value=st.session_state.deal_data["checklist_step"] >= 4, disabled=is_disabled)
        
        if not is_disabled and st.button("Advance Transaction", use_container_width=True):
            st.session_state.deal_data["checklist_step"] += 1
            st.rerun()

# --- 8. LOGOUT ---
if st.sidebar.button("Terminate Session"):
    st.session_state.authenticated = False
    st.rerun()
