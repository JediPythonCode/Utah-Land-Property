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

# ---> CUSTOM STYLING & CLEAN LAYOUT (ZILLOW UI + HIGH-END GAMING HUD / CYBERPUNK EXECUTIVE MOTIF) <---
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Inter:wght@400;500;600;700;800&family=Playfair+Display:wght@700;900&display=swap');

        /* Hide Streamlit Header, Menu, and Footer */
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display:none;}

        .stApp {
            background-color: #0b0f19;
            color: #f3f4f6;
            font-family: "Inter", -apple-system, BlinkMacSystemFont, sans-serif;
        }

        .main-header {
            background: linear-gradient(rgba(11, 15, 25, 0.75), rgba(11, 15, 25, 0.75)), 
                        url('https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=2400&q=80');
            background-size: cover;
            background-position: center;
            padding: 100px 20px;
            text-align: center;
            color: white;
            border-radius: 12px;
            margin-bottom: 30px;
            border: 1px solid rgba(0, 242, 254, 0.2);
            box-shadow: 0 0 40px rgba(0, 242, 254, 0.15), inset 0 0 20px rgba(0, 242, 254, 0.05);
        }

        .main-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 56px;
            font-weight: 900;
            margin-bottom: 15px;
            letter-spacing: 1px;
            color: #ffffff;
            text-shadow: 0 0 20px rgba(0, 242, 254, 0.6), 0 0 40px rgba(0, 242, 254, 0.3);
            background: linear-gradient(90deg, #ffffff, #00f2fe);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .main-subtitle {
            font-size: 18px;
            font-weight: 500;
            max-width: 900px;
            margin: 0 auto 8px auto;
            color: #cbd5e1;
            text-shadow: 0 2px 4px rgba(0,0,0,0.6);
        }

        .section-header {
            font-family: 'Orbitron', sans-serif;
            font-size: 1.8rem;
            font-weight: 700;
            color: #00f2fe;
            margin: 45px 0 15px 0;
            padding-bottom: 10px;
            border-bottom: 2px solid rgba(0, 242, 254, 0.3);
            letter-spacing: 0.5px;
            text-shadow: 0 0 10px rgba(0, 242, 254, 0.2);
        }

        /* Zillow UI Style Listing Cards with High-End Cyber Gaming HUD Accents (NO CARD IMAGES) */
        .zillow-card {
            background: #131b2e;
            border: 1px solid rgba(0, 242, 254, 0.2);
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.4);
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .zillow-card:hover {
            box-shadow: 0 0 25px rgba(0, 242, 254, 0.35);
            border-color: #00f2fe;
            transform: translateY(-3px);
        }

        .price-tag {
            font-family: 'Orbitron', sans-serif;
            font-size: 24px;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 6px;
            text-shadow: 0 0 10px rgba(255, 255, 255, 0.2);
        }

        .card-meta {
            font-size: 14px;
            color: #94a3b8;
            margin-bottom: 12px;
            font-weight: 500;
            line-height: 1.5;
        }

        .card-location {
            font-size: 13px;
            color: #64748b;
            margin-bottom: 14px;
        }

        .badge-available {
            background-color: rgba(6, 95, 70, 0.4);
            color: #34d399;
            border: 1px solid rgba(52, 211, 153, 0.3);
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .badge-contract {
            background-color: rgba(159, 18, 57, 0.4);
            color: #fb7185;
            border: 1px solid rgba(251, 113, 133, 0.3);
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        /* Cinematic Inter-Category Banner Styles */
        .category-banner {
            position: relative;
            border-radius: 10px;
            overflow: hidden;
            margin: 30px 0 10px 0;
            border: 1px solid rgba(0, 242, 254, 0.3);
            box-shadow: 0 4px 25px rgba(0,0,0,0.5);
        }
        .category-banner img {
            width: 100%;
            height: 220px;
            object-fit: cover;
            display: block;
            filter: brightness(0.65) contrast(1.1);
        }
        .category-banner-text {
            position: absolute;
            bottom: 20px;
            left: 25px;
            color: #ffffff;
            font-family: 'Orbitron', sans-serif;
            font-size: 24px;
            font-weight: 700;
            text-shadow: 0 2px 8px rgba(0,0,0,0.8);
            letter-spacing: 0.5px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---> AUTHENTICATION SESSION STATE SETUP <---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# ---> MAIN HEADER SECTION <---
st.markdown(
    """
    <div class="main-header">
        <div class="main-title">UTAH LAND & PROPERTY INC.</div>
        <div class="main-subtitle">TACTICAL REAL ESTATE CONTRACT ASSIGNMENTS & EQUITABLE INTEREST OPERATIONS</div>
        <div class="main-subtitle" style="font-size: 14px; color: #94a3b8; margin-top: 10px;">[SYSTEM NOTICE]: We are not brokers. We market our verified equitable interest in signed purchase contracts.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---> INVESTOR LOGIN GATEWAY <---
if not st.session_state["authenticated"]:
    st.markdown("### 🔒 Secure Tactical Investor Access Portal")
    st.markdown("Please enter your verified investor credentials to unlock off-market asset streams.")
    
    with st.form("login_form"):
        investor_email = st.text_input("Investor Email")
        secret_code = st.text_input("Secret Access Code", type="password")
        submit_login = st.form_submit_button("Authenticate & Initialize Portal")
        
        if submit_login:
            configured_email = st.secrets.get("INVESTOR_EMAIL", "douglas@utahlandproperty.com")
            configured_secret = st.secrets.get("INVESTOR_SECRET", "UTAH2026!")
            
            if investor_email.strip().lower() == configured_email.lower() and secret_code == configured_secret:
                st.session_state["authenticated"] = True
                st.success("Access Granted! Initializing HUD...")
                st.rerun()
            else:
                st.error("Authentication Failed: Invalid credentials.")
    
    st.stop()

# ---> SIDEBAR CONTROLS <---
st.sidebar.title("🎮 HUD Control Matrix")
category_filter = st.sidebar.selectbox("Filter Asset Sector", ["All", "Residential", "Raw Land", "Commercial"])
status_filter = st.sidebar.selectbox("Contract Status", ["All", "Available", "UNDER CONTRACT"])
st.sidebar.markdown("---")
st.sidebar.info("STATUS: SECURE 🟢\nOPERATOR: CEO / ADMIN\nSYSTEM: ACTIVE")

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

# ---> RENDER SECTIONS WITH CINEMATIC BETWEEN-CATEGORY IMAGES <---
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
                <img src="{category_banners[cat]}" alt="{cat} Sector">
                <div class="category-banner-text">SECTOR // {cat.upper()} ASSETS</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(f'<div class="section-header">⚡ {cat} Contract Assignments</div>', unsafe_allow_html=True)
    
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
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                            <div class="price-tag">${item['contract_price']:,} <span style="font-size: 12px; font-weight: 400; color: #64748b; font-family: 'Inter', sans-serif;">Fee</span></div>
                            <div>{badge_html}</div>
                        </div>
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
