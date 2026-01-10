import streamlit as st
import base64
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# --- 1. SYSTEM CONFIGURATION & SYNC ---
st.set_page_config(page_title="Utah Land & Property", layout="wide", initial_sidebar_state="collapsed")
st_autorefresh(interval=10000, key="ulp_sync_ping")

# --- 2. DATA PERSISTENCE LAYER ---
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

if "deal_history" not in st.session_state:
    st.session_state.deal_history = []

# --- 3. ORIGINAL ALIGNED PILLAR LOGIN (RESTORED BLUE & CENTERED) ---
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
        
        div.stButton > button {{ 
            background-color: #1d428a !important; 
            color: #FFFFFF !important; 
            font-family: 'Oswald', sans-serif !important; 
            font-weight: 700 !important; 
            text-transform: uppercase !important; 
            letter-spacing: 2px !important; 
            padding: 18px 45px !important; 
            border: 2px solid #1d428a !important; 
            width: 100% !important; 
            margin-top: 20px !important;
        }}
        input {{ text-align: center !important; font-size: 20px !important; border: 2px solid #1d428a !important; color: #1d428a !important; }}
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
    
    _, col_mid, _ = st.columns([1, 1.5, 1])
    with col_mid:
        with st.form("secure_login_form", clear_on_submit=False):
            input_key = st.text_input("Security Key", type="password", placeholder="ENTER PRIVATE ACCESS KEY", label_visibility="collapsed")
            submit = st.form_submit_button("Secure Access Terminal")
            if submit:
                try:
                    user_db = st.secrets["users"]
                    found_user = None
                    for username, profile in user_db.items():
                        if input_key == str(profile["key"]):
                            found_user = profile
                            break
                    if found_user:
                        st.session_state.authenticated = True
                        st.session_state.user_role = found_user["role"]
                        st.rerun()
                    else:
                        st.error("ACCESS DENIED: INVALID KEY")
                except: 
                    st.error("SYSTEM ERROR: DATABASE NOT FOUND")
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

# --- 5. ACTIVE ADMIN DEAL MANAGEMENT TERMINAL ---
role = st.session_state.user_role
D = st.session_state.current_deal

if role == "admin":
    with st.expander("ADMIN: UTAH LAND & PROPERTY DEAL MANAGEMENT", expanded=True):
        m1, m2, m3 = st.columns(3)
        if m1.button("CREATE NEW DEAL SESSION"):
            st.session_state.deal_history.append(D.copy())
            st.session_state.current_deal = {
                "deal_id": f"DEAL-{datetime.now().strftime('%m%d%H%M')}",
                "price": 330000.0, "seller_equity": 20000.0, "assignment_fee": 15000.0, 
                "vault": [], "notes": []
            }
            st.rerun()
            
        if m2.button("SAVE ACTIVE SESSION"):
            st.toast("Current session data cached in history.")
            
        if m3.button("RECALL LAST SESSION"): 
            if st.session_state.deal_history:
                st.session_state.current_deal = st.session_state.deal_history[-1]
                st.rerun()
        
        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        D["price"] = c1.number_input("Contract Sales Price", value=float(D["price"]))
        D["seller_equity"] = c2.number_input("Seller Equity Reduction", value=float(D["seller_equity"]))
        D["assignment_fee"] = c3.number_input("Utah Land & Property Assignment Fee", value=float(D["assignment_fee"]))
        
        if st.button("PUSH DATA TO ALL USERS", use_container_width=True):
            st.rerun()

# --- 6. CORE MATH & DASHBOARD ---
AITD_PRINCIPAL = D["price"] - D["seller_equity"]

st.markdown('<div class="ulp-header">Utah Land & Property</div>', unsafe_allow_html=True)
st.markdown(f"**SESSION ID:** {D['deal_id']} | **ROLE:** {role.upper()}")

col_hero, col_side = st.columns([2, 1])
with col_hero:
    st.markdown(f"""
        <div class="hero-bento">
            <div class="hero-label">AITD PRINCIPAL BALANCE</div>
            <div style="font-family: 'Inter'; font-size: 56px; font-weight: 900;">${AITD_PRINCIPAL:,.2f}</div>
            <div style="height: 1px; background: rgba(255,255,255,0.2); margin: 25px 0;"></div>
            <div style="display: flex; justify-content: space-between;">
                <div><div class="hero-label">CONTRACT SALES PRICE</div><div style="font-size:24px; font-weight:700;">${D['price']:,.2f}</div></div>
                <div style="text-align:right;"><div class="hero-label">SELLER EQUITY REDUCTION</div><div style="font-size:24px; font-weight:700;">${D['seller_equity']:,.2f}</div></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col_side:
    st.markdown(f"""
        <div class="bento-card">
            <div class="label-text">UTAH LAND & PROPERTY ASSIGNMENT FEE</div>
            <div class="value-text">${D['assignment_fee']:,.2f}</div>
            <p style='font-size:10px; color:#475569; margin-top:5px;'>Service fee paid to Utah Land & Property; does not affect principal.</p>
        </div>
    """, unsafe_allow_html=True)

# --- 7. TRANSACTION HUB & PRINTABLE DOCUMENTATION ---
st.markdown('<div class="hub-header">Transaction Communication Hub</div>', unsafe_allow_html=True)
v_col, n_col = st.columns([1.6, 1])

with v_col:
    with st.container(border=True):
        st.markdown("<p class='label-text'>Universal Vault & Settlement Exports</p>", unsafe_allow_html=True)
        
        if role == "admin":
            if st.button("GENERATE MASTER SETTLEMENT SHEET", use_container_width=True):
                instr = (
                    f"UTAH LAND & PROPERTY - OFFICIAL SETTLEMENT INSTRUCTIONS\n"
                    f"Deal ID: {D['deal_id']} | Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
                    f"--------------------------------------------------\n"
                    f"CONTRACT SALES PRICE:  ${D['price']:,.2f}\n"
                    f"SELLER EQUITY:        -${D['seller_equity']:,.2f}\n"
                    f"AITD PRINCIPAL:       ${AITD_PRINCIPAL:,.2f}\n"
                    f"--------------------------------------------------\n"
                    f"UTAH LAND & PROPERTY ASSIGNMENT FEE: ${D['assignment_fee']:,.2f}\n"
                    f"--------------------------------------------------\n"
                    f"Instructions: Pay ${D['seller_equity']:,.2f} to Seller. Pay ${D['assignment_fee']:,.2f} to Utah Land & Property, LLC."
                )
                D["vault"].append({"name": f"Settlement_{D['deal_id']}.txt", "content": instr})
                st.success("Instructions generated and pushed to vault.")

        for i, doc in enumerate(D["vault"]):
            v1, v2 = st.columns([4, 1.5])
            v1.write(f"FILE: {doc['name']}")
            b64 = base64.b64encode(doc['content'].encode()).decode()
            v2.markdown(f'<a href="data:file/txt;base64,{b64}" download="{doc["name"]}" style="text-decoration:none; padding:8px 12px; background:#1d428a; color:white; border-radius:5px; font-weight:bold; font-size:11px; text-transform:uppercase;">Download / Print</a>', unsafe_allow_html=True)

with n_col:
    with st.container(border=True):
        st.markdown("<p class='label-text'>Live Deal Notes</p>", unsafe_allow_html=True)
        new_note = st.text_input("Enter update", key="note_in", label_visibility="collapsed")
        if st.button("Post Note") and new_note:
            D["notes"].insert(0, f"{datetime.now().strftime('%H:%M')} ({role.upper()}): {new_note}")
            st.rerun()
        for n in D["notes"]:
            st.markdown(f"<p style='font-size:12px; border-bottom:1px solid #eee; padding:5px;'>{n}</p>", unsafe_allow_html=True)

if st.sidebar.button("TERMINATE SECURE SESSION"):
    st.session_state.authenticated = False
    st.rerun()
