from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import re
import smtplib
import pandas as pd
import pydeck as pdk
import streamlit as st

# ---> PAGE CONFIGURATION <---
st.set_page_config(
    page_title="Utah Land & Property Inc.",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---> CUSTOM STYLING: LIGHT APP BACKGROUND & ENLARGED LOGIN TEXT PANES <---
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Inter:wght@400;500;600;700;800&family=Playfair+Display:wght@700;900&display=swap');

        /* Hide Streamlit Header, Menu, and Footer */
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display:none;}

        /* Overall App Background: LIGHT */
        .stApp {
            background-color: #f8fafc;
            color: #1e293b;
            font-family: "Inter", -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* --- STICKY DUAL-PANEL BERKSHIRE-STYLE LOGIN GATEWAY (LARGER & EXPANDED) --- */
        .login-outer-wrapper {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 90vh;
            padding: 30px;
        }

        .berkshire-sticky-card {
            display: flex;
            width: 100%;
            max-width: 1100px;
            background-color: #ffffff;
            border: 1px solid #cbd5e1;
            border-radius: 12px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.18);
            overflow: hidden;
            color: #111827;
        }

        .berkshire-login-image-pane {
            flex: 1.2;
            background: linear-gradient(rgba(15, 23, 42, 0.55), rgba(15, 23, 42, 0.88)), 
                        url('https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=1200&q=80');
            background-size: cover;
            background-position: center;
            padding: 50px 45px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            color: #ffffff;
        }

        .berkshire-login-image-top h3 {
            font-family: 'Playfair Display', serif;
            font-size: 30px;
            font-weight: 700;
            margin-bottom: 14px;
            line-height: 1.3;
            text-shadow: 0 2px 4px rgba(0,0,0,0.8);
        }

        .berkshire-login-image-top p {
            font-size: 16px;
            color: #e2e8f0;
            line-height: 1.6;
            text-shadow: 0 1px 3px rgba(0,0,0,0.8);
        }

        .berkshire-login-image-bottom {
            margin-top: 30px;
            border-top: 1px solid rgba(255, 255, 255, 0.2);
            padding-top: 20px;
        }

        .berkshire-login-form-pane {
            flex: 1.3;
            padding: 50px 50px;
            background-color: #ffffff;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        .berkshire-brand-header {
            text-align: center;
            margin-bottom: 25px;
            border-bottom: 2px solid #1e3a8a;
            padding-bottom: 18px;
        }

        .berkshire-brand-header h1 {
            font-family: 'Playfair Display', serif;
            font-size: 32px;
            font-weight: 900;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            color: #1e3a8a;
            margin-bottom: 6px;
        }

        .berkshire-brand-header p {
            font-size: 13px;
            color: #3b82f6;
            letter-spacing: 0.15em;
            text-transform: uppercase;
            font-weight: 700;
        }

        /* --- DASHBOARD STYLING --- */
        .main-header {
            background: linear-gradient(rgba(30, 58, 138, 0.85), rgba(30, 58, 138, 0.92)), 
                        url('https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=2400&q=80');
            background-size: cover;
            background-position: center;
            padding: 80px 20px;
            text-align: center;
            color: white;
            border-radius: 12px;
            margin-bottom: 30px;
            border: 1px solid #cbd5e1;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        }

        .main-title {
            font-family: 'Playfair Display', serif;
            font-size: 46px;
            font-weight: 900;
            margin-bottom: 15px;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            color: #ffffff;
        }

        .main-subtitle {
            font-size: 16px;
            font-weight: 500;
            max-width: 900px;
            margin: 0 auto 8px auto;
            color: #e2e8f0;
            text-align: center;
            font-family: 'Inter', sans-serif;
        }

        .section-header {
            font-family: 'Playfair Display', serif;
            font-size: 2.2rem;
            font-weight: 700;
            color: #1e3a8a;
            margin: 45px 0 20px 0;
            padding-bottom: 10px;
            border-bottom: 2px solid #cbd5e1;
            letter-spacing: 0.02em;
            text-align: center;
        }

        /* Zillow UI Style Listing Cards: Dark Background, White Lettering, Centered Content */
        .zillow-card {
            background: #0f172a;
            border: 1px solid #334155;
            border-radius: 10px;
            padding: 24px 20px;
            margin-bottom: 20px;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
            text-align: center;
            color: #ffffff;
            transition: all 0.2s ease-in-out;
        }

        .zillow-card:hover {
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.25);
            border-color: #64748b;
            transform: translateY(-2px);
        }

        .price-tag {
            font-family: 'Inter', sans-serif;
            font-size: 24px;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 8px;
        }

        .card-meta {
            font-size: 14px;
            color: #cbd5e1;
            margin-bottom: 12px;
            font-weight: 400;
            line-height: 1.6;
            font-family: 'Inter', sans-serif;
        }

        .card-location {
            font-size: 13px;
            color: #94a3b8;
            margin-bottom: 16px;
            font-family: 'Inter', sans-serif;
        }

        .badge-available {
            background-color: rgba(6, 95, 70, 0.6);
            color: #34d399;
            border: 1px solid rgba(52, 211, 153, 0.4);
            padding: 4px 12px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            display: inline-block;
            margin-bottom: 10px;
            font-family: 'Inter', sans-serif;
        }

        .badge-contract {
            background-color: rgba(159, 18, 57, 0.6);
            color: #fb7185;
            border: 1px solid rgba(251, 113, 133, 0.4);
            padding: 4px 12px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            display: inline-block;
            margin-bottom: 10px;
            font-family: 'Inter', sans-serif;
        }

        /* Center Streamlit buttons inside columns */
        .stButton {
            display: flex;
            justify-content: center;
        }
        .stButton > button {
            width: 100%;
            background-color: #1e293b;
            color: #ffffff;
            border: 1px solid #475569;
            font-weight: 500;
            border-radius: 6px;
            padding: 8px 16px;
            font-family: 'Inter', sans-serif;
        }
        .stButton > button:hover {
            background-color: #334155;
            border-color: #94a3b8;
            color: #ffffff;
        }

        /* Cinematic Inter-Category Banner Styles */
        .category-banner {
            position: relative;
            border-radius: 12px;
            overflow: hidden;
            margin: 45px 0 15px 0;
            border: 1px solid #cbd5e1;
            box-shadow: 0 6px 20px rgba(0,0,0,0.1);
        }
        .category-banner img {
            width: 100%;
            height: 240px;
            object-fit: cover;
            display: block;
            filter: brightness(0.65) contrast(1.05);
        }
        .category-banner-text {
            position: absolute;
            bottom: 25px;
            left: 0;
            right: 0;
            text-align: center;
            color: #ffffff;
            font-family: 'Playfair Display', serif;
            font-size: 32px;
            font-weight: 700;
            text-shadow: 0 2px 8px rgba(0,0,0,0.9);
            letter-spacing: 0.03em;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---> AUTHENTICATION SESSION STATE SETUP <---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# ---> INVESTOR LOGIN GATEWAY (STICKY DUAL-PANEL BERKSHIRE HATHAWAY STYLE) <---
if not st.session_state["authenticated"]:
    st.markdown(
        """
        <div class="login-outer-wrapper">
            <div class="berkshire-sticky-card">
                <div class="berkshire-login-image-pane">
                    <div class="berkshire-login-image-top">
                        <h3>Uncompromising Integrity. Exceptional Value.</h3>
                        <p>Welcome to the Utah Land & Property executive investment portal. Dedicated to precision contract acquisitions, asset transparency, and long-term equity growth.</p>
                    </div>
                    <div class="berkshire-login-image-bottom">
                        <div id="portal-disclaimer" style="font-size: 11px; color: #cbd5e1; line-height: 1.5; border-left: 3px solid #38bdf8; padding-left: 10px; background-color: rgba(15, 23, 42, 0.6); padding-top: 6px; padding-bottom: 6px; border-radius: 0 4px 4px 0; margin-bottom: 12px;">
                            <strong>Disclosures:</strong> Utah Land & Property Inc. is a principal contract holder and is marketing the assignment of a legal purchase agreement. We are not licensed real estate agents or brokerages and do not represent the property owner. We are not selling the real property itself. Pursuant to Utah Code § 61-2f-202 and applicable statutory exemptions, transactions are executed as direct principal equitable interest assignments.
                        </div>
                        <div style="text-align: center; font-size: 11px; color: #94a3b8; line-height: 1.4;">
                            &copy; 2026 Utah Land & Property Inc. All rights reserved.<br>Protected by advanced encryption protocols.
                        </div>
                    </div>
                </div>
                <div class="berkshire-login-form-pane">
                    <div class="berkshire-brand-header">
                        <h1>Utah Land & Property</h1>
                        <p>Executive Investor Secure Portal</p>
                    </div>
        """,
        unsafe_allow_html=True,
    )
    
    with st.form("login_form"):
        st.markdown(
            """
            <div style="font-size: 12px; font-weight: 700; text-transform: uppercase; color: #374151; margin-bottom: 6px; letter-spacing: 0.05em;">
                Corporate Identifier / Email
            </div>
            """,
            unsafe_allow_html=True
        )
        investor_email = st.text_input("Investor Email", label_visibility="collapsed", placeholder="investor@utahlandproperty.com")
        
        st.markdown(
            """
            <div style="font-size: 12px; font-weight: 700; text-transform: uppercase; color: #374151; margin: 16px 0 6px 0; letter-spacing: 0.05em;">
                Security Password
            </div>
            """,
            unsafe_allow_html=True
        )
        secret_code = st.text_input("Security Password", type="password", label_visibility="collapsed", placeholder="••••••••••••")
        
        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
        submit_login = st.form_submit_button("Authenticate Securely", use_container_width=True)
        
        if submit_login:
            configured_email = st.secrets.get("INVESTOR_EMAIL", "douglas@utahlandproperty.com")
            configured_secret = st.secrets.get("INVESTOR_SECRET", "UTAH2026!")
            
            if investor_email.strip().lower() == configured_email.lower() and secret_code == configured_secret:
                st.session_state["authenticated"] = True
                st.success("Access Granted! Initializing HUD...")
                st.rerun()
            else:
                st.error("Authentication Failed: Invalid corporate credentials.")
    
    st.markdown(
        """
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

# ---> SIDEBAR CONTROLS <---
st.sidebar.title("Investor Menu")
category_filter = st.sidebar.selectbox("Filter Asset Sector", ["All", "Residential", "Raw Land", "Commercial"])
status_filter = st.sidebar.selectbox("Contract Status", ["All", "Available", "UNDER CONTRACT"])
st.sidebar.markdown("---")
st.sidebar.info("Portal Status: Secure\nOperator: Executive Admin\nSystem: Active")

# ---> MAIN HEADER SECTION <---
st.markdown(
    """
    <div class="main-header">
        <div class="main-title">Utah Land & Property Inc.</div>
        <div class="main-subtitle" style="font-size: 16px; font-weight: 500; letter-spacing: 0.02em; margin-bottom: 12px;">Verified Contract Assignments & Equitable Interest Portfolio</div>
        <div class="main-subtitle" style="font-size: 11px; color: #cbd5e1; margin-top: 15px; line-height: 1.5; max-width: 800px; margin-left: auto; margin-right: auto;">[Notice]: Acting as principal contract holder marketing equitable interests. Pursuant to Utah Code § 61-2f-202 and statutory exemptions, transactions are executed as direct principal assignments.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---> DATABASE GENERATOR <---
@st.cache_data
def load_utah_property_database():
    data = []
    statuses = ["Available", "UNDER CONTRACT"]
    
    # Generate 32 Residential Listings
    for i in range(1, 33):
        purchase_price = 150000 + (i * 12500)
        arv = int(purchase_price * 1.3)
        contract_price = 5000 + (i * 300)
        data.append({
            "id": f"RES-{1000+i}",
            "title": f"Equitable Interest Purchase Contract Assignment",
            "category": "Residential",
            "location": "Millcreek, UT 84117",
            "contract_price": contract_price,
            "purchase_price": purchase_price,
            "arv": arv,
            "status": statuses[i % 2],
            "lat": 40.6900 + (i * 0.001),
            "lon": -111.8500 - (i * 0.001)
        })

    # Generate 32 Raw Land Listings
    for i in range(1, 33):
        purchase_price = 45000 + (i * 4500)
        arv = int(purchase_price * 1.35)
        contract_price = 4000 + (i * 200)
        data.append({
            "id": f"LAND-{2000+i}",
            "title": f"Land Parcel Purchase Contract Assignment",
            "category": "Raw Land",
            "location": "Elko County, NV 89801",
            "contract_price": contract_price,
            "purchase_price": purchase_price,
            "arv": arv,
            "status": statuses[(i + 1) % 2],
            "lat": 41.5000 + (i * 0.001),
            "lon": -115.5000 - (i * 0.001)
        })

    # Generate 32 Commercial Listings
    for i in range(1, 33):
        purchase_price = 280000 + (i * 18000)
        arv = int(purchase_price * 1.28)
        contract_price = 12000 + (i * 500)
        data.append({
            "id": f"COMM-{3000+i}",
            "title": f"Commercial Purchase Contract Assignment",
            "category": "Commercial",
            "location": "Draper, UT 84020",
            "contract_price": contract_price,
            "purchase_price": purchase_price,
            "arv": arv,
            "status": statuses[i % 2],
            "lat": 40.5200 + (i * 0.001),
            "lon": -111.8600 - (i * 0.001)
        })

    return data

database = load_utah_property_database()

# ---> RENDER SECTIONS WITH CINEMATIC BETWEEN-CATEGORY IMAGES & CLEAN HEADERS <---
categories_to_show = ["Residential", "Raw Land", "Commercial"] if category_filter == "All" else [category_filter]

# Banner image URLs mapped to category themes
category_banners = {
    "Residential": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=2000&q=80",
    "Raw Land": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=2000&q=80",
    "Commercial": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=2000&q=80"
}

for cat in categories_to_show:
    # Cinematic Category Image Banner
    if cat in category_banners:
        st.markdown(
            f"""
            <div class="category-banner">
                <img src="{category_banners[cat]}" alt="{cat} Assets">
                <div class="category-banner-text">{cat} Contract Assignments</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(f'<div class="section-header">{cat} Contract Assignments</div>', unsafe_allow_html=True)
    
    cat_items = [item for item in database if item["category"] == cat]
    if status_filter != "All":
        cat_items = [item for item in cat_items if item["status"] == status_filter]
        
    for i in range(0, len(cat_items), 3):
        row_items = cat_items[i:i+3]
        cols = st.columns(len(row_items))
        for idx, item in enumerate(row_items):
            with cols[idx]:
                badge_html = f'<span class="badge-available">{item["status"]}</span>' if item["status"] == "Available" else f'<span class="badge-contract">{item["status"]}</span>'
                
                st.markdown(
                    f"""
                    <div class="zillow-card">
                        <div>{badge_html}</div>
                        <div class="price-tag">${item['contract_price']:,} <span style="font-size: 12px; font-weight: 400; color: #94a3b8; font-family: 'Inter', sans-serif;">Fee</span></div>
                        <div class="card-meta">
                            <b>Underlying Price:</b> ${item['purchase_price']:,}<br>
                            <b>Target ARV:</b> ${item['arv']:,}
                        </div>
                        <div class="card-location">
                            📍 <b>{item['location']}</b> &nbsp;|&nbsp; <code>{item['id']}</code>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                if st.button("Unlock Package", key=f"btn_{item['id']}"):
                    st.success(f"Accessing secure dossier for asset {item['id']}")
