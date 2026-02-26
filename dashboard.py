import streamlit as st
import streamlit.components.v1 as components
import os
from datetime import datetime
from automation_engine import generate_utah_addendum
from library import SHIELD_LIBRARY

# --- 1. PAGE SETUP ---
st.set_page_config(
    page_title="Utah Land & Property | Secure Asset Portal",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed" 
)

# --- 2. AUTHENTICATION LOGIC (STOCHASTIC PROTECTION) ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

SECRET_PASSWORD = st.secrets.get("acquisition_password", "gold2026")

# --- 3. CSS: FULL-WIDTH & SIDEBAR STYLING ---
st.markdown("""
    <style>
        #MainMenu, footer, header {visibility: hidden;}
        .block-container { padding: 0rem !important; max-width: 100% !important; }
        [data-testid="stSidebar"] { 
            background-color: #631D33 !important; 
            color: white !important; 
        }
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] label { color: white !important; }
        .stButton>button { background-color: #D4AF37 !important; color: black !important; font-weight: bold; width: 100%; border-radius: 0; }
    </style>
""", unsafe_allow_html=True)

# --- 4. LOGIN SCREEN (HERO VIEW) ---
if not st.session_state["authenticated"]:
    # Full-screen Hero Image with Login
    html_login = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Montserrat:wght@300;400;600&display=swap" rel="stylesheet">
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            :root {{ --bhhs-cabernet: #631D33; --overlay: rgba(0, 0, 0, 0.45); }}
            body, html {{ margin:0; padding:0; font-family:'Montserrat', sans-serif; overflow:hidden; width: 100vw; height: 100vh; }}
            .hero-container {{ position:relative; height:100vh; width:100vw; background-image: linear-gradient(var(--overlay), var(--overlay)), url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&q=80&w=2070'); background-size:cover; background-position:center; display:flex; flex-direction:column; align-items:center; justify-content:center; color:white; text-align:center; }}
            .disclaimer {{ font-size:12px; font-weight:bold; color:white; margin-top: 2rem; max-width: 800px; line-height: 1.4; }}
        </style>
    </head>
    <body>
        <section class="hero-container">
            <header class="absolute top-0 left-0 p-10">
                <div class="text-2xl font-bold font-serif tracking-tight">UTAH LAND & PROPERTY</div>
            </header>
            <div class="z-10 px-6 text-center flex flex-col items-center">
                <h1 class="text-7xl font-serif font-bold mb-2">Precision Acquisition.</h1>
                <p class="text-[0.9rem] uppercase tracking-[6px] mb-12 font-300">The Gold Standard in Utah Land Asset Strategy.</p>
                <div style="background: white; padding: 10px; border-radius: 4px; color: black;">
                    <p style="font-size: 10px; font-weight: bold; margin-bottom: 5px; color: #666;">ACQUISITION ID REQUIRED</p>
                </div>
            </div>
            <p class="disclaimer">Utah Land & Property Inc, are not licensed real estate agents or brokers. We are investment professionals. All activity is monitored and compliant with Utah regulations.</p>
        </section>
    </body>
    </html>
    """
    components.html(html_login, height=600)
    
    # Secure Login Input centered below the image
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        password_input = st.text_input("", type="password", placeholder="Enter Password to Unlock Vault")
        if password_input == SECRET_PASSWORD:
            st.session_state["authenticated"] = True
            st.rerun()

# --- 5. POST-LOGIN VAULT ---
else:
    # 1. Sidebar Printer Tray (Visible after login)
    with st.sidebar:
        st.header("🏔️ PRINTER TRAY")
        st.markdown("---")
        # Dynamic Date Selection via Calendar
        selected_date = st.date_input("Contract Effective Date", datetime.now())
        
        st.markdown("### Verify Details")
        f_n = st.text_input("Seller Name", value="Owen")
        f_a = st.text_input("Property Address")
        f_p = st.text_input("Parcel ID")
        f_t = st.text_area("Selected Docs (comma separated)")

        if st.button("GENERATE & DOWNLOAD PDF"):
            if f_n and f_a:
                deal_data = {
                    "seller_name": f_n,
                    "address": f_a,
                    "parcel_id": f_p,
                    "repc_date": selected_date.strftime("%m/%d/%Y"),
                    "addendum_no": "1"
                }
                try:
                    pdf_path = generate_utah_addendum(deal_data, [c.strip() for c in f_t.split(",")])
                    if pdf_path and os.path.exists(pdf_path):
                        with open(pdf_path, "rb") as f:
                            st.download_button("💾 SAVE REPC PDF", f, file_name=f"REPC_{f_n}.pdf")
                except Exception as e:
                    st.error(f"Mapping Error: {e}")

    # 2. Main Dashboard Content
    st.markdown("""
        <div style="padding: 4rem; background: #fcfcfc; min-height: 100vh;">
            <h1 style="font-family: 'Playfair Display'; color: #631D33;">Asset Acquisition Vault</h1>
            <p style="letter-spacing: 2px; font-size: 12px; color: #666;">SECURE TERMINAL | 2026 ACQUISITION CYCLE</p>
            <hr style="border: 0.5px solid #eee; margin: 2rem 0;">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px;">
                <div style="background: white; padding: 40px; border: 1px solid #e5e7eb; box-shadow: 0 4px 15px rgba(0,0,0,0.03);">
                    <h3 style="font-family: 'Playfair Display';">Status</h3>
                    <p style="color: green; font-weight: bold;">✓ LOGGED IN</p>
                    <p>Use the <b>Cabernet Sidebar</b> on the left to select the contract date and generate your REPC packet.</p>
                </div>
                <div style="background: white; padding: 40px; border: 1px solid #e5e7eb; box-shadow: 0 4px 15px rgba(0,0,0,0.03);">
                    <h3 style="font-family: 'Playfair Display';">Stochastic Prediction</h3>
                    <p>Winner Projection: <b>Ready for Execution</b></p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
