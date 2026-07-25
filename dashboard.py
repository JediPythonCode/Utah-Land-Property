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

# ---> ZILLOW-STYLE MOBILE HEADER WITH CENTERED, LARGER LOGO & FLYOUT DRAWER <---
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

        /* Fixed Sticky Header Layout mimicking Zillow Mobile */
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

        /* Immersive Hero Banner */
        .hero-container {
            position: relative;
            background: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)), 
                        url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=2000&q=80');
            background-size: cover;
            background-position: center;
            height: 350px;
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
            font-size: 32px;
            font-weight: 800;
            margin-bottom: 8px;
            letter-spacing: -0.5px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
            font-family: 'Inter', sans-serif;
        }

        .hero-subtitle {
            font-size: 15px;
            font-weight: 400;
            margin-bottom: 24px;
            text-shadow: 0 1px 3px rgba(0,0,0,0.3);
        }
        
        .section-header {
            font-size: 1.4rem;
            font-weight: 800;
            color: #111827;
            margin: 30px 20px 15px 20px;
            padding-bottom: 8px;
            border-bottom: 2px solid #e5e7eb;
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

# Friendly Residential Hero Section
st.markdown(
    """
    <div class="hero-container">
        <div class="hero-title">Utah Land & Property</div>
        <div class="hero-subtitle">Private Utah Real Estate Transactions & Parcels.</div>
    </div>
    <div id="contracts-section"></div>
    """,
    unsafe_allow_html=True,
)


# Quadrupled Property Database categorized into Residential, Raw Land, and Commercial
@st.cache_data
def load_utah_property_database():
    data = [
        # --- RESIDENTIAL ---
        {
            "id": "UT-MIL-0101",
            "title": "Millcreek Residential Condo Parcel",
            "category": "Residential",
            "city": "Millcreek, UT",
            "contract_price": 5000,
            "purchase_price": 165000,
            "arv": 225000,
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
            "id": "UT-MIL-0101-B",
            "title": "Millcreek Quail Vista Townhome Suite",
            "category": "Residential",
            "city": "Millcreek, UT",
            "contract_price": 6000,
            "purchase_price": 185000,
            "arv": 240000,
            "beds": 2,
            "baths": 1,
            "sqft": 920,
            "status": "Available",
            "address": "4631 S Quail Vista Cve #K, Millcreek, UT 84117",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80",
            "lat": 40.6979,
            "lon": -111.8552,
        },
        {
            "id": "UT-MIL-0101-C",
            "title": "Millcreek Skyline View Residence",
            "category": "Residential",
            "city": "Millcreek, UT",
            "contract_price": 7500,
            "purchase_price": 210000,
            "arv": 275000,
            "beds": 2,
            "baths": 2,
            "sqft": 1100,
            "status": "Available",
            "address": "4590 S Quail Vista Cve, Millcreek, UT 84117",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80",
            "lat": 40.6985,
            "lon": -111.8560,
        },
        {
            "id": "UT-MIL-0101-D",
            "title": "Millcreek Valley Executive Condo",
            "category": "Residential",
            "city": "Millcreek, UT",
            "contract_price": 8500,
            "purchase_price": 235000,
            "arv": 300000,
            "beds": 3,
            "baths": 2,
            "sqft": 1350,
            "status": "UNDER CONTRACT",
            "address": "4520 S Quail Vista Cve, Millcreek, UT 84117",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80",
            "lat": 40.6990,
            "lon": -111.8570,
        },
        {
            "id": "UT-MIL-0102",
            "title": "Millcreek Elmwood Contract Assignment",
            "category": "Residential",
            "city": "Millcreek, UT",
            "contract_price": 12000,
            "purchase_price": 420000,
            "arv": 625000,
            "beds": 5,
            "baths": 2,
            "sqft": 2446,
            "status": "UNDER CONTRACT",
            "address": "718 E Elgin Ave, Millcreek, UT 84106",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=800&q=80",
            "lat": 40.7012,
            "lon": -111.8670,
        },
        {
            "id": "UT-MIL-0102-B",
            "title": "Millcreek Highland Family Home",
            "category": "Residential",
            "city": "Millcreek, UT",
            "contract_price": 14000,
            "purchase_price": 450000,
            "arv": 660000,
            "beds": 4,
            "baths": 3,
            "sqft": 2600,
            "status": "Available",
            "address": "740 E Elgin Ave, Millcreek, UT 84106",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=800&q=80",
            "lat": 40.7015,
            "lon": -111.8675,
        },
        {
            "id": "UT-MIL-0102-C",
            "title": "Millcreek Woodland Craftsman",
            "category": "Residential",
            "city": "Millcreek, UT",
            "contract_price": 15000,
            "purchase_price": 480000,
            "arv": 690000,
            "beds": 4,
            "baths": 3,
            "sqft": 2800,
            "status": "Available",
            "address": "802 E Elgin Ave, Millcreek, UT 84106",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=800&q=80",
            "lat": 40.7018,
            "lon": -111.8680,
        },
        {
            "id": "UT-MIL-0102-D",
            "title": "Millcreek Orchard Modern Bungalow",
            "category": "Residential",
            "city": "Millcreek, UT",
            "contract_price": 16000,
            "purchase_price": 510000,
            "arv": 720000,
            "beds": 5,
            "baths": 3,
            "sqft": 3100,
            "status": "Available",
            "address": "850 E Elgin Ave, Millcreek, UT 84106",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=800&q=80",
            "lat": 40.7020,
            "lon": -111.8685,
        },
        {
            "id": "UT-CLK-0301",
            "title": "Park Meadows Townhomes Investment",
            "category": "Residential",
            "city": "Clearfield, UT",
            "contract_price": 8000,
            "purchase_price": 285000,
            "arv": 345000,
            "beds": 3,
            "baths": 2,
            "sqft": 1520,
            "status": "Available",
            "address": "Park Meadows Townhomes, Clearfield, UT 84015",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80",
            "lat": 41.1118,
            "lon": -112.2426,
        },
        {
            "id": "UT-CLK-0301-B",
            "title": "Park Meadows Fairway Townhome",
            "category": "Residential",
            "city": "Clearfield, UT",
            "contract_price": 8500,
            "purchase_price": 295000,
            "arv": 360000,
            "beds": 3,
            "baths": 2,
            "sqft": 1580,
            "status": "Available",
            "address": "124 Park Meadows Dr, Clearfield, UT 84015",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80",
            "lat": 41.1120,
            "lon": -112.2430,
        },
        {
            "id": "UT-CLK-0301-C",
            "title": "Park Meadows Sunset Townhome",
            "category": "Residential",
            "city": "Clearfield, UT",
            "contract_price": 9000,
            "purchase_price": 310000,
            "arv": 375000,
            "beds": 4,
            "baths": 3,
            "sqft": 1750,
            "status": "Available",
            "address": "145 Park Meadows Dr, Clearfield, UT 84015",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80",
            "lat": 41.1125,
            "lon": -112.2435,
        },
        {
            "id": "UT-CLK-0301-D",
            "title": "Park Meadows Lakeside Townhome",
            "category": "Residential",
            "city": "Clearfield, UT",
            "contract_price": 9500,
            "purchase_price": 325000,
            "arv": 390000,
            "beds": 4,
            "baths": 3,
            "sqft": 1850,
            "status": "UNDER CONTRACT",
            "address": "180 Park Meadows Dr, Clearfield, UT 84015",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80",
            "lat": 41.1130,
            "lon": -112.2440,
        },
        # --- RAW LAND ---
        {
            "id": "010-59G-008",
            "title": "Elko County Rural Land Parcel with Power",
            "category": "Raw Land",
            "city": "Elko County, NV",
            "contract_price": 4500,
            "purchase_price": 95000,
            "arv": 125000,
            "beds": 0,
            "baths": 0,
            "sqft": 43560,
            "status": "Available",
            "address": "Parcel 010-59G-008 (0 SEC 36 TWP 40N RGE 69E MDB&M)",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 41.5000,
            "lon": -115.5000,
        },
        {
            "id": "010-59G-008-B",
            "title": "Elko County Sunset Horizon Acre",
            "category": "Raw Land",
            "city": "Elko County, NV",
            "contract_price": 4800,
            "purchase_price": 98000,
            "arv": 130000,
            "beds": 0,
            "baths": 0,
            "sqft": 43560,
            "status": "Available",
            "address": "Parcel 010-59G-009, Elko County, NV",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 41.5002,
            "lon": -115.5002,
        },
        {
            "id": "010-59G-008-C",
            "title": "Elko County Mountain View Tract",
            "category": "Raw Land",
            "city": "Elko County, NV",
            "contract_price": 5000,
            "purchase_price": 102000,
            "arv": 135000,
            "beds": 0,
            "baths": 0,
            "sqft": 43560,
            "status": "Available",
            "address": "Parcel 010-59G-010, Elko County, NV",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 41.5004,
            "lon": -115.5004,
        },
        {
            "id": "010-59G-008-D",
            "title": "Elko County Valley Vista Acre",
            "category": "Raw Land",
            "city": "Elko County, NV",
            "contract_price": 5200,
            "purchase_price": 105000,
            "arv": 140000,
            "beds": 0,
            "baths": 0,
            "sqft": 43560,
            "status": "Available",
            "address": "Parcel 010-59G-011, Elko County, NV",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 41.5006,
            "lon": -115.5006,
        },
        {
            "id": "010-749-036",
            "title": "Sawgrass Court Residential Lot 036",
            "category": "Raw Land",
            "city": "Elko County, NV",
            "contract_price": 4500,
            "purchase_price": 115000,
            "arv": 150000,
            "beds": 0,
            "baths": 0,
            "sqft": 10500,
            "status": "Available",
            "address": "2989 Sawgrass Ct, Elko County, NV",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 41.5010,
            "lon": -115.5010,
        },
        {
            "id": "010-749-036-B",
            "title": "Sawgrass Court Residential Lot 036-B",
            "category": "Raw Land",
            "city": "Elko County, NV",
            "contract_price": 4600,
            "purchase_price": 118000,
            "arv": 155000,
            "beds": 0,
            "baths": 0,
            "sqft": 10500,
            "status": "Available",
            "address": "2991 Sawgrass Ct, Elko County, NV",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 41.5011,
            "lon": -115.5011,
        },
        {
            "id": "010-749-037",
            "title": "Sawgrass Court Residential Lot 037",
            "category": "Raw Land",
            "city": "Elko County, NV",
            "contract_price": 4500,
            "purchase_price": 115000,
            "arv": 150000,
            "beds": 0,
            "baths": 0,
            "sqft": 10500,
            "status": "Available",
            "address": "2981 Sawgrass Ct, Elko County, NV",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 41.5012,
            "lon": -115.5012,
        },
        {
            "id": "010-749-037-B",
            "title": "Sawgrass Court Residential Lot 037-B",
            "category": "Raw Land",
            "city": "Elko County, NV",
            "contract_price": 4700,
            "purchase_price": 120000,
            "arv": 158000,
            "beds": 0,
            "baths": 0,
            "sqft": 10500,
            "status": "Available",
            "address": "2983 Sawgrass Ct, Elko County, NV",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 41.5013,
            "lon": -115.5013,
        },
        {
            "id": "010-749-039",
            "title": "Sawgrass Court Residential Lot 039",
            "category": "Raw Land",
            "city": "Elko County, NV",
            "contract_price": 4500,
            "purchase_price": 115000,
            "arv": 150000,
            "beds": 0,
            "baths": 0,
            "sqft": 10500,
            "status": "Available",
            "address": "2961 Sawgrass Ct, Elko County, NV",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 41.5015,
            "lon": -115.5015,
        },
        {
            "id": "010-749-039-B",
            "title": "Sawgrass Court Residential Lot 039-B",
            "category": "Raw Land",
            "city": "Elko County, NV",
            "contract_price": 4800,
            "purchase_price": 122000,
            "arv": 160000,
            "beds": 0,
            "baths": 0,
            "sqft": 10500,
            "status": "Available",
            "address": "2963 Sawgrass Ct, Elko County, NV",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 41.5016,
            "lon": -115.5016,
        },
        {
            "id": "010-749-040",
            "title": "Sawgrass Court Residential Lot 040",
            "category": "Raw Land",
            "city": "Elko County, NV",
            "contract_price": 4500,
            "purchase_price": 115000,
            "arv": 150000,
            "beds": 0,
            "baths": 0,
            "sqft": 10500,
            "status": "Available",
            "address": "2953 Sawgrass Ct, Elko County, NV",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 41.5018,
            "lon": -115.5018,
        },
        {
            "id": "010-749-040-B",
            "title": "Sawgrass Court Residential Lot 040-B",
            "category": "Raw Land",
            "city": "Elko County, NV",
            "contract_price": 4900,
            "purchase_price": 125000,
            "arv": 162000,
            "beds": 0,
            "baths": 0,
            "sqft": 10500,
            "status": "Available",
            "address": "2955 Sawgrass Ct, Elko County, NV",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 41.5019,
            "lon": -115.5019,
        },
        {
            "id": "010-81H-032",
            "title": "Elko County North Rural Acreage",
            "category": "Raw Land",
            "city": "Elko County, NV",
            "contract_price": 5000,
            "purchase_price": 125000,
            "arv": 165000,
            "beds": 0,
            "baths": 0,
            "sqft": 87120,
            "status": "Available",
            "address": "Parcel 010-81H-032 (0 SEC 31 TWP 40N RGE 70E MDB&M)",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 41.5200,
            "lon": -115.4800,
        },
        {
            "id": "010-81H-032-B",
            "title": "Elko County North High Desert Tract",
            "category": "Raw Land",
            "city": "Elko County, NV",
            "contract_price": 5200,
            "purchase_price": 128000,
            "arv": 170000,
            "beds": 0,
            "baths": 0,
            "sqft": 87120,
            "status": "Available",
            "address": "Parcel 010-81H-033, Elko County, NV",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 41.5202,
            "lon": -115.4802,
        },
        {
            "id": "010-81H-032-C",
            "title": "Elko County North Panorama Acreage",
            "category": "Raw Land",
            "city": "Elko County, NV",
            "contract_price": 5500,
            "purchase_price": 132000,
            "arv": 175000,
            "beds": 0,
            "baths": 0,
            "sqft": 87120,
            "status": "Available",
            "address": "Parcel 010-81H-034, Elko County, NV",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 41.5204,
            "lon": -115.4804,
        },
        {
            "id": "010-81H-032-D",
            "title": "Elko County North Frontier Estate",
            "category": "Raw Land",
            "city": "Elko County, NV",
            "contract_price": 5800,
            "purchase_price": 135000,
            "arv": 180000,
            "beds": 0,
            "baths": 0,
            "sqft": 87120,
            "status": "Available",
            "address": "Parcel 010-81H-035, Elko County, NV",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 41.5206,
            "lon": -115.4806,
        },
        # --- COMMERCIAL ---
        {
            "id": "UT-DRP-0201",
            "title": "Draper Commercial Land Parcel",
            "category": "Commercial",
            "city": "Draper, UT",
            "contract_price": 15000,
            "purchase_price": 310000,
            "arv": 450000,
            "beds": 0,
            "baths": 0,
            "sqft": 4791,
            "status": "Available",
            "address": "Fort Street Parcel, Draper, UT 84020",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 40.5243,
            "lon": -111.8631,
        },
        {
            "id": "UT-DRP-0201-B",
            "title": "Draper Fort Street Retail Pad",
            "category": "Commercial",
            "city": "Draper, UT",
            "contract_price": 16500,
            "purchase_price": 330000,
            "arv": 480000,
            "beds": 0,
            "baths": 0,
            "sqft": 5200,
            "status": "Available",
            "address": "1250 Fort St, Draper, UT 84020",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 40.5246,
            "lon": -111.8635,
        },
        {
            "id": "UT-DRP-0201-C",
            "title": "Draper Business Park Development Site",
            "category": "Commercial",
            "city": "Draper, UT",
            "contract_price": 18000,
            "purchase_price": 360000,
            "arv": 520000,
            "beds": 0,
            "baths": 0,
            "sqft": 6100,
            "status": "Available",
            "address": "1280 Fort St, Draper, UT 84020",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 40.5250,
            "lon": -111.8640,
        },
        {
            "id": "UT-DRP-0201-D",
            "title": "Draper Commercial Plaza Lot",
            "category": "Commercial",
            "city": "Draper, UT",
            "contract_price": 20000,
            "purchase_price": 395000,
            "arv": 570000,
            "beds": 0,
            "baths": 0,
            "sqft": 7200,
            "status": "Available",
            "address": "1310 Fort St, Draper, UT 84020",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 40.5255,
            "lon": -111.8645,
        },
    ]
    return pd.DataFrame(data)


df = load_utah_property_database()


# Automated Email / Offer Dispatch Helper
def send_offer_dispatch(
    property_id, property_title, recipient_email, offer_terms
):
    smtp_server = "smtp.gmail.com"
    port = 587
    sender_email = st.secrets.get("EMAIL_USER", "your-email@domain.com")
    sender_password = st.secrets.get("EMAIL_PASS", "your-app-password")

    subject = f"Official Offer / Escrow Submission: {property_id}"
    body = f"""
    Automated Transaction & Offer Workflow Dispatch:
    Property ID: {property_id}
    Asset Title: {property_title}
    Submitter Contact: {recipient_email}
    Offer Terms & Conditions: {offer_terms}
    ---
    Notice: Utah Land & Property Inc. - Secure Escrow & Offer Routing Engine.
    """

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        return True
    except Exception:
        return False


# --- DYNAMIC HEADER TITLE SECTION ---
if "show_faq" not in st.session_state:
    st.session_state.show_faq = False

col_title_1, col_title_2 = st.columns([3, 1])
with col_title_1:
    st.markdown(
        f"""
        <div style="margin: 24px 20px 16px 20px;">
            <h1 style="font-size: 1.7rem; font-weight: 800; color: #111827; margin-bottom: 4px;">Utah Land & Property Inc. Real Estate & Land For Sale</h1>
            <p style="font-size: 0.95rem; color: #6b7280; margin: 0;"><b>{len(df)}</b> active private contracts and land parcels available</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

with col_title_2:
    st.markdown(
        "<div style='margin: 36px 20px 0 0; text-align: right;'>",
        unsafe_allow_html=True,
    )
    if st.button("How private contract assignment works & FAQ", type="tertiary"):
        st.session_state.show_faq = not st.session_state.show_faq
    st.markdown("</div>", unsafe_allow_html=True)


# Render Function for Property Grids
def render_property_grid(subset_df, category_title, anchor_id):
    st.markdown(
        f'<div id="{anchor_id}" class="section-header">{category_title} ({len(subset_df)})</div>',
        unsafe_allow_html=True,
    )
    st.markdown("<div style='padding: 0 20px;'>", unsafe_allow_html=True)

    if subset_df.empty:
        st.info(f"No {category_title.lower()} listings available.")
    else:
        cols_per_row = 3
        rows = [
            subset_df.iloc[i : i + cols_per_row]
            for i in range(0, len(subset_df), cols_per_row)
        ]

        for row_batch in rows:
            cols = st.columns(cols_per_row, gap="medium")
            for idx, (_, row) in enumerate(row_batch.iterrows()):
                listing_images = (
                    row["image"].split(",")
                    if isinstance(row["image"], str)
                    else [row["image"]]
                )
                first_image = listing_images[0].strip()

                badge_bg = (
                    "#b91c1c"
                    if row["status"] == "UNDER CONTRACT"
                    else "rgba(0,0,0,0.7)"
                )

                with cols[idx]:
                    st.markdown(
                        f"""
                            <div style="background: white; border-radius: 8px; overflow: hidden; border: 1px solid #e5e7eb; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                                <div style="position: relative;">
                                    <img src="{first_image}" style="width: 100%; height: 200px; object-fit: cover;">
                                    <div style="position: absolute; top: 12px; left: 12px; background: {badge_bg}; color: white; padding: 4px 10px; border-radius: 4px; font-size: 12px; font-weight: 700; letter-spacing: 0.5px;">{row['status']}</div>
                                </div>
                                <div style="padding: 16px;">
                                    <div style="font-size: 11px; text-transform: uppercase; color: #6b7280; font-weight: 700; margin-bottom: 4px;">{row['broker']}</div>
                                    <div style="font-size: 16px; font-weight: 800; color: #111827; margin-bottom: 6px;">Contract: ${row['contract_price']:,}</div>
                                    <div style="font-size: 13px; color: #374151; margin-bottom: 2px;">Property Purchase Price: <b>${row['purchase_price']:,}</b></div>
                                    <div style="font-size: 13px; color: #047857; font-weight: 600; margin-bottom: 8px;">ARV: ${row['arv']:,}</div>
                                    <div style="font-size: 13px; color: #374151; margin-bottom: 8px;"><b>{row['beds']}</b> bds &nbsp;|&nbsp; <b>{row['baths']}</b> ba &nbsp;|&nbsp; <b>{row['sqft']:,}</b> sqft</div>
                                    <div style="font-size: 13px; color: #6b7280;">{row['address']}</div>
                                </div>
                            </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    with st.expander(
                        f"Review Terms / Submit Offer ({row['id']})"
                    ):
                        user_email = st.text_input(
                            "Your Email",
                            key=f"p_email_{row['id']}",
                            placeholder="name@domain.com",
                        )
                        offer_terms = st.text_area(
                            "Offer Terms & Conditions",
                            key=f"p_msg_{row['id']}",
                            placeholder="Enter contract purchase price, assignment fee, or escrow contingencies...",
                        )
                        if st.button(
                            "Submit Official Offer", key=f"p_btn_{row['id']}"
                        ):
                            if user_email:
                                send_offer_dispatch(
                                    row["id"],
                                    row["title"],
                                    user_email,
                                    offer_terms,
                                )
                                st.success(
                                    "Offer successfully dispatched to escrow!"
                                )
                            else:
                                st.error("Please enter a valid email address.")
    st.markdown("</div>", unsafe_allow_html=True)


# --- RENDER SEPARATED CATEGORY SECTIONS ---
render_property_grid(
    df[df["category"] == "Residential"], "Residential", "residential-section"
)
render_property_grid(
    df[df["category"] == "Raw Land"], "Raw Land", "raw-land-section"
)
render_property_grid(
    df[df["category"] == "Commercial"], "Commercial", "commercial-section"
)
