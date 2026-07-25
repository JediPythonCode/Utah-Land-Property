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

# Page Configuration - Enterprise Real Estate Portal Layout
st.set_page_config(
    page_title="Utah Real Estate & Land For Sale. | Utah Land & Property Inc.",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---> MOBILE HEADER WITH CENTERED, LARGER LOGO & FLYOUT DRAWER <---
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Inter:wght@400;500;600;700;900&display=swap');

        /* Hide default Streamlit chrome & native sidebar controls */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        [data-testid="stSidebar"] {display: none !important;}
        
        .stApp {
            background-color: #f4f5f7;
            color: #2c3e50;
            font-family: "Inter", -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* Fixed Sticky Header Layout mimicking Mobile */
        .industry-header {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            background-color: #ffffff;
            border-bottom: 1px solid #e5e7eb;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 20px;
            height: 60px;
            z-index: 999999;
            box-sizing: border-box;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        }

        .header-left {
            display: flex;
            align-items: center;
            z-index: 2;
        }

        /* Pure CSS Checkbox Hack for Functional Hamburger Menu Drawer */
        #menu-toggle {
            display: none;
        }

        .hamburger-label {
            font-size: 24px;
            color: #111827;
            cursor: pointer;
            user-select: none;
            line-height: 1;
            font-weight: 700;
        }

        /* Absolutely Centered and Larger Header Logo */
        .header-logo-container {
            position: absolute;
            left: 50%;
            transform: translateX(-50%);
            text-align: center;
            z-index: 1;
        }

        .header-logo {
            font-size: 22px;
            font-weight: 900 !important;
            color: #d92228 !important;
            letter-spacing: 0.5px;
            text-decoration: none !important;
            font-family: 'Playfair Display', Georgia, serif;
            white-space: nowrap;
        }
        .header-logo:hover {
            color: #d92228 !important;
            text-decoration: none !important;
        }

        .header-right {
            display: flex;
            align-items: center;
            z-index: 2;
        }
        
        .sign-in-link {
            color: #d92228 !important;
            font-weight: 700 !important;
            font-size: 14px;
            text-decoration: none !important;
        }
        .sign-in-link:hover {
            color: #a8191e !important;
        }

        /* Slide-out Mobile Navigation Drawer */
        .mobile-drawer {
            position: fixed;
            top: 60px;
            left: -280px;
            width: 280px;
            height: calc(100vh - 60px);
            background-color: #ffffff;
            border-right: 1px solid #e5e7eb;
            box-shadow: 4px 0 12px rgba(0,0,0,0.1);
            transition: left 0.3s ease-in-out;
            z-index: 999998;
            padding: 20px;
            box-sizing: border-box;
        }

        #menu-toggle:checked ~ .mobile-drawer {
            left: 0;
        }

        .drawer-title {
            font-size: 16px;
            font-weight: 800;
            color: #111827;
            margin-bottom: 16px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .drawer-link {
            display: block;
            padding: 12px 16px;
            color: #374151;
            text-decoration: none;
            font-weight: 600;
            font-size: 15px;
            border-radius: 6px;
            margin-bottom: 6px;
            transition: background 0.2s;
        }

        .drawer-link:hover {
            background-color: #f3f4f6;
            color: #d92228;
        }
        
        .drawer-link.primary-action {
            background-color: #d92228;
            color: #ffffff;
            text-align: center;
            margin-top: 20px;
        }

        .drawer-link.primary-action:hover {
            background-color: #b51c22;
            color: #ffffff;
        }

        /* Push main content down below fixed header */
        .block-container {
            padding-top: 60px !important;
            padding-left: 0rem !important;
            padding-right: 0rem !important;
            max-width: 100% !important;
        }

        /* Immersive Zillow-Style Hero Banner */
        .hero-container {
            position: relative;
            background: linear-gradient(rgba(0, 0, 0, 0.45), rgba(0, 0, 0, 0.45)), 
                        url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=2000&q=80');
            background-size: cover;
            background-position: center;
            height: 380px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            color: white;
            padding: 0 20px;
            margin-bottom: 30px;
        }

        .hero-title {
            font-size: 52px;
            font-weight: 900;
            margin-bottom: 12px;
            letter-spacing: -0.5px;
            text-shadow: 0 3px 6px rgba(0,0,0,0.4);
            font-family: 'Inter', sans-serif;
            line-height: 1.1;
        }

        .hero-subtitle {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 24px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.4);
            letter-spacing: 0.3px;
        }
        
        .section-header {
            font-size: 1.4rem;
            font-weight: 800;
            color: #111827;
            margin: 30px 20px 15px 20px;
            padding-bottom: 8px;
            border-bottom: 2px solid #e5e7eb;
        }

        /* Legal Notice Footer Styling */
        .legal-footer {
            background-color: #111827;
            color: #9ca3af;
            font-size: 12px;
            line-height: 1.6;
            padding: 40px 20px;
            text-align: center;
            margin-top: 60px;
            border-top: 1px solid #374151;
        }
        .legal-footer-content {
            max-width: 900px;
            margin: 0 auto;
        }
    </style>

    <!-- Zillow-Style Mobile Header with Centered, Larger Title & Functional Drawer -->
    <input type="checkbox" id="menu-toggle">
    <div class="industry-header">
        <div class="header-left">
            <label for="menu-toggle" class="hamburger-label">&#9776;</label>
        </div>
        <div class="header-logo-container">
            <a href="#" class="header-logo">UTAH LAND & PROPERTY</a>
        </div>
        <div class="header-right">
            <a href="#contracts-section" class="sign-in-link">Sign In</a>
        </div>
    </div>

    <div class="mobile-drawer">
        <div class="drawer-title">Navigation Menu</div>
        <a href="#residential-section" class="drawer-link">Residential</a>
        <a href="#raw-land-section" class="drawer-link">Raw Land</a>
        <a href="#commercial-section" class="drawer-link">Commercial</a>
        <a href="#contracts-section" class="drawer-link primary-action">Sign In / Account</a>
    </div>
    """,
    unsafe_allow_html=True,
)

# Friendly Zillow-Inspired Hero Section
st.markdown(
    """
    <div class="hero-container">
        <div class="hero-title">Investments. Land. Utah Real Estate.</div>
        <div class="hero-subtitle">Off-Market Properties & Exclusive Real Estate Contracts</div>
    </div>
    <div id="contracts-section"></div>
    """,
    unsafe_allow_html=True,
)

# Load Property Database
@st.cache_data
def load_utah_property_database():
    data = [
        {
            "id": "UT-MIL-0101",
            "title": "Millcreek Residential Condo Parcel (Active Contract)",
            "category": "Residential",
            "city": "Millcreek, UT",
            "contract_price": 5000,
            "purchase_price": 165000,
            "down_payment_pct": 20,
            "down_payment_amt": int(165000 * 0.20),
            "arv": int(165000 * 1.32),
            "beds": 1,
            "baths": 1,
            "sqft": 750,
            "status": "UNDER CONTRACT",
            "address": "4629 S Quail Vista Cve #J, Millcreek, UT 84117",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80",
            "lat": 40.6977,
            "lon": -111.8550,
        },
        {
            "id": "UT-CLK-0301",
            "title": "Clearfield Off-Market Townhome Parcel",
            "category": "Residential",
            "city": "Clearfield, UT",
            "contract_price": 8000,
            "purchase_price": 285000,
            "down_payment_pct": 20,
            "down_payment_amt": int(285000 * 0.20),
            "arv": int(285000 * 1.28),
            "beds": 3,
            "baths": 2,
            "sqft": 1520,
            "status": "Available",
            "address": "350 S State St, Clearfield, UT 84015",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80",
            "lat": 41.1118,
            "lon": -112.2426,
        },
        {
            "id": "010-59G-008",
            "title": "Elko County Off-Market Rural Land Parcel",
            "category": "Raw Land",
            "city": "Elko County, NV",
            "contract_price": 4500,
            "purchase_price": 95000,
            "down_payment_pct": 25,
            "down_payment_amt": int(95000 * 0.25),
            "arv": int(95000 * 1.30),
            "beds": 0,
            "baths": 0,
            "sqft": 43560,
            "status": "UNDER CONTRACT",
            "address": "Off-Market Tract 12, Elko County, NV",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 41.5000,
            "lon": -115.5000,
        },
        {
            "id": "UT-DRP-0201",
            "title": "Draper Off-Market Commercial Land Parcel",
            "category": "Commercial",
            "city": "Draper, UT",
            "contract_price": 15000,
            "purchase_price": 310000,
            "down_payment_pct": 25,
            "down_payment_amt": int(310000 * 0.25),
            "arv": int(310000 * 1.30),
            "beds": 0,
            "baths": 0,
            "sqft": 4791,
            "status": "UNDER CONTRACT",
            "address": "Off-Market Fort St Parcel A, Draper, UT 84020",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 40.5243,
            "lon": -111.8631,
        },
    ]
    return data

properties = load_utah_property_database()

# ---> LIVE DEAL-FLOW TERMINAL & OPERATOR METRICS <---
st.markdown("### Live Deal-Flow Terminal & Operator Metrics", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Active Portfolios", "4", "+1 this week")
col2.metric("Contract Volume", "$1.28M", "+12.4%")
col3.metric("Operator Yield", "18.4%", "+2.1%")
col4.metric("Verification Status", "Secured", "100%")

# Interactive Map View using Pydeck
st.markdown("### Regional Asset Map", unsafe_allow_html=True)
df_map = pd.DataFrame(properties)
st.pydeck_chart(
    pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state=pdk.ViewState(
            latitude=df_map["lat"].mean(),
            longitude=df_map["lon"].mean(),
            zoom=7,
            pitch=30,
        ),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=df_map,
                get_position="[lon, lat]",
                get_color="[217, 34, 40, 200]",
                get_radius=8000,
                pickable=True,
            ),
        ],
    )
)

# Portfolio Catalog Display
st.markdown("### Active Inventory & Contract Listings", unsafe_allow_html=True)
for p in properties:
    with st.container():
        st.markdown(
            f"""
            <div style="background: white; padding: 20px; border-radius: 8px; border: 1px solid #e5e7eb; margin-bottom: 15px;">
                <h4 style="margin: 0 0 10px 0; color: #111827;">{p['title']}</h4>
                <p style="margin: 0 0 5px 0; color: #6b7280;"><b>Address:</b> {p['address']}</p>
                <p style="margin: 0 0 5px 0; color: #6b7280;"><b>Purchase Price:</b> ${p['purchase_price']:,} | <b>Down Payment:</b> ${p['down_payment_amt']:,} ({p['down_payment_pct']}%)</p>
                <p style="margin: 0; color: #d92228; font-weight: 700;">Status: {p['status']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

# Regulatory Compliance Footer
st.markdown(
    """
    <div class="legal-footer">
        <div class="legal-footer-content">
            <strong>Notice:</strong> Utah Land & Property Inc. is a private investment firm and is not a licensed real estate broker or agent.<br>
            We do not represent third parties in the purchase, sale, or management of outside real estate.<br>
            Pursuant to the exemption under Utah Code § 61-2f-202, all property management functions are executed solely by individuals, 
            operating as regular salaried employees of the specific legal entities that own the underlying real estate assets.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
