import streamlit as st
import base64
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# --- 1. SYSTEM CONFIGURATION ---
st.set_page_config(page_title="Utah Land & Property", layout="wide", initial_sidebar_state="collapsed")
st_autorefresh(interval=10000, key="ulp_sync_ping")

# --- 2. DATA PERSISTENCE (ROBUST ADMIN LOGIC) ---
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

# --- 3. THE ABSOLUTE CENTERED LOGIN (ZERO-COLUMN CSS) ---
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
        
        /* FORCE VERTICAL SPINE ALIGNMENT */
        .main-login-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 100%;
            text-align: center;
            padding-top: 10vh;
        }}

        .ulp-auth-title {{ 
            font-family: "Inter", sans-serif; 
            font-size: clamp(32px, 12vw, 80px); 
            font-weight: 900; 
            color: #1d428a; 
            letter-spacing: -4px; 
            text-transform: uppercase; 
            margin-bottom: 20px;
        }}
        
        .logo-container {{ position: relative; height: 120px; width: 100%; display: flex; justify-content: center; align-items: center; margin-bottom: 20px; }}
        .flip-logo {{ position: absolute; opacity: 0; animation: logoFlip {len(pillar_icons)*3}s infinite; }}
        @keyframes logoFlip {{ 0% {{ opacity: 0; }} 1% {{ opacity: 1; }} 30% {{ opacity: 1; }} 33% {{ opacity: 0; }} 100% {{ opacity: 0; }} }}
        
        .sync-label {{ font-family: "Oswald", sans-serif; font-size: 14px; color: #1d428a; letter-spacing: 2px; font-weight: bold; margin-bottom: 40px; }}

        /* TARGETING STREAMLIT WIDGETS DIRECTLY FOR ALIGNMENT */
        .stTextInput, .stButton {{
            width: 400px !important;
            margin: 0 auto !important;
        }}

        div.stButton > button {{ 
            background-color: #1d428a !important; 
            color: #FFFFFF !important; 
            font-family: 'Oswald', sans-serif !important; 
            font-weight: 700 !important; 
            text-transform: uppercase !important; 
            letter-spacing: 2px !important; 
            padding: 18px 0px !important; 
            border: 2px solid #1d428a !important; 
            width: 100% !important;
            border-radius: 0px !important;
            margin-top: 10px !important;
        }}
        
        input {{ 
            text-align: center !important; 
            font-size: 18px !important; 
            border: 2px solid #1d428a !important; 
            border-radius: 0px !important;
            height: 50px !important;
            color: #1d428a !important;
        }}
        </style>
        
        <div class="main-login-container">
            <div class="ulp-auth-title">Utah Land & Property</div>
            <div class="logo-container">{icon_stack}</div>
            <div class="sync-label">Maximum privacy. Maximum protection. Strategic land ownership in Utah.</div>
        </div>
    ''', unsafe_allow_html=True)
    
    # Simple block-level alignment
    input_key = st.text_input("Security Key", type="password", placeholder="ENTER PRIVATE ACCESS KEY", label_visibility="collapsed")
    if st.button("Secure Access Terminal"):
        try:
            user_db = st.secrets["users"]
            for username, profile in user_db.items():
                if input_key == str(profile["key"]):
                    st.session_state.authenticated = True
                    st.session_state.user_role = profile["role"]
                    st.rerun()
            st.error("ACCESS DENIED")
        except:
            st.error("SYSTEM ERROR: NO USER DATABASE FOUND")
    st.stop()

# --- 4. INTERNAL DASHBOARD STYLING (EMOJI-FREE) ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=Oswald:wght@500;700&display=swap');
        .stApp { background-color: #ffffff !important; }
        .bento-card { background: #ffffff; padding: 24px; border-radius: 12px; border: 1px solid #e2e8f0; margin-bottom: 20px; }
        .hero-bento { background: #1d428a; color: #ffffff; padding: 30px; border-radius: 12px; }
        .ulp-header { font-family: 'Inter', sans-serif; font-size: 36px; font-weight: 900; color: #1d428a; text-transform: uppercase; }
        .hub-header { font-family: 'Inter', sans-serif; font-size: 28px; font-weight: 900; color: #1d428a !important; margin: 30px 0 15px 0; border-bottom: 4px solid #1d428a; display: inline-block; }
        .label-text { font-family: 'Oswald'; font-size: 11px; letter-spacing: 1px; color: #475569; text-transform: uppercase; font-weight: 700; }
        .hero-label { font-family: 'Oswald'; font-size: 11px; letter-spacing: 1px; color: #cbd5e1; text-transform: uppercase; }
        .value-text { font-family: 'Inter'; font-size: 26px; font-weight: 700; color: #1d428a; }
    </style>
""", unsafe_allow_html=True)

# --- 5. FUNCTIONAL ADMIN TERMINAL (EDIT & CREATE DEALS) ---
role = st.session_state.user_role
D = st.session_state.current_deal

if role == "admin":
    with st.expander("ADMIN: UTAH LAND & PROPERTY DEAL MANAGEMENT", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        # Action: Create New Deal
        if col1.button("CREATE NEW DEAL SESSION"):
            st.session_state.deal_history.append(D.copy())
            st.session_state.current_deal = {
                "deal_id": f"DEAL-{datetime.now().strftime('%m%d%H%M')}",
                "price": 330000.0,
                "seller_equity": 20000.0,
                "assignment_fee": 15000.0,
                "vault": [],
                "notes": []
            }
            st.rerun()

        # Action: Generate Settlement PDF (Text-based Export)
        if col2.button("GENERATE SETTLEMENT SHEET"):
            AITD_VAL = D['price'] - D['seller_equity']
            sheet_content = (
                f"OFFICIAL SETTLEMENT SHEET - UTAH LAND & PROPERTY\n"
                f"Date: {datetime.now().strftime('%Y-%m-%d')}\n"
                f"Deal ID: {D['deal_id']}\n"
                f"------------------------------------------------\n"
                f"Contract Sales Price: ${D['price']:,.2f}\n"
                f"Seller Equity Credit: ${D['seller_equity']:,.2f}\n"
                f"AITD Principal Balance: ${AITD_VAL:,.2f}\n"
                f"------------------------------------------------\n"
                f"Assignment Fee (Utah Land & Property): ${D['assignment_fee']:,.2f}\n"
            )
            D["vault"].append({"name": f"Settlement_{D['deal_id']}.txt", "content": sheet_content})
            st.success("Sheet generated in Vault below.")

        if col3.button("SAVE CHANGES"):
            st.rerun()
        
        st.markdown("---")
        # Direct Value Editing
        ec1, ec2, ec3 = st.columns(3)
        D["price"] = ec1.number_input("Purchase Price", value=float(D["price"]))
        D["seller_equity"] = ec2.number_input("Seller Equity Credit", value=float(D["seller_equity"]))
        D["assignment_fee"] = ec3.number_input("Utah Land & Property Fee", value=float(D["assignment_fee"]))

# --- 6. LIVE CALCULATIONS & DASHBOARD ---
AITD_PRINCIPAL = D["price"] - D["seller_equity"]

st.markdown('<div class="ulp-header">Utah Land & Property</div>', unsafe_allow_html=True)
st.markdown(f"**SESSION:** {D['deal_id']} | **ROLE:** {role.upper()}")

col_hero, col_side = st.columns([2, 1])
with col_hero:
    st.markdown(f"""
        <div class="hero-bento">
            <div class="hero-label">AITD PRINCIPAL BALANCE</div>
            <div style="font-family: 'Inter'; font-size: 56px; font-weight: 900; color: white;">${AITD_PRINCIPAL:,.2f}</div>
            <div style="height: 1px; background: rgba(255,255,255,0.2); margin: 25px 0;"></div>
            <div style="display: flex; justify-content: space-between;">
                <div><div class="hero-label">SALES PRICE</div><div style="font-size:24px; font-weight:700; color: white;">${D['price']:,.2f}</div></div>
                <div style="text-align:right;"><div class="hero-label">SELLER EQUITY</div><div style="font-size:24px; font-weight:700; color: white;">${D['seller_equity']:,.2f}</div></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col_side:
    st.markdown(f"""
        <div class="bento-card">
            <div class="label-text">ASSIGNMENT FEE</div>
            <div class="value-text" style="color:#1d428a;">${D['assignment_fee']:,.2f}</div>
            <p style='font-size:10px; color:#475569; margin-top:5px;'>Payable to: Utah Land & Property, LLC</p>
        </div>
    """, unsafe_allow_html=True)

# --- 7. VAULT & HUB ---
st.markdown('<div class="hub-header">Transaction Hub</div>', unsafe_allow_html=True)
v_col, n_col = st.columns([1.6, 1])

with v_col:
    with st.container(border=True):
        st.markdown("<p class='label-text'>Universal Vault (Printable Docs)</p>", unsafe_allow_html=True)
        for doc in D["vault"]:
            v1, v2 = st.columns([4, 1.5])
            v1.write(f"DOCUMENT: {doc['name']}")
            b64 = base64.b64encode(doc['content'].encode()).decode()
            v2.markdown(f'<a href="data:file/txt;base64,{b64}" download="{doc["name"]}" style="text-decoration:none; padding:8px 12px; background:#1d428a; color:white; border-radius:5px; font-weight:bold; font-size:11px; text-transform:uppercase;">Download / Print</a>', unsafe_allow_html=True)

with n_col:
    with st.container(border=True):
        st.markdown("<p class='label-text'>Live Update Notes</p>", unsafe_allow_html=True)
        new_note = st.text_input("Add Update", key="note_in")
        if st.button("Commit") and new_note:
            D["notes"].insert(0, f"{datetime.now().strftime('%H:%M')} ({role.upper()}): {new_note}")
            st.rerun()
        for n in D["notes"]:
            st.markdown(f"<p style='font-size:12px; border-bottom:1px solid #eee; padding:5px;'>{n}</p>", unsafe_allow_html=True)

if st.sidebar.button("LOGOUT"):
    st.session_state.authenticated = False
    st.rerun()
