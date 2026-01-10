import base64
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
import streamlit as st
from PIL import Image

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
        "seller_name": "Douglas Stewart",
        "buyer_name": "Ashley Adams",
        "price": 455000.00,
        "seller_equity": 40000.00,
        "assignment_fee": 15000.00,
        "instr_title": "Standard Title Search Required.", 
        "instr_escrow": "Hold Earnest Money in neutral account.", 
        "instr_servicer": "AITD Servicing setup through [Company Name].",
        "disclosures": ["Property sold As-Is."],
        "vault": [], "images": []
    }

# --- 3. CSS (DEEP CLEAN & INSTITUTIONAL) ---
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
        .stDeployButton {display:none;} [data-testid="stHeader"] {background: rgba(0,0,0,0);}
        .stApp { background-color: #ffffff !important; }
        .branding-container { text-align: center; margin-bottom: 20px; }
        .branding-text { color: #1d428a !important; font-family: 'Oswald', sans-serif; font-weight: 700; font-size: 18px; text-transform: uppercase; letter-spacing: 1.5px; display: inline-block; vertical-align: middle; }
        .blink-indicator { height: 12px; width: 12px; background-color: #00ff00; border-radius: 50%; display: inline-block; margin-right: 12px; vertical-align: middle; box-shadow: 0 0 10px #00ff00; animation: blink 1.2s infinite; }
        @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.2; } 100% { opacity: 1; } }
        div.stButton > button { background-color: #1d428a !important; color: white !important; border: 2px solid #1d428a !important; border-radius: 4px !important; height: 56px !important; width: 100% !important; font-family: 'Oswald', sans-serif !important; font-weight: 700 !important; text-transform: uppercase !important; }
        [data-testid="stTextInput"] input { height: 56px !important; background-color: #1d428a !important; border: 2px solid #1d428a !important; border-radius: 4px !important; text-align: center !important; font-size: 18px !important; font-weight: 700 !important; color: white !important; }
        .admin-header-bar { background-color: #1d428a; color: white !important; padding: 16px; text-align: center; border-radius: 4px; font-family: 'Inter', sans-serif; font-weight: 900; font-size: 22px; text-transform: uppercase; margin-bottom: 30px; }
        .admin-label { font-family: 'Oswald', sans-serif !important; color: #1d428a !important; font-weight: 700 !important; text-transform: uppercase !important; font-size: 13px !important; margin-bottom: 8px; margin-top: 18px; display: block !important; }
        .buyer-card { background: #f1f5f9; padding: 20px; border-left: 5px solid #1d428a; border-radius: 4px; margin-bottom: 10px; }
        .buyer-label { font-family: 'Oswald', sans-serif; color: #1d428a; font-size: 11px; text-transform: uppercase; }
        .buyer-value { font-family: 'Inter', sans-serif; color: #1d428a; font-size: 26px; font-weight: 900; }
        .disclosure-item { background: #f1f5f9; color: #1d428a; padding: 12px; border-left: 5px solid #1d428a; margin-bottom: 8px; font-family: 'Inter', sans-serif; font-weight: 700; }
    </style>
""", unsafe_allow_html=True)

# --- 4. AUTH PAGE ---
if not st.session_state.authenticated:
    st.markdown('<div style="height: 15vh;"></div><div style="font-family:Inter; font-size:clamp(40px, 10vw, 75px); font-weight:900; color:#1d428a; text-align:center; line-height:0.9; margin-bottom:15px;">UTAH LAND & PROPERTY</div>', unsafe_allow_html=True)
    st.markdown('<div class="branding-container"><span class="blink-indicator"></span><span class="branding-text">Asset protection ● Maximum privacy ● Anonymous holdings</span></div>', unsafe_allow_html=True)
    _, col_mid, _ = st.columns([1, 0.45, 1])
    with col_mid:
        input_key = st.text_input("Access Key", type="password", placeholder="ENTER ACCESS KEY", label_visibility="collapsed")
        st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
        if st.button("Authorize Session"):
            try:
                for user, profile in st.secrets["users"].items():
                    if input_key == str(profile["key"]):
                        st.session_state.authenticated = True
                        st.session_state.user_role = str(profile["role"]).lower()
                        st.rerun()
                st.error("ACCESS DENIED")
            except: st.error("Config Error")
    st.stop()

# --- 5. DATA SYNC ---
role = st.session_state.user_role
D = st.session_state.current_deal
AITD_BAL = D["price"] - D["seller_equity"]

# --- 6. ADMIN TERMINAL ---
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
        f2.markdown('<span class="admin-label">Seller Equity Credit</span>', unsafe_allow_html=True)
        a_equity = f2.number_input("Equity", value=float(D["seller_equity"]), label_visibility="collapsed")
        f3.markdown('<span class="admin-label">Assignment Fee</span>', unsafe_allow_html=True)
        a_fee = f3.number_input("Fee", value=float(D["assignment_fee"]), label_visibility="collapsed")

        st.markdown('<span class="admin-label">Media Vault (Upload Images)</span>', unsafe_allow_html=True)
        up_files = st.file_uploader("Upload", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
        if up_files: D["images"] = [Image.open(x) for x in up_files]

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
            D["disclosures"].append(""); st.rerun()

        if st.button("UPDATE MASTER DASHBOARD"):
            D.update({"address": a_addr, "deal_id": a_id, "seller_name": a_seller, "buyer_name": a_buyer, "price": a_price, "seller_equity": a_equity, "assignment_fee": a_fee, "instr_title": a_title, "instr_escrow": a_escrow, "instr_servicer": a_servicer, "disclosures": updated_discs})
            st.rerun()

# --- 7. DASHBOARD & SETTLEMENT VAULT ---
st.markdown("---")
st.markdown(f'<div style="font-family:Inter; font-size:36px; font-weight:900; color:#1d428a; text-transform:uppercase;">{D["address"]}</div>', unsafe_allow_html=True)

if D["images"]:
    st.markdown('<div style="font-family:Oswald; font-size:14px; color:#1d428a; margin-top:20px; font-weight:700;">PROPERTY GALLERY</div>', unsafe_allow_html=True)
    icols = st.columns(3)
    for idx, img in enumerate(D["images"]): icols[idx % 3].image(img, use_container_width=True)

col_data, col_docs = st.columns([2, 1])
with col_data:
    p1, p2, p3 = st.columns(3)
    p1.markdown(f'<div class="buyer-card"><div class="buyer-label">Contract Price</div><div class="buyer-value">${D["price"]:,.2f}</div></div>', unsafe_allow_html=True)
    p2.markdown(f'<div class="buyer-card"><div class="buyer-label">Seller Equity Credit</div><div class="buyer-value">${D["seller_equity"]:,.2f}</div></div>', unsafe_allow_html=True)
    p3.markdown(f'<div class="buyer-card" style="background:#1d428a;"><div class="buyer-label" style="color:white;">AITD Principal Balance</div><div class="buyer-value" style="color:white;">${AITD_BAL:,.2f}</div></div>', unsafe_allow_html=True)
    
    st.markdown('<div style="font-family:Oswald; font-size:14px; color:#1d428a; margin-top:20px; font-weight:700;">ACTIVE DISCLOSURES</div>', unsafe_allow_html=True)
    for disc in D["disclosures"]:
        if disc: st.markdown(f'<div class="disclosure-item">✔️ {disc}</div>', unsafe_allow_html=True)

with col_docs:
    with st.container(border=True):
        st.markdown('<div style="font-family:Oswald; font-size:14px; color:#1d428a; font-weight:700;">SETTLEMENT VAULT</div>', unsafe_allow_html=True)
        if role == "admin" and st.button("📄 GENERATE MASTER DEAL SHEET"):
            d_list = "\n".join([f"- {x}" for x in D["disclosures"] if x])
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
AITD PRINCIPAL:   ${AITD_BAL:,.2f}
--------------------------------------------------

INSTRUCTIONS:
TITLE:    {D['instr_title']}
ESCROW:   {D['instr_escrow']}
SERVICER: {D['instr_servicer']}

DISCLOSURES:
{d_list}

--------------------------------------------------
SIGNATURES:

X_________________________________
BUYER: {D['buyer_name']}

X_________________________________
SELLER: {D['seller_name']}

DOCUMENT PREPARED BY UTAH LAND & PROPERTY, LLC."""
            D["vault"].append({"name": f"Deal_{D['deal_id']}_{datetime.now().strftime('%H%M')}.txt", "content": report})
            st.rerun()
        for doc in D["vault"]:
            v1, v2 = st.columns([2, 1])
            v1.markdown(f"<span style='font-size:12px; font-weight:bold; color:#1d428a;'>{doc['name']}</span>", unsafe_allow_html=True)
            b64 = base64.b64encode(doc['content'].encode()).decode()
            v2.markdown(f'<a href="data:file/txt;base64,{b64}" download="{doc["name"]}" style="color:#1d428a; font-weight:900; font-size:12px; text-decoration:underline;">PRINT</a>', unsafe_allow_html=True)

if st.sidebar.button("TERMINATE SESSION"):
    st.session_state.authenticated = False; st.rerun()
