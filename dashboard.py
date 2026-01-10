import base64
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
import streamlit as st

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
        "address": "123 Main St, Salt Lake City",
        "seller_name": "John Doe",
        "buyer_name": "Jane Smith",
        "price": 330000.00,
        "seller_equity": 20000.00,
        "assignment_fee": 15000.00,
        "terms": "Subject to existing financing. AITD terms applied.",
        "vault": [],
        "notes": []
    }

# --- 3. THE CENTERED CONFORMITY LOGIN ---
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
        
        [data-testid="stAppViewBlockContainer"] {{ 
            display: flex; flex-direction: column; justify-content: center; align-items: center; min-height: 85vh; 
        }}

        .ulp-auth-title {{ font-family: "Inter", sans-serif; font-size: clamp(32px, 8vw, 80px); font-weight: 900; color: #1d428a; letter-spacing: -4px; line-height: 1.0; margin-bottom: 10px; text-align: center; text-transform: uppercase; }}
        .logo-container {{ position: relative; height: 120px; width: 100%; display: flex; justify-content: center; align-items: center; margin: 10px 0; }}
        .flip-logo {{ position: absolute; opacity: 0; animation: logoFlip {len(pillar_icons)*3}s infinite; }}
        @keyframes logoFlip {{ 0% {{ opacity: 0; transform: scale(0.8); }} 1% {{ opacity: 1; transform: scale(1); }} 30% {{ opacity: 1; }} 33% {{ opacity: 0; transform: scale(1.05); }} 100% {{ opacity: 0; }} }}
        .sync-label {{ font-family: "Oswald", sans-serif; font-size: 15px; color: #1d428a; letter-spacing: 2px; font-weight: bold; text-transform: uppercase; }}
        
        /* Conformity: Matching Button and Input exactly */
        div.stButton > button {{ 
            background-color: #1d428a !important; color: #FFFFFF !important; font-family: 'Oswald', sans-serif !important; 
            font-weight: 700 !important; text-transform: uppercase !important; letter-spacing: 2px !important; 
            padding: 0px !important; border: 2px solid #1d428a !important; width: 100% !important; margin-top: 10px !important; 
            height: 52px !important; border-radius: 4px !important;
        }}
        [data-testid="stTextInput"] {{ width: 100% !important; }}
        input {{ 
            text-align: center !important; font-size: 18px !important; color: #1d428a !important; 
            border: 2px solid #e2e8f0 !important; border-radius: 4px !important; height: 52px !important;
        }}
        </style>
        <div class="ulp-auth-title">Utah Land & Property</div>
        <div class="logo-container">{icon_stack}</div>
        <div style="text-align: center; margin-bottom: 25px;"><span class="sync-label">Secure Access Terminal</span></div>
    ''', unsafe_allow_html=True)
    
    _, col_mid, _ = st.columns([1, 0.6, 1]) 
    with col_mid:
        input_key = st.text_input("Key", type="password", placeholder="ENTER ACCESS KEY", label_visibility="collapsed")
        if st.button("Authorize Session"):
            try:
                user_db = st.secrets["users"]
                for username, profile in user_db.items():
                    if input_key == str(profile["key"]):
                        st.session_state.authenticated = True
                        st.session_state.user_role = str(profile["role"]).lower() 
                        st.rerun()
                st.error("ACCESS DENIED")
            except: st.error("CRITICAL: Secrets Config Error")
    st.stop()

# --- 4. DASHBOARD STYLING ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=Oswald:wght@500;700&display=swap');
        .stApp { background-color: #ffffff !important; }
        .admin-terminal { background: #1d428a; border: 3px solid #0e2145; padding: 25px; border-radius: 12px; margin-bottom: 30px; color: white !important; }
        .admin-terminal h3 { color: white !important; font-weight: 900 !important; font-family: 'Inter', sans-serif; text-transform: uppercase; }
        .admin-terminal label { color: white !important; font-family: 'Oswald' !important; font-weight: 700 !important; text-transform: uppercase !important; font-size: 12px !important; }
        .hero-bento { background: #1d428a; color: #ffffff; padding: 30px; border-radius: 12px; }
        .ulp-header { font-family: 'Inter', sans-serif; font-size: 36px; font-weight: 900; color: #1d428a; text-transform: uppercase; }
        .label-text { font-family: 'Oswald'; font-size: 11px; letter-spacing: 1px; color: #475569; text-transform: uppercase; font-weight: 700; }
        .vault-link { color: #1d428a !important; font-weight: 900 !important; text-decoration: underline !important; font-family: 'Oswald', sans-serif; }
    </style>
""", unsafe_allow_html=True)

# --- 5. ADMIN COMMAND CENTER ---
role = st.session_state.user_role
D = st.session_state.current_deal

if role == "admin":
    st.markdown('<div class="admin-terminal">', unsafe_allow_html=True)
    st.markdown("### 🛡️ ADMIN: STRATEGIC DEAL JACKET")
    
    # Ensuring inputs use session state directly to force updates
    r1c1, r1c2 = st.columns(2)
    new_addr = r1c1.text_input("Property Address", value=D["address"])
    new_id = r1c2.text_input("Deal ID", value=D["deal_id"])
    
    r2c1, r2c2 = st.columns(2)
    new_seller = r2c1.text_input("Seller Name", value=D["seller_name"])
    new_buyer = r2c2.text_input("Buyer Name", value=D["buyer_name"])
    
    r3c1, r3c2, r3c3 = st.columns(3)
    new_price = r3c1.number_input("Sales Price", value=float(D["price"]))
    new_equity = r3c2.number_input("Seller Equity", value=float(D["seller_equity"]))
    new_fee = r3c3.number_input("Assignment Fee", value=float(D["assignment_fee"]))
    
    new_terms = st.text_area("Detailed Deal Terms", value=D["terms"])
    
    if st.button("🚀 UPDATE MASTER DASHBOARD", use_container_width=True):
        st.session_state.current_deal["address"] = new_addr
        st.session_state.current_deal["deal_id"] = new_id
        st.session_state.current_deal["seller_name"] = new_seller
        st.session_state.current_deal["buyer_name"] = new_buyer
        st.session_state.current_deal["price"] = new_price
        st.session_state.current_deal["seller_equity"] = new_equity
        st.session_state.current_deal["assignment_fee"] = new_fee
        st.session_state.current_deal["terms"] = new_terms
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- 6. LIVE DASHBOARD ---
AITD_PRINCIPAL = D["price"] - D["seller_equity"]
st.markdown('<div class="ulp-header">Utah Land & Property</div>', unsafe_allow_html=True)
st.caption(f"PROPERTY: {D['address']} | ID: {D['deal_id']} | AUTH: {role.upper()}")

c_hero, c_side = st.columns([2, 1])
with c_hero:
    st.markdown(f"""
        <div class="hero-bento">
            <div class="label-text" style="color: #cbd5e1;">AITD PRINCIPAL BALANCE</div>
            <div style="font-family: 'Inter'; font-size: 50px; font-weight: 900; color: white;">${AITD_PRINCIPAL:,.2f}</div>
            <div style="height: 1px; background: rgba(255,255,255,0.2); margin: 20px 0;"></div>
            <div style="display: flex; justify-content: space-between; color: white;">
                <div><div class="label-text" style="color:#cbd5e1">CONTRACT PRICE</div><div style="font-size:20px; font-weight:700;">${D['price']:,.2f}</div></div>
                <div style="text-align:right;"><div class="label-text" style="color:#cbd5e1">SELLER EQUITY</div><div style="font-size:20px; font-weight:700;">${D['seller_equity']:,.2f}</div></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with c_side:
    st.markdown(f"""
        <div style="background:white; padding:20px; border:1px solid #e2e8f0; border-radius:12px; height: 100%;">
            <div class="label-text">ULP ASSIGNMENT FEE</div>
            <div style="font-family:'Inter'; font-size:22px; font-weight:700; color:#1d428a;">${D['assignment_fee']:,.2f}</div>
            <div class="label-text" style="margin-top:15px">PRIMARY TERMS</div>
            <div style="font-size:12px; color:#475569;">{D['terms']}</div>
        </div>
    """, unsafe_allow_html=True)

# --- 7. TRANSACTION VAULT ---
v_col, n_col = st.columns([1.6, 1])
with v_col:
    with st.container(border=True):
        st.markdown("<p class='label-text'>Settlement Vault</p>", unsafe_allow_html=True)
        if role == "admin":
            if st.button("📄 GENERATE MASTER DEAL SHEET", use_container_width=True):
                # Full data entry into the TXT file
                report = f"""UTAH LAND & PROPERTY - OFFICIAL DEAL SHEET
--------------------------------------------------
DATE: {datetime.now().strftime('%Y-%m-%d %H:%M')}
DEAL ID: {D['deal_id']}
ADDRESS: {D['address']}

PARTIES:
SELLER: {D['seller_name']}
BUYER: {D['buyer_name']}

FINANCIAL STRUCTURE:
CONTRACT PRICE: ${D['price']:,.2f}
SELLER EQUITY:  ${D['seller_equity']:,.2f}
AITD PRINCIPAL: ${AITD_PRINCIPAL:,.2f}
ULP ASSIGN_FEE: ${D['assignment_fee']:,.2f}

STRATEGIC TERMS:
{D['terms']}
--------------------------------------------------
DOCUMENT GENERATED VIA SECURE TERMINAL"""
                D["vault"].append({"name": f"Deal_{D['deal_id']}.txt", "content": report})
                st.rerun()
        
        for doc in D["vault"]:
            v1, v2 = st.columns([4, 1.5])
            v1.markdown(f"📁 <span style='color:#1d428a; font-weight:bold;'>{doc['name']}</span>", unsafe_allow_html=True)
            b64 = base64.b64encode(doc['content'].encode()).decode()
            # Professional Blue Print Link
            v2.markdown(f'<a href="data:file/txt;base64,{b64}" download="{doc["name"]}" class="vault-link">PRINT/DOWNLOAD</a>', unsafe_allow_html=True)

with n_col:
    with st.container(border=True):
        st.markdown("<p class='label-text'>Live Deal Notes</p>", unsafe_allow_html=True)
        new_note = st.text_input("Log Entry", key="note_in", label_visibility="collapsed")
        if st.button("Commit Note") and new_note:
            D["notes"].insert(0, f"{datetime.now().strftime('%H:%M')}: {new_note}")
            st.rerun()
        for n in D["notes"]:
            st.markdown(f"<p style='font-size:12px; border-bottom:1px solid #eee; padding:5px; color:#1d428a;'>{n}</p>", unsafe_allow_html=True)

if st.sidebar.button("TERMINATE SESSION"):
    st.session_state.authenticated = False
    st.rerun()
