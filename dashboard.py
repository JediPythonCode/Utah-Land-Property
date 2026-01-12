import base64
import numpy_financial as npf
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
import streamlit as st

# --- 1. CONFIG ---
st.set_page_config(page_title="Utah Land & Property", layout="wide", initial_sidebar_state="expanded")
st_autorefresh(interval=10000, key="ulp_sync_ping")

# --- 2. DATA PERSISTENCE ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_role = None
    st.session_state.verified_by_admin = False

if "current_deal" not in st.session_state:
    st.session_state.current_deal = {
        "deal_id": "", "address": "", 
        "price": 0.0, "seller_equity": 20000.00, "assignment_fee": 15000.00,  
        "interest_rate": 0.0, "hoa_monthly": 0.0,
        "instr_title": "", "instr_escrow": "", "instr_servicer": "",
        "vault": []
    }

D = st.session_state.current_deal

# --- 3. THE ORIGINAL STYLING (DARK BLUE & BOLD) ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=Oswald:wght@500;700&display=swap');
        #MainMenu, footer, header {visibility: hidden;}
        .stApp { background-color: #ffffff !important; }
        
        /* Forced Dark Blue Text */
        .blue-text { color: #1d428a !important; font-family: 'Oswald', sans-serif; font-weight: 700; text-transform: uppercase; }
        .big-value { color: #1d428a !important; font-family: 'Inter', sans-serif; font-weight: 900; font-size: 38px; line-height: 1; }
        
        /* Buttons */
        div.stButton > button { 
            background-color: #1d428a !important; color: white !important; border-radius: 4px !important; 
            font-family: 'Oswald', sans-serif !important; font-weight: 700 !important; height: 50px !important; width: 100% !important;
        }
        
        /* Data Cards */
        .data-card { background: #f1f5f9; padding: 20px; border-left: 6px solid #1d428a; border-radius: 4px; margin-bottom: 15px; }
        .pmt-box { background: #1d428a; color: white !important; padding: 25px; border-radius: 4px; text-align: center; }
        
        /* Label Overrides */
        label, [data-testid="stWidgetLabel"] p { color: #1d428a !important; font-weight: 700 !important; font-family: 'Oswald', sans-serif !important; }
    </style>
""", unsafe_allow_html=True)

# --- 4. AUTH PAGE ---
if not st.session_state.authenticated:
    st.markdown('<div style="height: 15vh;"></div><h1 style="text-align:center; color:#1d428a; font-family:Inter; font-weight:900; font-size:60px; line-height:0.9;">UTAH LAND & PROPERTY</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#1d428a; font-family:Oswald; font-weight:700; letter-spacing:2px;">ASSET PROTECTION ● MAXIMUM PRIVACY</p>', unsafe_allow_html=True)
    _, col_mid, _ = st.columns([1, 0.4, 1])
    with col_mid:
        key = st.text_input("Access Key", type="password", placeholder="ENTER KEY", label_visibility="collapsed")
        if st.button("AUTHORIZE SESSION"):
            for user, profile in st.secrets["users"].items():
                if key == str(profile["key"]):
                    st.session_state.authenticated, st.session_state.user_role = True, str(profile["role"]).lower()
                    st.rerun()
    st.stop()

# --- 5. LOGIC & MEMO ---
EQ_BUYER_BAL = D["price"] - D["seller_equity"]

def calc_pmt(principal, rate, years):
    if rate <= 0 or years <= 0: return principal / (years * 12) if (years*12) > 0 else 0
    return abs(npf.pmt(rate/100/12, years*12, principal))

t15 = calc_pmt(EQ_BUYER_BAL, D["interest_rate"], 15) + D["hoa_monthly"]
t30 = calc_pmt(EQ_BUYER_BAL, D["interest_rate"], 30) + D["hoa_monthly"]

def generate_memo():
    return f"""UTAH LAND & PROPERTY, LLC - DEAL MEMO\nPROPERTY: {D['address']}\nPRICE: ${D['price']:,.2f}\nDOWNPAYMENT: ${D['seller_equity']:,.2f}\nEQUITY BUYER BALANCE: ${EQ_BUYER_BAL:,.2f}\nFEE: ${D['assignment_fee']:,.2f}"""

# --- 6. ADMIN PANEL ---
if st.session_state.user_role == "admin":
    st.markdown('<h2 class="blue-text">ADMIN: PRIVATE DEAL JACKET</h2>', unsafe_allow_html=True)
    with st.container(border=True):
        c1, c2, c3, c4 = st.columns(4)
        D["address"] = c1.text_input("Address", value=D["address"])
        D["deal_id"] = c2.text_input("Deal ID", value=D["deal_id"])
        D["interest_rate"] = c3.number_input("Rate %", value=float(D["interest_rate"]))
        D["hoa_monthly"] = c4.number_input("HOA", value=float(D["hoa_monthly"]))
        f1, f2, f3 = st.columns(3)
        D["price"] = f1.number_input("Sale Price", value=float(D["price"]))
        D["seller_equity"] = f2.number_input("Downpayment (Equity)", value=float(D["seller_equity"]))
        D["assignment_fee"] = f3.number_input("Assignment Fee", value=float(D["assignment_fee"]))
        st.markdown('<p class="blue-text">STRATEGIC INSTRUCTIONS</p>', unsafe_allow_html=True)
        i1, i2, i3 = st.columns(3)
        D["instr_title"] = i1.text_area("Title Search", value=D["instr_title"])
        D["instr_escrow"] = i2.text_area("Escrow Holder", value=D["instr_escrow"])
        D["instr_servicer"] = i3.text_area("Mortgage Servicer", value=D["instr_servicer"])
        if st.button("UPDATE PORTAL DATA"): st.rerun()
        if st.button("✅ REVEAL ADDRESS"): st.session_state.verified_by_admin = True; st.rerun()
        if st.button("🔒 LOCK ADDRESS"): st.session_state.verified_by_admin = False; st.rerun()

# --- 7. BUYER PORTAL (THE ORIGINAL VIEW) ---
st.markdown("---")
show = st.session_state.user_role == "admin" or st.session_state.verified_by_admin

if show and D["address"]:
    st.markdown(f'<h1 class="blue-text" style="font-size:45px;">{D["address"]}</h1>', unsafe_allow_html=True)
    st.download_button("🖨️ PRINT DEAL MEMO", data=generate_memo(), file_name=f"ULP_Memo_{D['deal_id']}.txt")
else:
    st.markdown('<h1 class="blue-text" style="font-size:45px;">PRIVATE ASSET: UNVETTED</h1>', unsafe_allow_html=True)

col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown('<p class="blue-text">FINANCIAL SUMMARY</p>', unsafe_allow_html=True)
    # Price
    st.markdown(f'<div class="data-card"><span class="blue-text">Sale Price</span><br><span class="big-value">${D["price"]:,.2f}</span></div>', unsafe_allow_html=True)
    # Downpayment
    st.markdown(f'<div class="data-card"><span class="blue-text">Downpayment (Seller Equity)</span><br><span class="big-value">${D["seller_equity"]:,.2f}</span></div>', unsafe_allow_html=True)
    # Equity Buyer Principal
    st.markdown(f'<div class="data-card" style="background:#1d428a;"><span style="color:white; font-family:Oswald; font-weight:700;">EQUITY BUYER BALANCE</span><br><span style="color:white; font-family:Inter; font-weight:900; font-size:38px;">${EQ_BUYER_BAL:,.2f}</span></div>', unsafe_allow_html=True)
    # Assignment Fee
    st.markdown(f'<div class="data-card"><span class="blue-text">Assignment Fee</span><br><span class="big-value">${D["assignment_fee"]:,.2f}</span></div>', unsafe_allow_html=True)

    if show:
        st.markdown('<p class="blue-text">STRATEGIC DATA</p>', unsafe_allow_html=True)
        st.info(f"**ESCROW:** {D['instr_escrow']}\n\n**SERVICER:** {D['instr_servicer']}")

with col_right:
    st.markdown('<p class="blue-text">PAYMENT CALCULATOR</p>', unsafe_allow_html=True)
    st.markdown(f'<div class="pmt-box"><span style="font-size:14px; opacity:0.8;">15-YR TOTAL</span><br><span style="font-size:36px; font-weight:900;">${t15:,.2f}</span></div>', unsafe_allow_html=True)
    st.markdown("<div style='height:15px;'></div>", unsafe_allow_html=True)
    st.markdown(f'<div class="pmt-box"><span style="font-size:14px; opacity:0.8;">30-YR TOTAL</span><br><span style="font-size:36px; font-weight:900;">${t30:,.2f}</span></div>', unsafe_allow_html=True)

    st.markdown('<p class="blue-text" style="margin-top:20px;">SETTLEMENT VAULT</p>', unsafe_allow_html=True)
    if not show:
        with st.form("vetting"):
            up = st.file_uploader("Upload ID to Unlock", type=['pdf','jpg','png'])
            if st.form_submit_button("SUBMIT"):
                if up: D["vault"].append({"name": up.name, "content": up.getvalue()}); st.success("Submitted.")
    else:
        for doc in D["vault"]:
            b64 = base64.b64encode(doc['content']).decode()
            st.markdown(f'<a href="data:application/octet-stream;base64,{b64}" download="{doc["name"]}" style="color:#1d428a; font-weight:bold;">📄 {doc["name"]} (PRINT)</a>', unsafe_allow_html=True)

if st.sidebar.button("LOGOUT"): st.session_state.authenticated = False; st.rerun()
