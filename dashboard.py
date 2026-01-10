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
        "address": "4646 S Quail Park Drive #C, Millcreek Utah 84117",
        "seller_name": "John Doe",
        "buyer_name": "Jane Smith",
        "price": 330000.00,
        "seller_equity": 20000.00,
        "assignment_fee": 15000.00,
        "terms": "Subject to existing financing.",
        "instr_title": "Standard Title Search Required.", 
        "instr_escrow": "Hold Earnest Money in neutral account.", 
        "instr_servicer": "AITD Servicing setup through [Company Name].",
        "disclosures": ["Property sold As-Is."],
        "vault": [], "notes": []
    }

# --- 3. REFINED CSS ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=Oswald:wght@500;700&display=swap');
        .stApp { background-color: #ffffff !important; }

        /* Buttons: Steady Blue with White Boundary Hover */
        div.stButton > button {
            background-color: #1d428a !important;
            color: white !important;
            border: 2px solid #1d428a !important;
            border-radius: 4px !important;
            height: 52px !important;
            width: 100% !important;
            font-family: 'Oswald', sans-serif !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
        }
        div.stButton > button:hover {
            border: 2px solid white !important;
            box-shadow: 0 0 0 2px #1d428a !important;
            color: white !important;
        }

        /* Admin Label - Dark Blue & Bold */
        .admin-label {
            font-family: 'Oswald', sans-serif !important;
            color: #1d428a !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            font-size: 13px !important;
            margin-bottom: 8px !important;
            margin-top: 18px !important;
            display: block !important;
        }

        /* Admin Header Bar (Centered Title) */
        .admin-header-bar {
            background-color: #1d428a;
            color: white;
            padding: 16px;
            text-align: center;
            border-radius: 4px;
            font-family: 'Inter', sans-serif;
            font-weight: 900;
            font-size: 22px;
            text-transform: uppercase;
            margin-bottom: 30px;
            border: 2px solid #1d428a;
        }

        /* Disclosure List Styling */
        .disclosure-item {
            background: #f1f5f9;
            color: #1d428a;
            padding: 12px;
            border-left: 5px solid #1d428a;
            margin-bottom: 8px;
            font-family: 'Inter', sans-serif;
            font-weight: 700;
            font-size: 14px;
        }
        
        input { height: 52px !important; }
    </style>
""", unsafe_allow_html=True)

# --- 4. LOGIN ---
if not st.session_state.authenticated:
    st.markdown('<div style="font-family:Inter; font-size:50px; font-weight:900; color:#1d428a; text-align:center; margin-top:80px;">UTAH LAND & PROPERTY</div>', unsafe_allow_html=True)
    _, col_mid, _ = st.columns([1, 0.6, 1])
    with col_mid:
        input_key = st.text_input("Access Key", type="password", placeholder="ENTER KEY", label_visibility="collapsed")
        if st.button("Authorize Session"):
            try:
                for user, profile in st.secrets["users"].items():
                    if input_key == str(profile["key"]):
                        st.session_state.authenticated = True
                        st.session_state.user_role = str(profile["role"]).lower()
                        st.rerun()
                st.error("DENIED")
            except: st.error("Config Missing")
    st.stop()

# --- 5. ADMIN TERMINAL ---
role = st.session_state.user_role
D = st.session_state.current_deal

if role == "admin":
    st.markdown('<div class="admin-header-bar">ADMIN: STRATEGIC DEAL JACKET</div>', unsafe_allow_html=True)
    
    with st.container(border=True):
        c1, c2 = st.columns(2)
        c1.markdown('<span class="admin-label">Property Address</span>', unsafe_allow_html=True)
        a_addr = c1.text_input("Addr", value=D["address"], label_visibility="collapsed")
        c2.markdown('<span class="admin-label">Deal ID</span>', unsafe_allow_html=True)
        a_id = c2.text_input("ID", value=D["deal_id"], label_visibility="collapsed")
        
        n1, n2 = st.columns(2)
        n1.markdown('<span class="admin-label">Seller Name</span>', unsafe_allow_html=True)
        a_seller = n1.text_input("Seller", value=D["seller_name"], label_visibility="collapsed")
        n2.markdown('<span class="admin-label">Buyer Name</span>', unsafe_allow_html=True)
        a_buyer = n2.text_input("Buyer", value=D["buyer_name"], label_visibility="collapsed")
        
        f1, f2, f3 = st.columns(3)
        f1.markdown('<span class="admin-label">Sales Price</span>', unsafe_allow_html=True)
        a_price = f1.number_input("Price", value=float(D["price"]), label_visibility="collapsed")
        f2.markdown('<span class="admin-label">Seller Equity</span>', unsafe_allow_html=True)
        a_equity = f2.number_input("Equity", value=float(D["seller_equity"]), label_visibility="collapsed")
        f3.markdown('<span class="admin-label">Assignment Fee</span>', unsafe_allow_html=True)
        a_fee = f3.number_input("Fee", value=float(D["assignment_fee"]), label_visibility="collapsed")

        st.markdown('<span class="admin-label">Title / Escrow / Servicing Instructions</span>', unsafe_allow_html=True)
        i1, i2, i3 = st.columns(3)
        a_title = i1.text_area("Title", value=D["instr_title"], label_visibility="collapsed")
        a_escrow = i2.text_area("Escrow", value=D["instr_escrow"], label_visibility="collapsed")
        a_servicer = i3.text_area("Servicer", value=D["instr_servicer"], label_visibility="collapsed")

        st.markdown('<span class="admin-label">Buyer Disclosures</span>', unsafe_allow_html=True)
        updated_discs = []
        for i, d in enumerate(D["disclosures"]):
            updated_discs.append(st.text_input(f"D{i}", value=d, key=f"d_adm_{i}", label_visibility="collapsed"))
        
        if st.button("Add Disclosure Line +"):
            D["disclosures"].append("")
            st.rerun()

        if st.button("UPDATE MASTER DASHBOARD"):
            st.session_state.current_deal.update({
                "address": a_addr, "deal_id": a_id, "seller_name": a_seller,
                "buyer_name": a_buyer, "price": a_price, "seller_equity": a_equity,
                "assignment_fee": a_fee, "instr_title": a_title, 
                "instr_escrow": a_escrow, "instr_servicer": a_servicer, 
                "disclosures": updated_discs
            })
            st.rerun()

# --- 6. DASHBOARD & VAULT ---
AITD_PRINCIPAL = D["price"] - D["seller_equity"]
st.markdown(f'<div style="font-family:Inter; font-size:36px; font-weight:900; color:#1d428a; margin-top:20px; text-transform:uppercase;">{D["address"]}</div>', unsafe_allow_html=True)

col_data, col_docs = st.columns([2, 1])

with col_data:
    st.markdown(f"""
        <div style="background:#1d428a; padding:30px; border-radius:8px; color:white; margin-bottom:20px;">
            <div style="font-family:Oswald; font-size:12px; opacity:0.8; letter-spacing:1px;">AITD PRINCIPAL BALANCE</div>
            <div style="font-family:Inter; font-size:48px; font-weight:900;">${AITD_PRINCIPAL:,.2f}</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div style="font-family:Oswald; font-size:14px; color:#1d428a; margin-bottom:12px; font-weight:700;">ACTIVE DISCLOSURES</div>', unsafe_allow_html=True)
    for disc in D["disclosures"]:
        if disc:
            st.markdown(f'<div class="disclosure-item">✔️ {disc}</div>', unsafe_allow_html=True)

with col_docs:
    with st.container(border=True):
        st.markdown('<div style="font-family:Oswald; font-size:14px; color:#1d428a; font-weight:700;">SETTLEMENT VAULT</div>', unsafe_allow_html=True)
        if role == "admin" and st.button("📄 GENERATE MASTER DEAL SHEET"):
            d_list = "\n".join([f"- {x}" for x in D["disclosures"] if x])
            # ENTIRE DEAL STRUCTURE LOGIC
            report = f"""UTAH LAND & PROPERTY: MASTER SETTLEMENT SHEET
--------------------------------------------------
DATE: {datetime.now().strftime('%Y-%m-%d %H:%M')}
DEAL ID: {D['deal_id']}
ADDRESS: {D['address']}

PARTIES:
SELLER: {D['seller_name']}
BUYER:  {D['buyer_name']}

FINANCIAL STRUCTURE:
CONTRACT PRICE:   ${D['price']:,.2f}
SELLER EQUITY:    ${D['seller_equity']:,.2f}
ASSIGNMENT FEE:   ${D['assignment_fee']:,.2f}
--------------------------------------------------
AITD PRINCIPAL:   ${AITD_PRINCIPAL:,.2f}
--------------------------------------------------

INSTRUCTIONS:
TITLE:    {D['instr_title']}
ESCROW:   {D['instr_escrow']}
SERVICER: {D['instr_servicer']}

DISCLOSURES:
{d_list}

DOCUMENT PREPARED BY UTAH LAND & PROPERTY, LLC.
"""
            D["vault"].append({"name": f"Deal_{D['deal_id']}_{datetime.now().strftime('%H%M')}.txt", "content": report})
            st.rerun()
        
        for doc in D["vault"]:
            v1, v2 = st.columns([2, 1])
            v1.markdown(f"<span style='font-size:12px; font-weight:bold; color:#1d428a;'>{doc['name']}</span>", unsafe_allow_html=True)
            b64 = base64.b64encode(doc['content'].encode()).decode()
            v2.markdown(f'<a href="data:file/txt;base64,{b64}" download="{doc["name"]}" style="color:#1d428a; font-weight:900; font-size:12px; text-decoration:underline;">PRINT</a>', unsafe_allow_html=True)

if st.sidebar.button("EXIT TERMINAL"):
    st.session_state.authenticated = False
    st.rerun()
