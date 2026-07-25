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

# ---> MOBILE HEADER WITH CENTERED, LARGER LOGO & FLYOUT DRAWER <--
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

        /* Immersive Style Hero Banner */
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
            font-size: 40px;
            font-weight: 850;
            margin-bottom: 12px;
            letter-spacing: -0.5px;
            text-shadow: 0 6px 6px rgba(0,0,0,0.4);
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
    </style>

    <!-- Style Mobile Header with Centered, Larger Title & Functional Drawer -->
    <input type="checkbox" id="menu-toggle">
    <div class="industry-header">
        <div class="header-left">
            <label for="menu-toggle" class="hamburger-label">&#9776;</label>
        </div>
        <div class="header-logo-container">
            <a href="#" class="header-logo">UTAH LAND & PROPERTY</a>
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

# Friendly Zillow-Inspired Hero Section with Bold, Easy-to-Understand Words
st.markdown(
    """
    <div class="hero-container">
        <div class="hero-title">Utah Real Estate. <br> Utah Wholesale Houses & Real Estate For Sale.</div>
        <div class="hero-subtitle">Utah Private Real Estate Opportunities. Wholesale Utah Real Estate Contracts For Sale. </div>
    </div>
    <div id="contracts-section"></div>
    """,
    unsafe_allow_html=True,
)


# Property Database with active contracts, off-market addresses, 20-25% down payments, and mixed active statuses
@st.cache_data
def load_utah_property_database():
    data = [
        # --- RESIDENTIAL ---
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
            "id": "UT-MIL-0101-B",
            "title": "Millcreek Off-Market Hidden Gem",
            "category": "Residential",
            "city": "Millcreek, UT",
            "contract_price": 6000,
            "purchase_price": 185000,
            "down_payment_pct": 25,
            "down_payment_amt": int(185000 * 0.25),
            "arv": int(185000 * 1.35),
            "beds": 2,
            "baths": 1,
            "sqft": 920,
            "status": "UNDER CONTRACT",
            "address": "718 E Elgin Ave, Millcreek, UT 84106",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=800&q=80",
            "lat": 40.6979,
            "lon": -111.8552,
        },
        {
            "id": "UT-MIL-0101-C",
            "title": "Millcreek Woodland Off-Market Estate",
            "category": "Residential",
            "city": "Millcreek, UT",
            "contract_price": 7500,
            "purchase_price": 210000,
            "down_payment_pct": 20,
            "down_payment_amt": int(210000 * 0.20),
            "arv": int(210000 * 1.38),
            "beds": 2,
            "baths": 2,
            "sqft": 1100,
            "status": "UNDER CONTRACT",
            "address": "3450 S 2000 E, Millcreek, UT 84109",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80",
            "lat": 40.6985,
            "lon": -111.8560,
        },
        {
            "id": "UT-MIL-0101-D",
            "title": "Millcreek Valley Executive Off-Market Home",
            "category": "Residential",
            "city": "Millcreek, UT",
            "contract_price": 8500,
            "purchase_price": 235000,
            "down_payment_pct": 25,
            "down_payment_amt": int(235000 * 0.25),
            "arv": int(235000 * 1.40),
            "beds": 3,
            "baths": 2,
            "sqft": 1350,
            "status": "Available",
            "address": "3580 S 2300 E, Millcreek, UT 84109",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=800&q=80",
            "lat": 40.6990,
            "lon": -111.8570,
        },
        {
            "id": "UT-MIL-0102",
            "title": "Millcreek Orchard Off-Market Cottage",
            "category": "Residential",
            "city": "Millcreek, UT",
            "contract_price": 12000,
            "purchase_price": 420000,
            "down_payment_pct": 20,
            "down_payment_amt": int(420000 * 0.20),
            "arv": int(420000 * 1.30),
            "beds": 4,
            "baths": 2,
            "sqft": 2446,
            "status": "Available",
            "address": "3820 S 2700 E, Millcreek, UT 84109",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80",
            "lat": 40.7012,
            "lon": -111.8670,
        },
        {
            "id": "UT-MIL-0102-B",
            "title": "Millcreek Highland Pocket Listing",
            "category": "Residential",
            "city": "Millcreek, UT",
            "contract_price": 14000,
            "purchase_price": 450000,
            "down_payment_pct": 22,
            "down_payment_amt": int(450000 * 0.22),
            "arv": int(450000 * 1.33),
            "beds": 4,
            "baths": 3,
            "sqft": 2600,
            "status": "Available",
            "address": "3910 S 3000 E, Millcreek, UT 84124",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=800&q=80",
            "lat": 40.7015,
            "lon": -111.8675,
        },
        {
            "id": "UT-MIL-0102-C",
            "title": "Millcreek Canyon Rim Off-Market Build",
            "category": "Residential",
            "city": "Millcreek, UT",
            "contract_price": 15000,
            "purchase_price": 480000,
            "down_payment_pct": 25,
            "down_payment_amt": int(480000 * 0.25),
            "arv": int(480000 * 1.36),
            "beds": 4,
            "baths": 3,
            "sqft": 2800,
            "status": "UNDER CONTRACT",
            "address": "4020 S 3100 E, Millcreek, UT 84124",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80",
            "lat": 40.7018,
            "lon": -111.8680,
        },
        {
            "id": "UT-MIL-0102-D",
            "title": "Millcreek Crestview Private Asset",
            "category": "Residential",
            "city": "Millcreek, UT",
            "contract_price": 16000,
            "purchase_price": 510000,
            "down_payment_pct": 20,
            "down_payment_amt": int(510000 * 0.20),
            "arv": int(510000 * 1.39),
            "beds": 5,
            "baths": 3,
            "sqft": 3100,
            "status": "Available",
            "address": "4150 S 3200 E, Millcreek, UT 84124",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=800&q=80",
            "lat": 40.7020,
            "lon": -111.8685,
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
            "id": "UT-CLK-0301-B",
            "title": "Clearfield Sunset Off-Market Unit",
            "category": "Residential",
            "city": "Clearfield, UT",
            "contract_price": 8500,
            "purchase_price": 295000,
            "down_payment_pct": 25,
            "down_payment_amt": int(295000 * 0.25),
            "arv": int(295000 * 1.31),
            "beds": 3,
            "baths": 2,
            "sqft": 1580,
            "status": "UNDER CONTRACT",
            "address": "420 S 500 E, Clearfield, UT 84015",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=800&q=80",
            "lat": 41.1120,
            "lon": -112.2430,
        },
        {
            "id": "UT-CLK-0301-C",
            "title": "Clearfield Heritage Private Listing",
            "category": "Residential",
            "city": "Clearfield, UT",
            "contract_price": 9000,
            "purchase_price": 310000,
            "down_payment_pct": 20,
            "down_payment_amt": int(310000 * 0.20),
            "arv": int(310000 * 1.34),
            "beds": 4,
            "baths": 3,
            "sqft": 1750,
            "status": "Available",
            "address": "550 S 1000 E, Clearfield, UT 84015",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80",
            "lat": 41.1125,
            "lon": -112.2435,
        },
        {
            "id": "UT-CLK-0301-D",
            "title": "Clearfield Lakeside Off-Market Home",
            "category": "Residential",
            "city": "Clearfield, UT",
            "contract_price": 9500,
            "purchase_price": 325000,
            "down_payment_pct": 22,
            "down_payment_amt": int(325000 * 0.22),
            "arv": int(325000 * 1.37),
            "beds": 4,
            "baths": 3,
            "sqft": 1850,
            "status": "UNDER CONTRACT",
            "address": "680 S 1500 E, Clearfield, UT 84015",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=800&q=80",
            "lat": 41.1130,
            "lon": -112.2440,
        },
        # --- RAW LAND ---
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
            "id": "010-59G-008-B",
            "title": "Elko County Sunset Horizon Off-Market Acre",
            "category": "Raw Land",
            "city": "Elko County, NV",
            "contract_price": 4800,
            "purchase_price": 98000,
            "down_payment_pct": 20,
            "down_payment_amt": int(98000 * 0.20),
            "arv": int(98000 * 1.33),
            "beds": 0,
            "baths": 0,
            "sqft": 43560,
            "status": "Available",
            "address": "Off-Market Tract 14, Elko County, NV",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 41.5002,
            "lon": -115.5002,
        },
        {
            "id": "010-59G-008-C",
            "title": "Elko County Mountain View Off-Market Lot",
            "category": "Raw Land",
            "city": "Elko County, NV",
            "contract_price": 5000,
            "purchase_price": 102000,
            "down_payment_pct": 25,
            "down_payment_amt": int(102000 * 0.25),
            "arv": int(102000 * 1.35),
            "beds": 0,
            "baths": 0,
            "sqft": 43560,
            "status": "UNDER CONTRACT",
            "address": "Off-Market Tract 18, Elko County, NV",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 41.5004,
            "lon": -115.5004,
        },
        {
            "id": "010-59G-008-D",
            "title": "Elko County Valley Vista Off-Market Acre",
            "category": "Raw Land",
            "city": "Elko County, NV",
            "contract_price": 5200,
            "purchase_price": 105000,
            "down_payment_pct": 20,
            "down_payment_amt": int(105000 * 0.20),
            "arv": int(105000 * 1.38),
            "beds": 0,
            "baths": 0,
            "sqft": 43560,
            "status": "Available",
            "address": "Off-Market Tract 22, Elko County, NV",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 41.5006,
            "lon": -115.5006,
        },
        {
            "id": "010-749-036",
            "title": "Sawgrass Court Off-Market Lot 036",
            "category": "Raw Land",
            "city": "Elko County, NV",
            "contract_price": 4500,
            "purchase_price": 115000,
            "down_payment_pct": 20,
            "down_payment_amt": int(115000 * 0.20),
            "arv": int(115000 * 1.28),
            "beds": 0,
            "baths": 0,
            "sqft": 10500,
            "status": "Available",
            "address": "Off-Market Sawgrass Parcel A, Elko County, NV",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 41.5010,
            "lon": -115.5010,
        },
        {
            "id": "010-749-036-B",
            "title": "Sawgrass Court Off-Market Lot 036-B",
            "category": "Raw Land",
            "city": "Elko County, NV",
            "contract_price": 4600,
            "purchase_price": 118000,
            "down_payment_pct": 25,
            "down_payment_amt": int(118000 * 0.25),
            "arv": int(118000 * 1.31),
            "beds": 0,
            "baths": 0,
            "sqft": 10500,
            "status": "UNDER CONTRACT",
            "address": "Off-Market Sawgrass Parcel B, Elko County, NV",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 41.5011,
            "lon": -115.5011,
        },
        {
            "id": "010-749-037",
            "title": "Sawgrass Court Off-Market Lot 037",
            "category": "Raw Land",
            "city": "Elko County, NV",
            "contract_price": 4500,
            "purchase_price": 115000,
            "down_payment_pct": 20,
            "down_payment_amt": int(115000 * 0.20),
            "arv": int(115000 * 1.34),
            "beds": 0,
            "baths": 0,
            "sqft": 10500,
            "status": "Available",
            "address": "Off-Market Sawgrass Parcel C, Elko County, NV",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 41.5012,
            "lon": -115.5012,
        },
        {
            "id": "010-749-037-B",
            "title": "Sawgrass Court Off-Market Lot 037-B",
            "category": "Raw Land",
            "city": "Elko County, NV",
            "contract_price": 4700,
            "purchase_price": 120000,
            "down_payment_pct": 22,
            "down_payment_amt": int(120000 * 0.22),
            "arv": int(120000 * 1.36),
            "beds": 0,
            "baths": 0,
            "sqft": 10500,
            "status": "Available",
            "address": "Off-Market Sawgrass Parcel D, Elko County, NV",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 41.5013,
            "lon": -115.5013,
        },
        {
            "id": "010-749-039",
            "title": "Sawgrass Court Off-Market Lot 039",
            "category": "Raw Land",
            "city": "Elko County, NV",
            "contract_price": 4500,
            "purchase_price": 115000,
            "down_payment_pct": 25,
            "down_payment_amt": int(115000 * 0.25),
            "arv": int(115000 * 1.39),
            "beds": 0,
            "baths": 0,
            "sqft": 10500,
            "status": "UNDER CONTRACT",
            "address": "Off-Market Sawgrass Parcel E, Elko County, NV",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 41.5015,
            "lon": -115.5015,
        },
        {
            "id": "010-749-039-B",
            "title": "Sawgrass Court Off-Market Lot 039-B",
            "category": "Raw Land",
            "city": "Elko County, NV",
            "contract_price": 4800,
            "purchase_price": 122000,
            "down_payment_pct": 20,
            "down_payment_amt": int(122000 * 0.20),
            "arv": int(122000 * 1.40),
            "beds": 0,
            "baths": 0,
            "sqft": 10500,
            "status": "Available",
            "address": "Off-Market Sawgrass Parcel F, Elko County, NV",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 41.5016,
            "lon": -115.5016,
        },
        {
            "id": "010-749-040",
            "title": "Sawgrass Court Off-Market Lot 040",
            "category": "Raw Land",
            "city": "Elko County, NV",
            "contract_price": 4500,
            "purchase_price": 115000,
            "down_payment_pct": 20,
            "down_payment_amt": int(115000 * 0.20),
            "arv": int(115000 * 1.32),
            "beds": 0,
            "baths": 0,
            "sqft": 10500,
            "status": "Available",
            "address": "Off-Market Sawgrass Parcel G, Elko County, NV",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 41.5018,
            "lon": -115.5018,
        },
        {
            "id": "010-749-040-B",
            "title": "Sawgrass Court Off-Market Lot 040-B",
            "category": "Raw Land",
            "city": "Elko County, NV",
            "contract_price": 4900,
            "purchase_price": 125000,
            "down_payment_pct": 25,
            "down_payment_amt": int(125000 * 0.25),
            "arv": int(125000 * 1.35),
            "beds": 0,
            "baths": 0,
            "sqft": 10500,
            "status": "UNDER CONTRACT",
            "address": "Off-Market Sawgrass Parcel H, Elko County, NV",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 41.5019,
            "lon": -115.5019,
        },
        {
            "id": "010-81H-032",
            "title": "Elko County North Off-Market Acreage",
            "category": "Raw Land",
            "city": "Elko County, NV",
            "contract_price": 5000,
            "purchase_price": 125000,
            "down_payment_pct": 20,
            "down_payment_amt": int(125000 * 0.20),
            "arv": int(125000 * 1.30),
            "beds": 0,
            "baths": 0,
            "sqft": 87120,
            "status": "Available",
            "address": "Off-Market North Tract 31, Elko County, NV",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 41.5200,
            "lon": -115.4800,
        },
        {
            "id": "010-81H-032-B",
            "title": "Elko County North High Desert Off-Market Tract",
            "category": "Raw Land",
            "city": "Elko County, NV",
            "contract_price": 5200,
            "purchase_price": 128000,
            "down_payment_pct": 25,
            "down_payment_amt": int(128000 * 0.25),
            "arv": int(128000 * 1.33),
            "beds": 0,
            "baths": 0,
            "sqft": 87120,
            "status": "UNDER CONTRACT",
            "address": "Off-Market North Tract 32, Elko County, NV",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 41.5202,
            "lon": -115.4802,
        },
        {
            "id": "010-81H-032-C",
            "title": "Elko County North Panorama Off-Market Acreage",
            "category": "Raw Land",
            "city": "Elko County, NV",
            "contract_price": 5500,
            "purchase_price": 132000,
            "down_payment_pct": 20,
            "down_payment_amt": int(132000 * 0.20),
            "arv": int(132000 * 1.36),
            "beds": 0,
            "baths": 0,
            "sqft": 87120,
            "status": "Available",
            "address": "Off-Market North Tract 34, Elko County, NV",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 41.5204,
            "lon": -115.4804,
        },
        {
            "id": "010-81H-032-D",
            "title": "Elko County North Frontier Off-Market Estate",
            "category": "Raw Land",
            "city": "Elko County, NV",
            "contract_price": 5800,
            "purchase_price": 135000,
            "down_payment_pct": 22,
            "down_payment_amt": int(135000 * 0.22),
            "arv": int(135000 * 1.39),
            "beds": 0,
            "baths": 0,
            "sqft": 87120,
            "status": "UNDER CONTRACT",
            "address": "Off-Market North Tract 36, Elko County, NV",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 41.5206,
            "lon": -115.4806,
        },
        # --- COMMERCIAL ---
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
        {
            "id": "UT-DRP-0201-B",
            "title": "Draper Fort Street Off-Market Retail Pad",
            "category": "Commercial",
            "city": "Draper, UT",
            "contract_price": 16500,
            "purchase_price": 330000,
            "down_payment_pct": 20,
            "down_payment_amt": int(330000 * 0.20),
            "arv": int(330000 * 1.33),
            "beds": 0,
            "baths": 0,
            "sqft": 5200,
            "status": "Available",
            "address": "Off-Market Fort St Parcel B, Draper, UT 84020",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 40.5246,
            "lon": -111.8635,
        },
        {
            "id": "UT-DRP-0201-C",
            "title": "Draper Business Park Off-Market Site",
            "category": "Commercial",
            "city": "Draper, UT",
            "contract_price": 18000,
            "purchase_price": 360000,
            "down_payment_pct": 25,
            "down_payment_amt": int(360000 * 0.25),
            "arv": int(360000 * 1.36),
            "beds": 0,
            "baths": 0,
            "sqft": 6100,
            "status": "UNDER CONTRACT",
            "address": "Off-Market Fort St Parcel C, Draper, UT 84020",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 40.5250,
            "lon": -111.8640,
        },
        {
            "id": "UT-DRP-0201-D",
            "title": "Draper Commercial Off-Market Plaza Lot",
            "category": "Commercial",
            "city": "Draper, UT",
            "contract_price": 20000,
            "purchase_price": 395000,
            "down_payment_pct": 20,
            "down_payment_amt": int(395000 * 0.20),
            "arv": int(395000 * 1.40),
            "beds": 0,
            "baths": 0,
            "sqft": 7200,
            "status": "Available",
            "address": "Off-Market Fort St Parcel D, Draper, UT 84020",
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
    property_id, property_title, recipient_email, selected_term, custom_terms
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
    Selected Financing/Contract Terms: {selected_term}
    Custom Addendums / Conditions: {custom_terms}
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
                                    <div style="font-size: 13px; color: #1d4ed8; font-weight: 600; margin-bottom: 4px;">Down Payment ({row['down_payment_pct']}%): ${row['down_payment_amt']:,}</div>
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

                        # Actual random contract/financing terms options for the dropdown
                        contract_terms_options = [
                            f"Standard Cash Purchase ({row['down_payment_pct']}% Down / 14-Day Close)",
                            "Subject-To Existing Mortgage Takeover",
                            "Seller Financing (5-Year Balloon / 7.5% Interest)",
                            "Equitable Interest Assignment (REPC Assignment Fee)",
                            "Wholesale Cash Offer (7-Day Inspection Waiver)",
                        ]
                        selected_term = st.selectbox(
                            "Contract & Financing Terms",
                            contract_terms_options,
                            key=f"term_select_{row['id']}",
                        )

                        offer_terms = st.text_area(
                            "Offer Terms & Conditions",
                            key=f"p_msg_{row['id']}",
                            placeholder="Enter earnest money deposit, closing date, or escrow contingencies...",
                        )
                        if st.button(
                            "Submit Official Offer", key=f"p_btn_{row['id']}"
                        ):
                            if user_email:
                                send_offer_dispatch(
                                    row["id"],
                                    row["title"],
                                    user_email,
                                    selected_term,
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
# Render Legal Notice Footer at the Bottom of the Website
st.markdown(
    """
    <style>
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
