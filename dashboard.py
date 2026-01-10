import base64
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
import streamlit as st

# --- 1. CONFIG & REFRESH ---
st.set_page_config(page_title="Utah Land & Property", layout="wide", initial_sidebar_state="collapsed")
st_autorefresh(interval=10000, key="ulp_sync_ping")

# --- 2. DATA PERSISTENCE & NEW SECTIONS ---
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
        "instr_title": "Standard Title Search Required.",
        "instr_escrow": "Hold Earnest Money in neutral account.",
        "instr_servicer": "AITD Servicing setup through [Company Name].",
        "disclosures": ["Property sold As-Is."], # Dynamic List
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
        [data-testid="stAppViewBlockContainer"] {{ display: flex; flex-direction: column; justify-content: center; align-items: center; min-height: 85vh; }}
        .ulp-auth-title {{ font-family: "Inter", sans-serif; font-size: clamp(32px, 8vw, 80px); font-weight: 900; color: #1d428a; letter-spacing: -4px; line-height: 1.0; margin-bottom: 10px; text-align: center; text-transform: uppercase; }}
        .logo-container {{ position: relative; height: 120px; width: 100%; display: flex; justify-content: center; align-items: center; margin: 10px 0; }}
        .flip-logo {{ position: absolute; opacity: 0; animation: logoFlip {len(pillar_icons)*3}s infinite; }}
        @keyframes logoFlip {{ 0% {{ opacity: 0; transform: scale(0.8); }} 1% {{ opacity: 1; transform: scale(1); }} 30% {{ opacity: 1; }} 33% {{ opacity: 0; transform: scale(1.05); }} 100% {{ opacity: 0; }} }}
        div.stButton > button {{ 
            background-color: #1d428a !important; color: #FFFFFF !important; font-family: 'Oswald', sans-serif !important; 
            font-weight: 700 !important; text-transform: uppercase !important; letter-spacing: 2px !important; 
            border: 2px solid #1d428a !important; width: 100% !important; margin-top: 10px !important; 
            height: 52px !important; border-radius: 4px !important; cursor: pointer;
        }}
        [data-testid="stTextInput"] {{ width: 100% !important; }}
        input {{ text-align: center !important; font-size: 18px !important; color: #1d428a !important; height: 52px !important; }}
        </style>
        <div class="ulp-auth-title">Utah Land & Property</div>
        <div class="logo-container">{icon_stack}</div>
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
            except: st.error("Secrets Config Missing")
    st.stop()

# --- 4. DASHBOARD STYLING ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=Oswald:wght@500;700&display=swap');
        .stApp { background-color: #ffffff !important; }
        .admin-terminal { background: #f8fafc; border: 3px solid #1d428a; padding: 30px; border-radius: 12px; margin-bottom: 30px; }
        .admin-title { font-family: 'Inter', sans-serif; font-weight: 900; text-align: center; font-size: 24px; text-transform: uppercase; color: #1d428a; margin-bottom: 25px; }
        .admin-label { font-family: 'Oswald', sans-serif !important; color: #1d428a !important; font-weight: 700 !important; text-transform: uppercase !important; font-size: 13px; margin-bottom: -15px; }
        .hero-bento { background: #1d428a; color: #ffffff; padding: 30px; border-radius: 12px; }
        .ulp-header { font-family: 'Inter', sans-serif; font-size: 36px; font-weight: 900; color: #1d428a; text-transform: uppercase; }
        .label-text { font-family: 'Oswald'; font-size: 11px; letter-spacing: 1px; color: #475569; text-transform: uppercase; font-weight: 700; }
    </style>
""", unsafe_allow_html=True)

# --- 5. ADMIN COMMAND CENTER ---
role = st.session_state.user_role
D = st.session_state.current_deal

if role == "admin":
    st.markdown('<div class="admin-terminal">', unsafe_allow_html=True)
    st.markdown('<div class="admin-title">ADMIN: STRATEGIC DEAL JACKET</div>', unsafe_allow_html=True)
    
    # Financial & Property Basics
    c1, c2 = st.columns(2)
    c1.markdown('<p class="admin-label">Property Address</p>', unsafe_allow_html=True)
    a_addr = c1.text_input("Property Address", value=D["address"], label_visibility="collapsed")
    c2.markdown('<p class="admin-label">Deal ID</p>', unsafe_allow_html=True)
    a_id = c2.text_input("Deal ID", value=D["deal_id"], label_visibility="collapsed")
    
    f1, f2, f3 = st.columns(3)
    f1.markdown('<p class="admin-label">Sales Price</p>', unsafe_allow_html=True)
    a_price = f1.number_input("Sales Price", value=float(D["price"]), label_visibility="collapsed")
    f2.markdown('<p class="admin-label">Seller Equity</p>', unsafe_allow_html=True)
    a_equity = f2.number_input("Seller Equity", value=float(D["seller_equity"]), label_visibility="collapsed")
    f3.markdown('<p class="admin-label">Assignment Fee</p>', unsafe_allow_html=True)
    a_fee = f3.number_input("Assignment Fee", value=float(D["assignment_fee"]), label_visibility="collapsed")

    # Instruction Blocks
    st.markdown("---")
    i1, i2, i3 = st.columns(3)
    i1.markdown('<p class="admin-label">Instructions to Title</p>', unsafe_allow_html=True)
    a_title = i1.text_area("Title", value=D["instr_title"], label_visibility="collapsed")
    i2.markdown('<p class="admin-label">Instructions to Escrow</p>', unsafe_allow_html=True)
    a_escrow = i2.text_area("Escrow", value=D["instr_escrow"], label_visibility="collapsed")
    i3.markdown('<p class="admin-label">Instructions to Servicer</p>', unsafe_allow_html=True)
    a_servicer = i3.text_area("Servicer", value=D["instr_servicer"], label_visibility="collapsed")

    # Disclosures Section (+)
    st.markdown('<p class="admin-label">Buyer Disclosures</p>', unsafe_allow_html=True)
    temp_disclosures = []
    for i, disc in enumerate(D["disclosures"]):
        temp_disclosures.append(st.text_input(f"Disc {i+1}", value=disc, key=f"disc_{i}", label_visibility="collapsed"))
    
    if st.button("Add Disclosure Line +"):
        D["disclosures"].append("")
        st.rerun()

    if st.button("UPDATE MASTER DASHBOARD", use_container_width=True):
        st.session_state.current_deal.update({
            "address": a_addr, "deal_id": a_id, "price": a_price, 
            "seller_equity": a_equity, "assignment_fee": a_fee,
            "instr_title": a_title, "instr_escrow": a_escrow, "instr_servicer": a_servicer,
            "disclosures": temp_disclosures
        })
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- 6. LIVE DASHBOARD ---
AITD_PRINCIPAL = D["price"] - D["seller_equity"]
st.markdown('<div class="ulp-header">Utah Land & Property</div>', unsafe_allow_html=True)
st.caption(f"PROPERTY: {D['address']} | ID: {D['deal_id']}")

col_h, col_s = st.columns([2, 1])
with col_h:
    st.markdown(f"""
        <div class="hero-bento">
            <div class="label-text" style="color: #cbd5e1;">AITD PRINCIPAL BALANCE</div>
            <div style="font-family: 'Inter'; font-size: 50px; font-weight: 900; color: white;">${AITD_PRINCIPAL:,.2f}</div>
            <div style="height: 1px; background: rgba(255,255,255,0.2); margin: 20px 0;"></div>
            <div style="display: flex; justify-content: space-between; color: white;">
                <div><div class="label-text" style="color:#cbd5e1">SALES PRICE</div><div style="font-size:20px; font-weight:700;">${D['price']:,.2f}</div></div>
                <div style="text-align:right;"><div class="label-text" style="color:#cbd5e1">SELLER EQUITY</div><div style="font-size:20px; font-weight:700;">${D['seller_equity']:,.2f}</div></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col_s:
    with st.container(border=True):
        st.markdown('<p class="label-text">Buyer Disclosures</p>', unsafe_allow_html=True)
        for disc in D["disclosures"]:
            if disc: st.markdown(f"✅ <span style='font-size:12px; font-weight:bold; color:#1d428a;'>{disc}</span>", unsafe_allow_html=True)

# --- 7. VAULT ---
with st.container(border=True):
    st.markdown("<p class='label-text'>Settlement Vault</p>", unsafe_allow_html=True)
    if role == "admin" and st.button("📄 GENERATE MASTER DEAL SHEET"):
        disc_text = "\n".join([f"- {d}" for d in D["disclosures"]])
        report = f"""UTAH LAND & PROPERTY MASTER DEAL SHEET
--------------------------------------------------
ADDRESS: {D['address']}
AITD PRINCIPAL: ${AITD_PRINCIPAL:,.2f}
--------------------------------------------------
TITLE INSTR: {D['instr_title']}
ESCROW INSTR: {D['instr_escrow']}
SERVICER INSTR: {D['instr_servicer']}
--------------------------------------------------
DISCLOSURES:
{disc_text}
"""
        D["vault"].append({"name": f"Master_Jacket_{D['deal_id']}.txt", "content": report})
        st.rerun()
    
    for doc in D["vault"]:
        v1, v2 = st.columns([3, 1])
        v1.write(f"📁 **{doc['name']}**")
        b64 = base64.b64encode(doc['content'].encode()).decode()
        v2.markdown(f'<a href="data:file/txt;base64,{b64}" download="{doc["name"]}" style="color:#1d428a; font-weight:bold;">PRINT/PDF</a>', unsafe_allow_html=True)

if st.sidebar.button("TERMINATE SESSION"):
    st.session_state.authenticated = False
    st.rerun()
