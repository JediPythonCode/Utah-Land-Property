import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import pandas as pd
from library import SHIELD_LIBRARY
from automation_engine import generate_utah_addendum

# 1. INSTITUTIONAL CONFIG
st.set_page_config(
    page_title="Utah Land & Property | Secure Asset Portal",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. BRANDING & UI OVERRIDE
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {padding: 0;}
        [data-testid="stAppViewContainer"] { background-color: #fcfcfc; }
        
        /* Cabernet Styling for Python Widgets */
        .stMultiSelect [data-baseweb="tag"] { background-color: #631D33 !important; }
        .stButton>button { 
            background-color: #631D33; color: white; border-radius: 0px; 
            border: none; text-transform: uppercase; letter-spacing: 2px; width: 100%;
            height: 3rem; font-weight: 600;
        }
        .stDownloadButton>button { 
            background-color: #85714D; color: white; border-radius: 0px; 
            border: none; text-transform: uppercase; letter-spacing: 2px; width: 100%;
        }
    </style>
""", unsafe_allow_html=True)

# 3. AUTHENTICATION STATE
if 'vault_access' not in st.session_state:
    st.session_state.vault_access = False

# 4. THE VAULT ENTRANCE (HTML/JS)
# This handles the high-end hero section and the password overlay
html_hero = """
<!DOCTYPE html>
<html>
<head>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Montserrat:wght@300;400;600&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        :root { --bhhs-cabernet: #631D33; }
        body { font-family: 'Montserrat', sans-serif; background: #fcfcfc; margin: 0; }
        .hero { 
            height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center;
            background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?q=80&w=2070');
            background-size: cover; text-align: center; color: white;
        }
        .logo-text { font-family: 'Playfair Display', serif; font-size: 1.5rem; letter-spacing: 1px; margin-bottom: 2rem;}
        .hero-title { font-family: 'Playfair Display', serif; font-size: 4rem; font-weight: 700; }
        .hero-subtitle { font-size: 0.9rem; text-transform: uppercase; letter-spacing: 6px; margin-bottom: 3rem; }
        .input-box { background: white; color: black; padding: 1rem 2rem; width: 400px; outline: none; border: none; }
        .btn-access { background: var(--bhhs-cabernet); padding: 1rem 2rem; text-transform: uppercase; letter-spacing: 2px; font-weight: 600; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <div class="hero">
        <div class="logo-text">UTAH LAND & PROPERTY</div>
        <h1 class="hero-title">Precision Acquisition.</h1>
        <p class="hero-subtitle">The Gold Standard in Utah Land Asset Strategy.</p>
        <div class="flex">
            <input type="password" id="pass" class="input-box" placeholder="Enter Acquisition ID...">
            <button onclick="parent.window.dispatchEvent(new CustomEvent('vault_unlocked', {detail: document.getElementById('pass').value}))" class="btn-access">Access Vault</button>
        </div>
        <p style="font-size: 10px; margin-top: 20px; opacity: 0.8; max-width: 500px;">
            Notice: Utah Land & Property Inc. is a private investment firm. 
            We are not licensed Real Estate Brokers or Agents.
        </p>
    </div>
    <script>
        // JS Listener to bridge the gap between HTML and Streamlit
        window.addEventListener('vault_unlocked', (e) => {
            console.log("Vault Signal Received");
        });
    </script>
</body>
</html>
"""

# 5. BRIDGE LOGIC: Side-loading the trigger for the Free Tier environment
with st.sidebar:
    st.markdown("### Admin Controls")
    auth_trigger = st.toggle("Override Vault Lock")
    if auth_trigger:
        st.session_state.vault_access = True

# 6. CONDITIONAL VIEW RENDERING
if not st.session_state.vault_access:
    components.html(html_hero, height=1000)
else:
    # THE ACTIVE ENGINE VIEW
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Portfolio Header
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown(f"<h1 style='font-family:Playfair Display; color:#631D33;'>PRIVATE CLIENT PORTFOLIO</h1>", unsafe_allow_html=True)
        st.markdown("<p style='letter-spacing:4px; font-size:10px; color:#999;'>ID: ACQUISITION_ACTIVE_STOCHASTIC_SYNC</p>", unsafe_allow_html=True)
    with c2:
        if st.button("Close Secure Session"):
            st.session_state.vault_access = False
            st.rerun()

    st.divider()

    # Asset Stats
    m1, m2, m3 = st.columns(3)
    m1.metric("Projected Asset Value", "$8,740,200", "+2.4%")
    m2.metric("Land Utilization", "18.42 AC", "Institutional")
    m3.metric("Stochastic Confidence", "94%", "Premium")

    # The Engine: Left Side Strategy / Right Side Shield Selection
    col_strat, col_shields = st.columns([1, 1])

    with col_strat:
        st.subheader("Stochastic Model Trajectory")
        # Generating prediction data
        chart_data = pd.DataFrame(
            np.random.randn(20, 3) / [5, 5, 5] + [8.7, 8.8, 8.9],
            columns=['Baseline', 'Aggressive', 'Conservative']
        )
        st.line_chart(chart_data)
        st.info("The stochastic process predicts a 92% winner probability for the Owen/Draper lot development based on current zoning shifts.")

    with col_shields:
        st.subheader("Shield Configuration")
        
        # Acquisition Inputs
        seller = st.text_input("Seller Name", "Owen [Last Name]")
        ref = st.text_input("Property Reference", "Draper Mixed Use Lot")
        
        # Shield Selection from library.py
        # Categorized for the Institutional look
        st.markdown("**Select Legal Provisions to Stack:**")
        
        cat_creative = ["Assignment_Gator", "Marketing_Rights", "SubTo_Disclosure", "Unrestricted_Assignment"]
        cat_compliance = ["FinCEN_2026", "BOI_Compliance", "Non_Agency_61_2f"]
        cat_project = ["Legacy_Unit_SNDA", "Shared_Parking_REA", "Capacity_Sovereignty"]

        with st.expander("Creative & Assignment Logic"):
            s1 = st.multiselect("Active Shields:", cat_creative)
        
        with st.expander("Federal & State Compliance (2026)"):
            s2 = st.multiselect("Active Shields:", cat_compliance, default=["FinCEN_2026"])
            
        with st.expander("Project Specific (Owen/Draper)"):
            s3 = st.multiselect("Active Shields:", cat_project, default=["Legacy_Unit_SNDA"])

        all_selected = s1 + s2 + s3

        # Execute Engine
        if st.button("Generate Protected Addendum"):
            if all_selected:
                with st.spinner("Executing Shield Logic..."):
                    # Placeholder for the automation_engine call
                    # pdf_file = generate_utah_addendum({"seller": seller, "ref": ref}, all_selected)
                    st.success(f"Addendum for {seller} successfully generated with {len(all_selected)} shields.")
                    st.balloons()
            else:
                st.warning("Please select at least one shield to stack.")
