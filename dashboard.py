import base64
import io
import hashlib
from datetime import datetime

import streamlit as st
from streamlit_autorefresh import st_autorefresh
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas

# ==================================================
# 1. CONFIG & REFRESH
# ==================================================
st.set_page_config(
    page_title="Utah Land & Property",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st_autorefresh(interval=10000, key="ulp_sync_ping")

# ==================================================
# 2. SESSION STATE & SHARED DEAL STORE
# ==================================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_role = None

if "shared_deals" not in st.session_state:
    st.session_state.shared_deals = {}

if "active_deal_id" not in st.session_state:
    st.session_state.active_deal_id = "DEAL-PRIMARY"


def deal_hash(deal: dict) -> str:
    payload = f"{deal['price']}{deal['seller_equity']}{deal['assignment_fee']}"
    return hashlib.md5(payload.encode()).hexdigest()


if st.session_state.active_deal_id not in st.session_state.shared_deals:
    st.session_state.shared_deals[st.session_state.active_deal_id] = {
        "deal_id": st.session_state.active_deal_id,
        "price": 330000.00,
        "seller_equity": 20000.00,
        "assignment_fee": 15000.00,
        "vault": [],
        "notes": [],
        "version": ""
    }

D = st.session_state.shared_deals[st.session_state.active_deal_id]

# ==================================================
# 3. AUTH TERMINAL — ORIGINAL LOOK (FIXED CENTERING)
# ==================================================
if not st.session_state.authenticated:

    pillar_icons = [
        '<svg viewBox="0 0 24 24" width="80" height="80" stroke="#1d428a" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>',
        '<svg viewBox="0 0 24 24" width="80" height="80" stroke="#1d428a" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>',
    ]

    icon_stack = "".join(
        [f'<div class="flip-logo" style="animation-delay:{i * 3}s">{svg}</div>'
         for i, svg in enumerate(pillar_icons)]
    )

    st.markdown(f"""
    <style>
    @import url("https://fonts.googleapis.com/css2?family=Inter:wght@900&family=Oswald:wght@700&display=swap");

    html, body, .stApp {{
        background-color: #ffffff !important;
    }}

    header, footer, [data-testid="stHeader"] {{
        display: none !important;
    }}

    section.main > div {{
        padding-top: 0 !important;
    }}

    .main-auth-container {{
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
    }}

    .ulp-auth-title {{
        font-family: "Inter", sans-serif;
        font-size: clamp(32px, 8vw, 80px);
        font-weight: 900;
        color: #1d428a;
        letter-spacing: -4px;
        line-height: 1.0;
        margin-bottom: 10px;
        text-transform: uppercase;
    }}

    .logo-container {{
        position: relative;
        height: 100px;
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 20px 0;
    }}

    .flip-logo {{
        position: absolute;
        opacity: 0;
        animation: logoFlip {len(pillar_icons)*3}s infinite;
    }}

    @keyframes logoFlip {{
        0% {{ opacity: 0; transform: scale(0.85); }}
        5% {{ opacity: 1; }}
        30% {{ opacity: 1; }}
        33% {{ opacity: 0; transform: scale(1.05); }}
        100% {{ opacity: 0; }}
    }}

    .sync-box {{
        margin-bottom: 30px;
        display: flex;
        align-items: center;
        gap: 8px;
    }}

    .pulse-dot {{
        height: 10px;
        width: 10px;
        background-color: #00ff41;
        border-radius: 50%;
        box-shadow: 0 0 10px #00ff41;
        animation: pulse-green 1.5s infinite;
    }}

    @keyframes pulse-green {{
        0% {{ box-shadow: 0 0 0px 0px rgba(0,255,65,0.7); }}
        70% {{ box-shadow: 0 0 0px 10px rgba(0,255,65,0); }}
        100% {{ box-shadow: 0 0 0px 0px rgba(0,255,65,0); }}
    }}

    .sync-label {{
        font-family: "Oswald", sans-serif;
        font-size: 14px;
        color: #1d428a;
        letter-spacing: 2px;
        font-weight: bold;
        text-transform: uppercase;
    }}

    input {{
        text-align: center !important;
        font-size: 18px !important;
    }}

    div.stButton > button {{
        background-color: #1d428a !important;
        color: #ffffff !important;
        font-family: 'Oswald', sans-serif !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        padding: 15px 0 !important;
        border: 2px solid #1d428a !important;
        width: 100%;
        margin-top: 10px;
    }}
    </style>

    <div class="main-auth-container">
        <div class="ulp-auth-title">Utah Land & Property</div>
        <div class="logo-container">{icon_stack}</div>
        <div class="sync-box">
            <span class="pulse-dot"></span>
            <span class="sync-label">Secure Access Terminal</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    _, col_mid, _ = st.columns([1.2, 1, 1.2])
    with col_mid:
        input_key = st.text_input(
            "Security Key",
            type="password",
            placeholder="ENTER PRIVATE ACCESS KEY",
            label_visibility="collapsed"
        )

        if st.button(
            "Authorize Session",
            disabled=st.session_state.get("auth_lock", False)
        ):
            st.session_state.auth_lock = True
            try:
                for _, profile in st.secrets["users"].items():
                    if input_key == str(profile["key"]):
                        st.session_state.authenticated = True
                        st.session_state.user_role = profile["role"]
                        st.session_state.auth_lock = False
                        st.rerun()

                st.error("ACCESS DENIED")
                st.session_state.auth_lock = False
            except:
                st.error("SYSTEM ERROR: CHECK SECRETS")
                st.session_state.auth_lock = False

    st.stop()

# ==================================================
# 4. USER AUTO-SYNC
# ==================================================
role = st.session_state.user_role
if role != "admin":
    if "local_version" not in st.session_state:
        st.session_state.local_version = D["version"]
    if D["version"] != st.session_state.local_version:
        st.session_state.local_version = D["version"]
        st.toast("🔄 Deal Updated by Admin")
        st.rerun()

# ==================================================
# 5. ADMIN DEAL MANAGEMENT
# ==================================================
if role == "admin":
    with st.expander("🛡️ ADMIN: DEAL MANAGEMENT TERMINAL", expanded=False):
        c1, c2, c3 = st.columns(3)
        p = c1.number_input("Sales Price", value=D["price"])
        e = c2.number_input("Seller Equity", value=D["seller_equity"])
        f = c3.number_input("ULP Assignment Fee", value=D["assignment_fee"])

        if st.button("🔁 RESTRUCTURE & PUSH LIVE", use_container_width=True):
            D["price"], D["seller_equity"], D["assignment_fee"] = p, e, f
            D["version"] = deal_hash(D)
            st.toast("Deal pushed live")
            st.rerun()

# ==================================================
# 6. CORE DASHBOARD
# ==================================================
AITD = D["price"] - D["seller_equity"]

st.markdown("## Utah Land & Property")
st.caption(f"SESSION: {D['deal_id']} | ROLE: {role.upper()}")

c1, c2 = st.columns([2, 1])
c1.metric("AITD Principal Balance", f"${AITD:,.2f}")
c2.metric("ULP Assignment Fee", f"${D['assignment_fee']:,.2f}")

# ==================================================
# 7. TRANSACTION HUB
# ==================================================
st.markdown("### Transaction Hub")

v_col, n_col = st.columns([1.5, 1])

with v_col:
    if role == "admin" and st.button("📄 GENERATE PDF SETTLEMENT"):
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=LETTER)
        w, h = LETTER

        c.setFont("Helvetica-Bold", 18)
        c.drawString(72, h - 72, "Utah Land & Property – Settlement Summary")

        c.setFont("Helvetica", 12)
        y = h - 140
        for line in [
            f"Deal ID: {D['deal_id']}",
            f"Sales Price: ${D['price']:,.2f}",
            f"Seller Equity Credit: ${D['seller_equity']:,.2f}",
            f"AITD Balance: ${AITD:,.2f}",
            f"ULP Assignment Fee: ${D['assignment_fee']:,.2f}",
            "",
            f"Generated: {datetime.now().strftime('%m/%d/%Y %H:%M')}"
        ]:
            c.drawString(72, y, line)
            y -= 22

        c.showPage()
        c.save()
        buffer.seek(0)

        D["vault"].append({
            "name": f"Settlement_{D['deal_id']}.pdf",
            "content": buffer.read()
        })

        st.success("PDF Generated")

    for doc in D["vault"]:
        b64 = base64.b64encode(doc["content"]).decode()
        st.markdown(
            f'<a href="data:application/pdf;base64,{b64}" download="{doc["name"]}">📥 {doc["name"]}</a>',
            unsafe_allow_html=True
        )

with n_col:
    note = st.text_input("Add Note", label_visibility="collapsed")
    if st.button("Post") and note:
        D["notes"].insert(0, f"{datetime.now().strftime('%H:%M')} – {note}")
        st.rerun()

    for n in D["notes"]:
        st.markdown(f"- {n}")

# ==================================================
# 8. LOGOUT
# ==================================================
if st.sidebar.button("LOGOUT"):
    st.session_state.authenticated = False
    st.rerun()
