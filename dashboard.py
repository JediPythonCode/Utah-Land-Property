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

# Default data structure
if "current_deal" not in st.session_state:
    st.session_state.current_deal = {
        "deal_id": "DEAL-PRIMARY",
        "address": "Enter Property Address",
        "seller_name": "",
        "buyer_name": "",
        "price": 330000.00,
        "seller_equity": 20000.00,
        "assignment_fee": 15000.00,
        "terms": "Enter deal terms here...",
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
        
        [data-testid="stAppViewBlockContainer"] {{ 
            display: flex; 
            flex-direction: column; 
            justify-content: center; 
            align-items: center; 
            min-height: 85vh; 
        }}

        .ulp-auth-title {{ font-family: "Inter", sans-serif; font-size: clamp(32px, 8vw, 80px); font-weight: 900; color: #1d428a; letter-spacing: -4px; line-height: 1.0; margin-bottom: 10px; text-align: center; text-transform: uppercase; }}
        .logo-container {{ position: relative; height: 120px; width: 100%; display: flex; justify-content: center; align-items: center; margin: 10px 0; }}
        .flip-logo {{ position: absolute; opacity: 0; animation: logoFlip {len(pillar_icons)*3}s infinite; }}
        @keyframes logoFlip {{ 0% {{ opacity: 0; transform: scale(0.8); }} 1% {{ opacity: 1; transform: scale(1); }} 30% {{ opacity: 1; }} 33% {{ opacity: 0; transform: scale(1.05); }} 100% {{ opacity: 0; }} }}
        
        .sync-label {{ font-family: "Oswald", sans-serif; font-size: 15px; color: #1d428a; letter-spacing: 2px; font-weight: bold; text-transform: uppercase; }}
        
        div.stButton > button {{ 
            background-color: #1d428a !important; 
            color: #FFFFFF !important; 
            font-family: 'Oswald', sans-serif !important; 
            font-weight: 700 !important; 
            text-transform: uppercase !important; 
            letter-spacing: 2px !important; 
            padding: 15px 0px !important; 
            border: 2px solid #1d428a !important; 
            width: 100% !important; 
            margin-top: 15px !important; 
        }}
        [data-testid="stTextInput"] {{ width: 100% !important; }}
        input {{ text-align: center !important; font-size: 18px !important; }}
        </style>
        
        <div class="ulp-auth-title">Utah Land & Property</div>
        <div class="logo-container">{icon_stack}</div>
        <div style="text-align: center; margin-bottom: 25px;"><span class="sync-label">Secure Access Terminal</span></div>
    ''', unsafe_allow_html=True)
    
    # Perfect centering for the input and button stack
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
            except: st.error("SYSTEM ERROR: Check Secrets Configuration")
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
    with st.expander("🛡️ ADMIN: FULL DEAL JACKET & FINANCIAL OVERRIDE", expanded=True):
        st.markdown("#### 1. Property & Client Details")
        f1, f2 = st.columns(2)
        # Using .get() for safety against KeyErrors
        new_addr = f1.text_input("Property Address", value=D.get("address", ""))
        new_deal_id = f2.text_input("Internal Deal ID", value=D.get("deal_id", "DEAL-PRIMARY"))
        
        f3, f4 = st.columns(2)
        new_seller = f3.text_input("Seller Name(s)", value=D.get("seller_name", ""))
        new_buyer = f4.text_input("Buyer Name(s)", value=D.get("buyer_name", ""))
        
        st.markdown("#### 2. Financial Structure")
        c1, c2, c3 = st.columns(3)
        new_price = c1.number_input("Contract Sales Price", value=float(D.get("price", 0.0)))
        new_equity = c2.number_input("Seller Equity Credit", value=float(D.get("seller_equity", 0.0)))
        new_fee = c3.number_input("ULP Assignment Fee", value=float(D.get("assignment_fee", 0.0)))
        
        st.markdown("#### 3. Strategic Terms")
        new_terms = st.text_area("Detailed Deal Terms", value=D.get("terms", ""), height=100)
        
        if st.button("PUSH FULL JACKET TO DASHBOARD", use_container_width=True):
            st.session_state.current_deal.update({
                "address": new_addr, "deal_id": new_deal_id, "seller_name": new_seller,
                "buyer_name": new_buyer, "price": new_price, "seller_equity": new_equity,
                "assignment_fee": new_fee, "terms": new_terms
            })
            st.rerun()

# --- 6. DASHBOARD RENDERING ---
# AITD Principal: Price minus Equity
AITD_PRINCIPAL = D.get("price", 0.0) - D.get("seller_equity", 0.0)

st.markdown('<div class="ulp-header">Utah Land & Property</div>', unsafe_allow_html=True)
st.caption(f"ADDRESS: {D.get('address', 'PENDING')} | ID: {D.get('deal_id', 'PRIMARY')} | AUTH: {role.upper()}")

col_hero, col_side = st.columns([2, 1])
with col_hero:
    st.markdown(f"""
        <div class="hero-bento">
            <div style="font-family: 'Oswald'; font-size: 11px; letter-spacing: 1px; color: #cbd5e1;">AITD PRINCIPAL BALANCE</div>
            <div style="font-family: 'Inter'; font-size: 50px; font-weight: 900; color: white;">${AITD_PRINCIPAL:,.2f}</div>
            <div style="height: 1px; background: rgba(255,255,255,0.2); margin: 20px 0;"></div>
            <div style="display: flex; justify-content: space-between; color: white;">
                <div><div class="label-text" style="color:#cbd5e1">SALES PRICE</div><div style="font-size:20px; font-weight:700;">${D.get('price', 0.0):,.2f}</div></div>
                <div style="text-align:right;"><div class="label-text" style="color:#cbd5e1">SELLER EQUITY</div><div style="font-size:20px; font-weight:700;">${D.get('seller_equity', 0.0):,.2f}</div></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col_side:
    st.markdown(f"""
        <div class="bento-card">
            <div class="label-text">ULP ASSIGNMENT FEE</div>
            <div class="value-text">${D.get('assignment_fee', 0.0):,.2f}</div>
            <div class="label-text" style="margin-top:15px">KEY TERMS</div>
            <div style="font-size:12px; color:#475569;">{D.get('terms', '')[:100]}...</div>
        </div>
    """, unsafe_allow_html=True)

# --- 7. TRANSACTION HUB ---
v_col, n_col = st.columns([1.6, 1])
with v_col:
    with st.container(border=True):
        st.markdown("<p class='label-text'>Settlement Vault</p>", unsafe_allow_html=True)
        if role == "admin":
            if st.button("📄 GENERATE MASTER SETTLEMENT SHEET", use_container_width=True):
                report = f"PROPERTY: {D.get('address')}\nPRICE: ${D.get('price'):,.2f}\nAITD: ${AITD_PRINCIPAL:,.2f}\nBUYER: {D.get('buyer_name')}"
                D["vault"].append({"name": f"Settlement_{datetime.now().strftime('%m%d')}.txt", "content": report})
                st.rerun()
        
        for doc in D.get("vault", []):
            v1, v2 = st.columns([4, 1])
            v1.write(f"📁 **{doc['name']}**")
            b64 = base64.b64encode(doc['content'].encode()).decode()
            v2.markdown(f'<a href="data:file/txt;base64,{b64}" download="{doc["name"]}" style="color:#1d428a; font-weight:bold;">PRINT</a>', unsafe_allow_html=True)

with n_col:
    with st.container(border=True):
        st.markdown("<p class='label-text'>Live Deal Notes</p>", unsafe_allow_html=True)
        new_note = st.text_input("Post Update", key="note_in", label_visibility="collapsed")
        if st.button("Post") and new_note:
            D["notes"].insert(0, f"{datetime.now().strftime('%H:%M')}: {new_note}")
            st.rerun()
        for n in D.get("notes", []):
            st.markdown(f"<p style='font-size:12px; border-bottom:1px solid #eee; padding:5px;'>{n}</p>", unsafe_allow_html=True)

if st.sidebar.button("TERMINATE SESSION"):
    st.session_state.authenticated = False
    st.rerun()
