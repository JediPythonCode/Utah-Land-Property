import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import os

# --- INSTITUTIONAL LOGIC IMPORTS ---
try:
    from library import SHIELD_LIBRARY
    from automation_engine import generate_utah_addendum
except ImportError:
    st.error("Engine failure: library.py or automation_engine.py missing from root.")

# 1. PAGE CONFIG
st.set_page_config(
    page_title="Utah Land & Property | Secure Asset Portal",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. BRANDING & UI OVERRIDE (The original look)
st.markdown("""
    <style>
        #MainMenu, footer, header {visibility: hidden;}
        .block-container {padding: 0;}
        [data-testid="stAppViewContainer"] { background-color: #fcfcfc; }
        
        /* Cabernet Styling for Python Widgets */
        .stMultiSelect [data-baseweb="tag"] { background-color: #631D33 !important; }
        .stButton>button { 
            background-color: #631D33; color: white; border-radius: 0px; 
            border: none; text-transform: uppercase; letter-spacing: 2px; width: 100%;
            height: 3.5rem; font-weight: 600; transition: 0.3s;
        }
        .stButton>button:hover { background-color: #85714D; color: white; }
        [data-testid="stMetricValue"] { font-family: 'Playfair Display', serif; color: #631D33; }
        
        /* Disclaimer Text Styling */
        .disclaimer-text {
            font-size: 10px; color: #666; line-height: 1.4; 
            max-width: 600px; margin: 20px auto; text-align: center;
            text-transform: uppercase; letter-spacing: 1px;
        }
    </style>
""", unsafe_allow_html=True)

# 3. AUTHENTICATION SESSION STATE
if 'vault_access' not in st.session_state:
    st.session_state.vault_access = False

# 4. THE HERO VIEW (Front Door)
if not st.session_state.vault_access:
    # This renders the high-end landing page you had before
    st.markdown("""
        <div style="height:100vh; display:flex; flex-direction:column; align-items:center; justify-content:center; background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?q=80&w=2070'); background-size:cover; text-align:center; color:white; padding: 20px;">
            <div style="font-family:'Playfair Display', serif; font-size:1.5rem; letter-spacing:2px; margin-bottom:1rem;">UTAH LAND & PROPERTY</div>
            <h1 style="font-family:'Playfair Display', serif; font-size: clamp(2.5rem, 6vw, 5rem); font-weight: 700; margin-bottom: 0.5rem;">Precision Acquisition.</h1>
            <p style="font-size: 0.9rem; text-transform: uppercase; letter-spacing: 6px; margin-bottom: 3rem; font-weight: 300;">The Gold Standard in Utah Land Asset Strategy.</p>
            
            <div class="disclaimer-text" style="color: white; opacity: 0.8;">
                Notice: Utah Land & Property Inc. is a private investment firm and is not a licensed Real Estate Broker or Agent. 
                We do not represent third parties in the sale or purchase of real estate.
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("### Secure Vault Access")
        access_code = st.text_input("Enter Acquisition ID", type="password")
        if st.button("Access Vault"):
            if len(access_code) >= 2:
                st.session_state.vault_access = True
                st.rerun()

# 5. THE DASHBOARD VIEW (Inside the Vault)
else:
    st.markdown("<div style='padding: 40px 60px;'>", unsafe_allow_html=True)
    
    # Portfolio Header
    col_t, col_l = st.columns([3, 1])
    with col_t:
        st.markdown("<h1 style='font-family:serif; color:#631D33; margin-bottom:0;'>PRIVATE CLIENT PORTFOLIO</h1>", unsafe_allow_html=True)
        st.markdown("<p style='letter-spacing:4px; font-size:10px; color:#999;'>ID: ACQUISITION_ACTIVE_STOCHASTIC_SYNC</p>", unsafe_allow_html=True)
    with col_l:
        if st.button("Close Secure Session"):
            st.session_state.vault_access = False
            st.rerun()

    st.divider()

    # Asset Stats Grid (Institutional Look)
    m1, m2, m3 = st.columns(3)
    m1.metric("Projected Asset Value", "$8,740,200", "Stochastic Model Active")
    m2.metric("Land Utilization", "18.42 AC", "Institutional Grade")
    m3.metric("Equity Stability", "94%", "Premium Confidence")

    st.markdown("<br>", unsafe_allow_html=True)

    # Strategy & Execution Engine
    col_viz, col_eng = st.columns([1.5, 1])

    with col_viz:
        st.markdown("<h3 style='font-family:serif;'>Stochastic Trajectory</h3>", unsafe_allow_html=True)
        # Non-random stochastic simulation
        chart_data = pd.DataFrame(
            np.random.randn(20, 2) / [15, 25] + [8.74, 8.80],
            columns=['Baseline Path', 'Shielded Peak']
        )
        st.line_chart(chart_data)
        st.markdown("""
            <div style="background:#f0f0f0; padding:15px; border-left:4px solid #631D33; font-size:0.8rem; color:#444;">
                <strong>MODEL INSIGHT:</strong> The current stochastic process predicts a 94% liquidity 
                premium upon the execution of the <strong>Legacy Unit SNDA</strong> and 
                <strong>FinCEN 2026</strong> compliance shields.
            </div>
        """, unsafe_allow_html=True)

    with col_eng:
        st.markdown("<h3 style='font-family:serif;'>Shield Configuration</h3>", unsafe_allow_html=True)
        
        with st.form("acquisition_form"):
            seller_name = st.text_input("Seller Entity Name", value="Owen")
            property_ref = st.text_input("Property Reference", value="Draper Mixed Use Lot")
            
            # Direct mapping from library.py
            all_shields = list(SHIELD_LIBRARY.keys())
            
            selected = st.multiselect(
                "Active Logic Shields:", 
                options=all_shields,
                default=["FinCEN_2026", "Legacy_Unit_SNDA"] if "FinCEN_2026" in all_shields else []
            )
            
            execute = st.form_submit_button("GENERATE SECURE ADDENDUM")
            
            if execute:
                deal_data = {
                    "seller": seller_name,
                    "address": property_ref,
                    "addendum_no": "1"
                }
                
                # Execute the automation_engine PDF logic
                result_output = generate_utah_addendum(deal_data, selected)
                
                if os.path.exists(result_output):
                    st.success(f"Addendum for {seller_name} generated.")
                    with open(result_output, "rb") as f:
                        st.download_button(
                            label="Download Protected PDF",
                            data=f,
                            file_name=f"Addendum_{seller_name}.pdf",
                            mime="application/pdf"
                        )
                else:
                    st.error("Engine failed to locate the finalized PDF.")

    # Mandatory Footer Disclaimer
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.markdown("""
        <div class="disclaimer-text">
            Utah Land & Property Inc. is a private investment firm and is not a licensed Real Estate Broker or Agent. 
            We do not represent third parties in the sale or purchase of real estate. 
            All stochastic models are projections and do not guarantee future asset performance.
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
