import base64
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
import streamlit as st

# --- 1. CONFIG & REFRESH ---
st.set_page_config(page_title="Utah Land & Property", layout="wide", initial_sidebar_state="collapsed")
st_autorefresh(interval=10000, key="ulp_sync_ping")

# --- 2. DATA PERSISTENCE & EXTENDED DEAL JACKET ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_role = None

if "current_deal" not in st.session_state:
    st.session_state.current_deal = {
        "deal_id": "DEAL-PRIMARY",
        "address": "123 Main St, Salt Lake City, UT",
        "seller_name": "John Doe",
        "buyer_name": "Jane Smith",
        "price": 330000.00,
        "seller_equity": 20000.00,
        "assignment_fee": 15000.00,
        "terms": "Subject to existing financing. AITD at 4.5% interest.",
        "vault": [],
        "notes": []
    }

# --- 3. ORIGINAL STYLE CENTERED LOGIN ---
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
        [data-testid="stAppViewBlockContainer"] {{ display: flex; flex-direction: column; justify-content: center; align-items: center; min-height: 85vh; }}
        .ulp-auth-title {{ font-family: "Inter", sans-serif; font-size: clamp(32px, 8vw, 80px); font-weight: 900; color: #1d428a; letter-spacing: -4px; line-height: 1.0; margin-bottom: 10px; text-align: center; text-transform: uppercase; }}
        .logo-container {{ position: relative; height: 120px; width: 100%; display: flex; justify-content: center; align-items: center; margin: 10px 0; }}
        .flip-logo {{ position: absolute; opacity: 0; animation: logoFlip {len(pillar_icons)*3}s infinite; }}
        @keyframes logoFlip {{ 0% {{ opacity: 0; transform: scale(0.8); }} 1% {{ opacity: 1; transform: scale(1); }} 30% {{ opacity: 1; }} 33% {{ opacity: 0; transform: scale(1.05); }} 100% {{ opacity: 0; }} }}
        .sync-label {{ font-family: "Oswald", sans-serif; font-size: 15px; color: #1d428a; letter-spacing: 2px; font-weight: bold; text-transform: uppercase; }}
        div.stButton > button {{ background-color: #1d428a !important; color: #FFFFFF !important; font-family: 'Oswald', sans-serif !important; font-weight: 700 !important; text-transform: uppercase !important; letter-spacing: 2px !important; padding: 15px 0px !important; border: 2px solid #1d428a !important; width: 100% !important; margin-top: 15px !important; }}
        input {{ text-align: center !important; font-size: 18px !important; }}
        </style>
        <div class="ulp-auth-title">Utah Land & Property</div>
        <div class="logo-container">{icon_stack}</div>
        <div style="text-align: center; margin-bottom: 25px;"><span class="sync-label">Secure Access Terminal</span></div>
    ''', unsafe_allow_html=True)
    
    _, col_mid, _ = st.columns([1, 0.7, 1])
    with col_mid:
        input_key = st.text_input("Key", type="password", placeholder="ENTER ACCESS KEY", label_visibility="collapsed")
        if st.button("Authorize Session"):
            try:
                user_db = st.secrets["users"]
                for username, profile in user_db.items():
                    if input_key == str(profile["key"]):
                        st.session_state.authenticated = True
                        st.session_state.user_role = profile["role"]
                        st.rerun()
                st.error("ACCESS DENIED")
            except: st.error("SYSTEM ERROR")
    st.stop()

# --- 4. DASHBOARD STYLING ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=Oswald:wght@500;700&display=swap');
        .stApp { background-color: #ffffff !important; }
        .bento-card { background: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #e2e8f0; margin-bottom: 15px; }
        .hero-bento { background: #1d428a; color: #ffffff; padding: 30px; border-radius: 12px; }
        .ulp-header { font-family: 'Inter', sans-serif; font-size: 36px; font-weight: 900; color: #1d428a; text-transform: uppercase; }
        .label-text { font-family: 'Oswald'; font-size: 11px; letter-spacing: 1px; color: #475569; text-transform: uppercase; font-weight: 700; }
        .value-text { font-family: 'Inter'; font-size: 22px; font-weight: 700; color: #1d428a; }
    </style>
""", unsafe_allow_html=True)

# --- 5. FULL DEAL JACKET ADMIN FORM ---
role = st.session_state.user_role
D = st.session_state.current_deal

if role == "admin":
    with st.expander("🛡️ ADMIN: FULL DEAL JACKET & PDF GENERATOR", expanded=True):
        st.markdown("#### Property & Client Information")
        f1, f2 = st.columns(2)
        new_addr = f1.text_input("Property Address", value=D["address"])
        new_deal_id = f2.text_input("Internal Deal ID", value=D["deal_id"])
        
        f3, f4 = st.columns(2)
        new_seller = f3.text_input("Seller Name(s)", value=D["seller_name"])
        new_buyer = f4.text_input("Buyer Name(s)", value=D["buyer_name"])
        
        st.markdown("#### Financial Structure")
        c1, c2, c3 = st.columns(3)
        new_price = c1.number_input("Sales Price", value=D["price"])
        new_equity = c2.number_input("Seller Equity", value=D["seller_equity"])
        new_fee = c3.number_input("ULP Fee", value=D["assignment_fee"])
        
        st.markdown("#### Deal Terms & Conditions")
        new_terms = st.text_area("Detailed Terms", value=D["terms"], height=100)
        
        if st.button("SAVE DEAL JACKET & UPDATE DASHBOARD", use_container_width=True):
            st.session_state.current_deal.update({
                "address": new_addr, "deal_id": new_deal_id, "seller_name": new_seller,
                "buyer_name": new_buyer, "price": new_price, "seller_equity": new_equity,
                "assignment_fee": new_fee, "terms": new_terms
            })
            st.rerun()

# --- 6. CORE CALCULATION & DASHBOARD ---
AITD_PRINCIPAL = D["price"] - D["seller_equity"]

st.markdown('<div class="ulp-header">Utah Land & Property</div>', unsafe_allow_html=True)
st.caption(f"ADDRESS: {D['address']} | AUTH: {role.upper()}")

col_hero, col_side = st.columns([2, 1])
with col_hero:
    st.markdown(f"""
        <div class="hero-bento">
            <div style="font-family: 'Oswald'; font-size: 11px; letter-spacing: 1px; color: #cbd5e1;">AITD PRINCIPAL BALANCE</div>
            <div style="font-family: 'Inter'; font-size: 50px; font-weight: 900; color: white;">${AITD_PRINCIPAL:,.2f}</div>
            <div style="height: 1px; background: rgba(255,255,255,0.2); margin: 20px 0;"></div>
            <div style="display: flex; justify-content: space-between; color: white;">
                <div><div class="label-text" style="color:#cbd5e1">PRICE</div><div style="font-size:20px; font-weight:700;">${D['price']:,.2f}</div></div>
                <div style="text-align:right;"><div class="label-text" style="color:#cbd5e1">EQUITY CREDIT</div><div style="font-size:20px; font-weight:700;">${D['seller_equity']:,.2f}</div></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col_side:
    st.markdown(f"""
        <div class="bento-card">
            <div class="label-text">ULP ASSIGNMENT FEE</div>
            <div class="value-text">${D['assignment_fee']:,.2f}</div>
            <div class="label-text" style="margin-top:15px">PRIMARY TERMS</div>
            <div style="font-size:12px; color:#475569;">{D['terms'][:80]}...</div>
        </div>
    """, unsafe_allow_html=True)

# --- 7. TRANSACTION HUB & PDF EXPORT ---
v_col, n_col = st.columns([1.6, 1])
with v_col:
    with st.container(border=True):
        st.markdown("<p class='label-text'>Settlement Vault</p>", unsafe_allow_html=True)
        if role == "admin":
            if st.button("📄 EXPORT OFFICIAL DEAL JACKET (TXT/PDF)", use_container_width=True):
                report = f"""
                UTAH LAND & PROPERTY - DEAL JACKET
                ----------------------------------
                DATE: {datetime.now().strftime('%Y-%m-%d')}
                ID: {D['deal_id']}
                ADDRESS: {D['address']}
                
                SELLER: {D['seller_name']}
                BUYER: {D['buyer_name']}
                
                FINANCIALS:
                - Purchase Price: ${D['price']:,.2f}
                - Seller Equity: ${D['seller_equity']:,.2f}
                - AITD Principal: ${AITD_PRINCIPAL:,.2f}
                - ULP Fee: ${D['assignment_fee']:,.2f}
                
                TERMS:
                {D['terms']}
                ----------------------------------
                """
                D["vault"].append({"name": f"Deal_Jacket_{D['deal_id']}.txt", "content": report})
                st.rerun()
        
        for doc in D["vault"]:
            v1, v2 = st.columns([4, 1])
            v1.write(f"📁 **{doc['name']}**")
            b64 = base64.b64encode(doc['content'].encode()).decode()
            v2.markdown(f'<a href="data:file/txt;base64,{b64}" download="{doc["name"]}" style="color:#1d428a; font-weight:bold;">PRINT</a>', unsafe_allow_html=True)

with n_col:
    with st.container(border=True):
        st.markdown("<p class='label-text'>Deal Notes</p>", unsafe_allow_html=True)
        new_note = st.text_input("Update", key="note_in", label_visibility="collapsed")
        if st.button("Post") and new_note:
            D["notes"].insert(0, f"{datetime.now().strftime('%H:%M')}: {new_note}")
            st.rerun()
        for n in D["notes"]:
            st.markdown(f"<p style='font-size:12px; border-bottom:1px solid #eee; padding:5px;'>{n}</p>", unsafe_allow_html=True)

if st.sidebar.button("TERMINATE SESSION"):
    st.session_state.authenticated = False
    st.rerun()
