import base64
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
import streamlit as st

# --- 1. CONFIG & REFRESH ---
st.set_page_config(page_title="Utah Land & Property", layout="wide", initial_sidebar_state="collapsed")
st_autorefresh(interval=10000, key="ulp_sync_ping")

# --- 2. DATA PERSISTENCE & MULTI-DEAL LOGIC ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_role = None

# current_deal stores the live dashboard data based on your specific sale parameters
if "current_deal" not in st.session_state:
    st.session_state.current_deal = {
        "deal_id": "DEAL-PRIMARY",
        "price": 330000.00,
        "seller_equity": 20000.00,
        "assignment_fee": 15000.00,
        "vault": [],
        "notes": []
    }

if "deal_history" not in st.session_state:
    st.session_state.deal_history = []

# --- 3. CENTERED AUTHENTICATION TERMINAL ---
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
        
        /* Center the entire block vertically */
        .main-auth-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin-top: 15vh;
            text-align: center;
        }}

        .ulp-auth-title {{ font-family: "Inter", sans-serif; font-size: clamp(32px, 8vw, 80px); font-weight: 900; color: #1d428a; letter-spacing: -4px; line-height: 1.0; margin-bottom: 10px; text-transform: uppercase; }}
        .logo-container {{ position: relative; height: 100px; width: 100%; display: flex; justify-content: center; align-items: center; margin: 20px 0; }}
        .flip-logo {{ position: absolute; opacity: 0; animation: logoFlip {len(pillar_icons)*3}s infinite; }}
        @keyframes logoFlip {{ 0% {{ opacity: 0; transform: scale(0.8); }} 1% {{ opacity: 1; transform: scale(1); }} 30% {{ opacity: 1; }} 33% {{ opacity: 0; transform: scale(1.05); }} 100% {{ opacity: 0; }} }}
        
        .sync-box {{ margin-bottom: 30px; }}
        .pulse-dot {{ height: 10px; width: 10px; background-color: #00ff41; border-radius: 50%; display: inline-block; margin-right: 8px; box-shadow: 0 0 10px #00ff41; animation: pulse-green 1.5s infinite; }}
        @keyframes pulse-green {{ 0% {{ box-shadow: 0 0 0px 0px rgba(0, 255, 65, 0.7); }} 70% {{ box-shadow: 0 0 0px 10px rgba(0, 255, 65, 0); }} 100% {{ box-shadow: 0 0 0px 0px rgba(0, 255, 65, 0); }} }}
        .sync-label {{ font-family: "Oswald", sans-serif; font-size: 14px; color: #1d428a; letter-spacing: 2px; font-weight: bold; text-transform: uppercase; }}
        
        div.stButton > button {{ background-color: #1d428a !important; color: #FFFFFF !important; font-family: 'Oswald', sans-serif !important; font-weight: 700 !important; text-transform: uppercase !important; letter-spacing: 2px !important; padding: 15px 0 !important; border: 2px solid #1d428a !important; width: 100%; transition: all 0.3s ease; margin-top: 10px; }}
        input {{ text-align: center !important; font-size: 18px !important; border-radius: 4px !important; }}
        </style>
        
        <div class="main-auth-container">
            <div class="ulp-auth-title">Utah Land & Property</div>
            <div class="logo-container">{icon_stack}</div>
            <div class="sync-box">
                <span class="pulse-dot"></span>
                <span class="sync-label">Secure Access Terminal</span>
            </div>
        </div>
    ''', unsafe_allow_html=True)
    
    _, col_mid, _ = st.columns([1.2, 1, 1.2])
    with col_mid:
        input_key = st.text_input("Security Key", type="password", placeholder="ENTER PRIVATE ACCESS KEY", label_visibility="collapsed")
        if st.button("Authorize Session"):
            try:
                user_db = st.secrets["users"]
                for username, profile in user_db.items():
                    if input_key == str(profile["key"]):
                        st.session_state.authenticated = True
                        st.session_state.user_role = profile["role"]
                        st.rerun()
                st.error("ACCESS DENIED")
            except: 
                st.error("SYSTEM ERROR: CHECK SECRETS")
    st.stop()

# --- 4. INTERNAL DASHBOARD STYLING ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=Oswald:wght@500;700&display=swap');
        .stApp { background-color: #ffffff !important; color: #1e293b !important; }
        .bento-card { background: #ffffff; padding: 24px; border-radius: 12px; border: 1px solid #e2e8f0; margin-bottom: 20px; }
        .hero-bento { background: #1d428a; color: #ffffff; padding: 30px; border-radius: 12px; }
        .ulp-header { font-family: 'Inter', sans-serif; font-size: 36px; font-weight: 900; color: #1d428a; text-transform: uppercase; }
        .hub-header { font-family: 'Inter', sans-serif; font-size: 28px; font-weight: 900; color: #1d428a !important; margin: 30px 0 15px 0; border-bottom: 4px solid #1d428a; display: inline-block; }
        .label-text { font-family: 'Oswald'; font-size: 11px; letter-spacing: 1px; color: #475569; text-transform: uppercase; font-weight: 700; }
        .hero-label { font-family: 'Oswald'; font-size: 11px; letter-spacing: 1px; color: #cbd5e1; text-transform: uppercase; }
        .value-text { font-family: 'Inter'; font-size: 26px; font-weight: 700; color: #1d428a; }
        .hero-bento * { color: white !important; }
    </style>
""", unsafe_allow_html=True)

# --- 5. ADMIN COMMAND CENTER ---
role = st.session_state.user_role
D = st.session_state.current_deal

if role == "admin":
    with st.expander("🛡️ ADMIN: DEAL MANAGEMENT TERMINAL", expanded=False):
        m1, m2, m3 = st.columns(3)
        if m1.button("➕ NEW DEAL"):
            st.session_state.deal_history.append(D.copy())
            st.session_state.current_deal = {"deal_id": f"DEAL-{datetime.now().strftime('%m%d%H%M')}", "price": 0.0, "seller_equity": 0.0, "assignment_fee": 0.0, "vault": [], "notes": []}
            st.rerun()
        if m2.button("💾 SAVE PROGRESS"):
            st.toast("Data Archived")
        if m3.button("📂 RECALL PREVIOUS"): 
            if st.session_state.deal_history:
                st.session_state.current_deal = st.session_state.deal_history[-1]
                st.rerun()
        
        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        edt_p = c1.number_input("Sales Price", value=float(D["price"]))
        edt_e = c2.number_input("Seller Equity", value=float(D["seller_equity"]))
        edt_f = c3.number_input("ULP Fee", value=float(D["assignment_fee"]))
        
        if st.button("UPDATE DASHBOARD", use_container_width=True):
            D["price"], D["seller_equity"], D["assignment_fee"] = edt_p, edt_e, edt_f
            st.rerun()

# --- 6. CORE CALCULATION & DASHBOARD ---
# Logic: $330k Price - $20k Equity = $310k AITD Principal
AITD_PRINCIPAL = D["price"] - D["seller_equity"]

st.markdown('<div class="ulp-header">Utah Land & Property</div>', unsafe_allow_html=True)
st.caption(f"SESSION: {D['deal_id']} | AUTH: {role.upper()}")

col_hero, col_side = st.columns([2, 1])
with col_hero:
    st.markdown(f"""
        <div class="hero-bento">
            <div class="hero-label">AITD PRINCIPAL BALANCE</div>
            <div style="font-family: 'Inter'; font-size: 56px; font-weight: 900;">${AITD_PRINCIPAL:,.2f}</div>
            <div style="height: 1px; background: rgba(255,255,255,0.2); margin: 25px 0;"></div>
            <div style="display: flex; justify-content: space-between;">
                <div><div class="hero-label">ORIGINAL SALES PRICE</div><div style="font-size:24px; font-weight:700;">${D['price']:,.2f}</div></div>
                <div style="text-align:right;"><div class="hero-label">SELLER EQUITY CREDIT</div><div style="font-size:24px; font-weight:700;">${D['seller_equity']:,.2f}</div></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col_side:
    st.markdown(f"""
        <div class="bento-card">
            <div class="label-text">ULP ASSIGNMENT FEE</div>
            <div class="value-text">${D['assignment_fee']:,.2f}</div>
            <p style='font-size:10px; color:#475569; margin-top:5px;'>Payable to Utah Land & Property, LLC at closing.</p>
        </div>
    """, unsafe_allow_html=True)

# --- 7. TRANSACTION HUB ---
st.markdown('<div class="hub-header">Transaction Hub</div>', unsafe_allow_html=True)
v_col, n_col = st.columns([1.5, 1])

with v_col:
    with st.container(border=True):
        st.markdown("<p class='label-text'>Settlement Vault</p>", unsafe_allow_html=True)
        if role == "admin" and st.button("📄 GENERATE MASTER SETTLEMENT SHEET", use_container_width=True):
            instr = f"ULP SETTLEMENT: {D['deal_id']}\nPrice: ${D['price']:,.2f}\nEquity to Seller: ${D['seller_equity']:,.2f}\nAITD Balance: ${AITD_PRINCIPAL:,.2f}\nULP Fee: ${D['assignment_fee']:,.2f}"
            D["vault"].append({"name": f"Settlement_{D['deal_id']}.txt", "content": instr})
            st.success("Instructions Generated")

        for doc in D["vault"]:
            v1, v2 = st.columns([4, 1])
            v1.write(f"📁 {doc['name']}")
            b64 = base64.b64encode(doc['content'].encode()).decode()
            v2.markdown(f'<a href="data:file/txt;base64,{b64}" download="{doc["name"]}" style="color:#1d428a; font-weight:bold;">PRINT</a>', unsafe_allow_html=True)

with n_col:
    with st.container(border=True):
        st.markdown("<p class='label-text'>Live Deal Notes</p>", unsafe_allow_html=True)
        new_note = st.text_input("Add update", key="note_in", label_visibility="collapsed")
        if st.button("Post") and new_note:
            D["notes"].insert(0, f"{datetime.now().strftime('%H:%M')}: {new_note}")
            st.rerun()
        for n in D["notes"]:
            st.markdown(f"<p style='font-size:12px; border-bottom:1px solid #eee;
