import base64
import numpy_financial as npf
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
import streamlit as st
import io

# --- 1. CONFIG ---
# Removed 'collapsed' to get rid of the annoying double-arrow requirement
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
        "price": 330000.00, 
        "seller_equity": 20000.00, 
        "assignment_fee": 15000.00,  
        "interest_rate": 0.0, "hoa_monthly": 0.0,
        "instr_title": "", "instr_escrow": "", "instr_servicer": "",
        "vault": []
    }

D = st.session_state.current_deal

# --- 3. CSS (FORCED BUTTON VISIBILITY) ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=Oswald:wght@500;700&display=swap');
        
        /* Force background white */
        .stApp { background-color: #ffffff !important; }

        /* Force ALL button text to be WHITE and BOLD */
        button p, .stButton > button {
            color: white !important;
            font-size: 16px !important;
            font-weight: 700 !important;
            font-family: 'Oswald', sans-serif !important;
            text-transform: uppercase !important;
        }

        /* Dark Blue Headers */
        h1, h2, h3, .section-label {
            color: #1d428a !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 900 !important;
        }

        /* Label visibility */
        label, [data-testid="stWidgetLabel"] p {
            color: #1d428a !important;
            font-weight: 700 !important;
            font-size: 14px !important;
        }

        /* Metric Boxes */
        .metric-card {
            background: #f8fafc;
            border: 2px solid #1d428a;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 10px;
        }
        
        .pmt-box {
            background: #1d428a;
            color: white !important;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# --- 4. AUTH PAGE ---
if not st.session_state.authenticated:
    st.markdown('<h1 style="text-align:center; font-size:60px;">UTAH LAND & PROPERTY</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#1d428a; font-weight:700;">ASSET PROTECTION ● MAXIMUM PRIVACY</p>', unsafe_allow_html=True)
    
    _, col_mid, _ = st.columns([1, 0.4, 1])
    with col_mid:
        key = st.text_input("Access Key", type="password")
        if st.button("AUTHORIZE SESSION"):
            try:
                for user, profile in st.secrets["users"].items():
                    if key == str(profile["key"]):
                        st.session_state.authenticated, st.session_state.user_role = True, str(profile["role"]).lower()
                        st.rerun()
                st.error("Invalid Key")
            except: st.error("Secrets.toml error")
    st.stop()

# --- 5. MATH (EQUITY BUYER $310k) ---
EQ_BUYER_BAL = D["price"] - D["seller_equity"]

def calc_pmt(principal, rate, years):
    if rate <= 0 or years <= 0: return principal / (years * 12) if (years*12) > 0 else 0
    return abs(npf.pmt(rate/100/12, years*12, principal))

t15 = calc_pmt(EQ_BUYER_BAL, D["interest_rate"], 15) + D["hoa_monthly"]
t30 = calc_pmt(EQ_BUYER_BAL, D["interest_rate"], 30) + D["hoa_monthly"]

# --- 6. ADMIN PANEL ---
if st.session_state.user_role == "admin":
    st.markdown("### ADMIN CONTROL PANEL")
    with st.container(border=True):
        c1, c2, c3, c4 = st.columns(4)
        D["address"] = c1.text_input("Address", value=D["address"])
        D["deal_id"] = c2.text_input("Deal ID", value=D["deal_id"])
        D["interest_rate"] = c3.number_input("Rate %", value=float(D["interest_rate"]))
        D["hoa_monthly"] = c4.number_input("HOA", value=float(D["hoa_monthly"]))
        
        f1, f2, f3 = st.columns(3)
        D["price"] = f1.number_input("Sale Price", value=float(D["price"]))
        D["seller_equity"] = f2.number_input("Seller Equity (Down)", value=float(D["seller_equity"]))
        D["assignment_fee"] = f3.number_input("Assignment Fee", value=float(D["assignment_fee"]))

        st.markdown("#### STRATEGIC INSTRUCTIONS")
        i1, i2, i3 = st.columns(3)
        D["instr_title"] = i1.text_area("Title Search", value=D["instr_title"])
        D["instr_escrow"] = i2.text_area("Escrow Holder", value=D["instr_escrow"])
        D["instr_servicer"] = i3.text_area("Mortgage Servicer", value=D["instr_servicer"])
        
        if st.button("SAVE CHANGES"): st.rerun()
        if st.button("REVEAL ADDRESS TO BUYER"): st.session_state.verified_by_admin = True; st.rerun()
        if st.button("LOCK ADDRESS"): st.session_state.verified_by_admin = False; st.rerun()

# --- 7. BUYER PORTAL ---
st.divider()
show = st.session_state.user_role == "admin" or st.session_state.verified_by_admin

if show and D["address"]:
    st.markdown(f"## {D['address']}")
else:
    st.markdown("## PRIVATE ASSET: UNVETTED")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### FINANCIALS")
    m1, m2, m3 = st.columns(3)
    m1.markdown(f'<div class="metric-card"><b>Price</b><br><span style="font-size:24px;">${D["price"]:,.0f}</span></div>', unsafe_allow_html=True)
    m2.markdown(f'<div class="metric-card"><b>Downpayment</b><br><span style="font-size:24px;">${D["seller_equity"]:,.0f}</span></div>', unsafe_allow_html=True)
    m3.markdown(f'<div class="metric-card"><b>Equity Buyer Bal</b><br><span style="font-size:24px;">${EQ_BUYER_BAL:,.0f}</span></div>', unsafe_allow_html=True)
    
    st.markdown(f'<div class="metric-card"><b>Assignment Fee</b><br><span style="font-size:24px;">${D["assignment_fee"]:,.0f}</span></div>', unsafe_allow_html=True)

    if show:
        st.markdown("### STRATEGIC DATA")
        st.info(f"**Escrow:** {D['instr_escrow']}\n\n**Servicer:** {D['instr_servicer']}")

with col2:
    st.markdown("### PAYMENTS")
    st.markdown(f'<div class="pmt-box">15-YR TOTAL<br><span style="font-size:28px;">${t15:,.2f}</span></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f'<div class="pmt-box">30-YR TOTAL<br><span style="font-size:28px;">${t30:,.2f}</span></div>', unsafe_allow_html=True)

if st.sidebar.button("LOGOUT"):
    st.session_state.authenticated = False
    st.rerun()
