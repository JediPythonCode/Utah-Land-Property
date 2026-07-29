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

# ---> AUTHENTICATION SESSION STATE SETUP <---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# ---> CUSTOM STYLING & CLEAN LAYOUT <---
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Inter:wght@400;500;600;700;900&display=swap');

        .stApp {
            background-color: #f8fafc;
            color: #1e293b;
            font-family: "Inter", -apple-system, BlinkMacSystemFont, sans-serif;
        }

        .main-header {
            background: linear-gradient(rgba(0, 0, 0, 0.45), rgba(0, 0, 0, 0.45)), 
                        url('https://images.unsplash.com/photo-1564013799919-ab600027ffc6?auto=format&fit=crop&w=2000&q=80');
            background-size: cover;
            background-position: center;
            padding: 80px 20px;
            text-align: center;
            color: white;
            border-radius: 12px;
            margin-bottom: 30px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        }

        .main-title {
            font-family: 'Playfair Display', Georgia, serif;
            font-size: 48px;
            font-weight: 900;
            margin-bottom: 12px;
            letter-spacing: -0.5px;
            text-shadow: 0 4px 8px rgba(0,0,0,0.4);
        }

        .main-subtitle {
            font-size: 18px;
            font-weight: 500;
            max-width: 800px;
            margin: 0 auto 8px auto;
            text-shadow: 0 2px 4px rgba(0,0,0,0.4);
        }

        .section-header {
            font-family: 'Playfair Display', Georgia, serif;
            font-size: 2rem;
            font-weight: 700;
            color: #0f172a;
            margin: 40px 0 20px 0;
            padding-bottom: 10px;
            border-bottom: 3px solid #d92228;
        }

        .property-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 16px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        .property-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 15px rgba(0,0,0,0.08);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---> MAIN HEADER SECTION <---
st.markdown(
    """
    <div class="main-header">
        <div class="main-title">Utah Land & Property Inc.</div>
        <div class="main-subtitle">Wholesale Real Estate Contract Assignments & Equitable Interest Opportunities</div>
        <div class="main-subtitle" style="font-size: 15px; opacity: 0.9;">We are not real estate agents or brokers. We market our equitable interest in signed purchase contracts.</div>
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

# ---> DATABASE GENERATOR (32 LISTINGS PER CATEGORY WITH TREE/LANDSCAPE IMAGERY, CITY & ZIP ONLY) <---
@st.cache_data
def load_utah_property_database():
    residential_images = [
        "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1600566753376-12c8ab7fb75b?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1600585154526-990dced4db0d?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1600573472550-8090b5e0745e?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1600047509807-ba8f99d2cdde?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1600585152220-90363fe7e115?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1600585154363-67eb9e2e2099?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1600566753086-acf0c8d7699f?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=800&q=80"
    ]
    
    land_images = [
        "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1447752875215-b2761acb3c5d?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1426604966848-d7adacbd02bf?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1511497584788-876761197069?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1454496522488-7a8e488e8606?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1434725039720-aaad6dd32dfe?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1509316975850-ff9c5deb0cd9?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1469474968028-56623f02e42e?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1473448912268-2022ce9509d8?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1541781774459-bb2af2f05b55?auto=format&fit=crop&w=800&q=80"
    ]

    commercial_images = [
        "https://images.unsplash.com/photo-1444703686981-a3bb84d82f60?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1554469384-e58fac16e23a?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1577495508048-b635879837f1?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=800&q=80"
    ]

    data = []
    statuses = ["Available", "UNDER CONTRACT"]
    
    # Generate 32 Residential Listings
    for i in range(1, 33):
        purchase_price = 150000 + (i * 12500)
        arv = int(purchase_price * 1.3)
        contract_price = 5000 + (i * 300)
        data.append({
            "id": f"RES-{1000+i}",
            "title": f"ASSIGNMENT OF PURCHASE CONTRACT. Equitable Interest, Utah Land & Property Inc. is selling contractual rights to purchase property, Millcreek 84117, Contract Purchase Price ${purchase_price:,} and Assignment Fee: $10,000 Estimated ARV Price: ${arv:,}",
            "category": "Residential",
            "city": "Millcreek, UT 84117",
            "contract_price": contract_price,
            "purchase_price": purchase_price,
            "arv": arv,
            "status": statuses[i % 2],
            "image": residential_images[(i - 1) % len(residential_images)],
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
            "title": f"ASSIGNMENT OF PURCHASE CONTRACT. Equitable Interest, Utah Land & Property Inc. is selling contractual rights to purchase land parcel, Elko County 89801, Contract Purchase Price ${purchase_price:,} and Assignment Fee: $10,000 Estimated ARV Price: ${arv:,}",
            "category": "Raw Land",
            "city": "Elko County, NV 89801",
            "contract_price": contract_price,
            "purchase_price": purchase_price,
            "arv": arv,
            "status": statuses[(i + 1) % 2],
            "image": land_images[(i - 1) % len(land_images)],
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
            "title": f"ASSIGNMENT OF PURCHASE CONTRACT. Equitable Interest, Utah Land & Property Inc. is selling contractual rights to purchase commercial property, Draper 84020, Contract Purchase Price ${purchase_price:,} and Assignment Fee: $10,000 Estimated ARV Price: ${arv:,}",
            "category": "Commercial",
            "city": "Draper, UT 84020",
            "contract_price": contract_price,
            "purchase_price": purchase_price,
            "arv": arv,
            "status": statuses[i % 2],
            "image": commercial_images[(i - 1) % len(commercial_images)],
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
                st.markdown('<div class="property-card">', unsafe_allow_html=True)
                st.image(item["image"], use_container_width=True)
                st.markdown(f"**{item['title']}**")
                st.markdown(f"Status: `{item['status']}` | Location: **{item['city']}**")
                st.markdown(f"Assignment Price: **${item['contract_price']:,}**")
                if st.button(f"View Details", key=f"btn_{item['id']}"):
                    st.success(f"Viewing documentation package for {item['id']}")
                st.markdown('</div>', unsafe_allow_html=True)
