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

# ---> CUSTOM STYLING & CLEAN LAYOUT (ZILLOW UI INSPIRATION + HIDE STREAMLIT CHROME & HOUSING CARD IMAGES) <---
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Playfair+Display:wght@700;900&display=swap');

        /* Hide Streamlit Header, Menu, and Footer */
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display:none;}

        .stApp {
            background-color: #f7f8fa;
            color: #2c3e50;
            font-family: "Inter", -apple-system, BlinkMacSystemFont, sans-serif;
        }

        .main-header {
            background: linear-gradient(rgba(0, 0, 0, 0.45), rgba(0, 0, 0, 0.45)), 
                        url('https://images.unsplash.com/photo-1564013799919-ab600027ffc6?auto=format&fit=crop&w=2000&q=80');
            background-size: cover;
            background-position: center;
            padding: 70px 20px;
            text-align: center;
            color: white;
            border-radius: 10px;
            margin-bottom: 25px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }

        .main-title {
            font-family: 'Playfair Display', Georgia, serif;
            font-size: 42px;
            font-weight: 900;
            margin-bottom: 10px;
            letter-spacing: -0.5px;
            text-shadow: 0 3px 6px rgba(0,0,0,0.4);
        }

        .main-subtitle {
            font-size: 16px;
            font-weight: 500;
            max-width: 800px;
            margin: 0 auto 6px auto;
            text-shadow: 0 2px 4px rgba(0,0,0,0.4);
        }

        .section-header {
            font-family: 'Inter', sans-serif;
            font-size: 1.5rem;
            font-weight: 700;
            color: #1a1a1a;
            margin: 35px 0 15px 0;
            padding-bottom: 8px;
            border-bottom: 2px solid #006aff;
        }

        /* Zillow UI Style Listing Cards (Clean, Modern Border, No Card Images) */
        .zillow-card {
            background: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 18px;
            margin-bottom: 20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
            transition: all 0.2s ease-in-out;
        }

        .zillow-card:hover {
            box-shadow: 0 8px 25px rgba(0,0,0,0.08);
            border-color: #cbd5e1;
            transform: translateY(-2px);
        }

        .price-tag {
            font-size: 22px;
            font-weight: 800;
            color: #1a1a1a;
            margin-bottom: 4px;
        }

        .card-meta {
            font-size: 14px;
            color: #4b5563;
            margin-bottom: 10px;
            font-weight: 500;
        }

        .card-location {
            font-size: 13px;
            color: #6b7280;
            margin-bottom: 12px;
        }

        .badge-available {
            background-color: #ecfdf5;
            color: #065f46;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .badge-contract {
            background-color: #fff1f2;
            color: #9f1239;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
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
        <div class="main-title">Utah Land & Property Inc.</div>
        <div class="main-subtitle">Wholesale Real Estate Contract Assignments & Equitable Interest Opportunities</div>
        <div class="main-subtitle" style="font-size: 14px; opacity: 0.85;">We are not real estate agents or brokers. We market our equitable interest in signed purchase contracts.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---> INVESTOR LOGIN GATEWAY <---
if not st.session_state["authenticated"]:
    st.markdown("### 🔒 Investor Portfolio Access Portal")
    st.markdown("Please enter your verified investor email and secure access code to unlock off-market contract assignment details.")
    
    with st.form("login_form"):
        investor_email = st.text_input("Investor Email")
        secret_code = st.text_input("Secret Access Code", type="password")
        submit_login = st.form_submit_button("Authenticate & View Contracts")
        
        if submit_login:
            if investor_email.strip() != "" and secret_code == "UTAH2026!":
                st.session_state["authenticated"] = True
                st.success("Authentication successful! Loading contract assignments...")
                st.rerun()
            else:
                st.error("Invalid credentials. Please enter a valid email and correct secret code.")
    
    st.stop()

# ---> SIDEBAR FILTERS & CONTROLS <---
st.sidebar.title("Navigation & Filters")
category_filter = st.sidebar.selectbox("Filter by Category", ["All", "Residential", "Raw Land", "Commercial"])
status_filter = st.sidebar.selectbox("Contract Status", ["All", "Available", "UNDER CONTRACT"])
st.sidebar.markdown("---")
st.sidebar.info("Logged in as Verified Investor.\nUtah Land & Property Inc. Portfolio Manager.")

# ---> DATABASE GENERATOR (32 LISTINGS PER CATEGORY, ZILLOW UI CLEAN STYLE, NO CARD IMAGES) <---
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

# ---> RENDER SECTIONS <---
categories_to_show = ["Residential", "Raw Land", "Commercial"] if category_filter == "All" else [category_filter]

for cat in categories_to_show:
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
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                            <div class="price-tag">${item['contract_price']:,} <span style="font-size: 13px; font-weight: 400; color: #6b7280;">Assignment Fee</span></div>
                            <div>{badge_html}</div>
                        </div>
                        <div class="card-meta">
                            <b>Underlying Purchase Price:</b> ${item['purchase_price']:,}<br>
                            <b>Estimated ARV:</b> ${item['arv']:,}
                        </div>
                        <div class="card-location">
                            📍 <b>{item['location']}</b> &nbsp;|&nbsp; ID: <code>{item['id']}</code>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                if st.button("View Documentation", key=f"btn_{item['id']}"):
                    st.success(f"Accessing secure package for {item['id']}")
