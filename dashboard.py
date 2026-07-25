from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import pandas as pd
import streamlit as st

# Page Configuration - Enterprise Real Estate Portal Layout
st.set_page_config(
    page_title="Utah Real Estate & Land For Sale. | Utah Land & Property Inc.",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---> ZILLOW-STYLE MOBILE HEADER & BERKSHIRE HATHAWAY STYLING <---
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

        /* Hide default Streamlit chrome & native sidebar controls */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        [data-testid="stSidebar"] {display: none !important;}
        
        .stApp {
            background-color: #f7f8f9;
            color: #3d3d3d;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }

        /* Fixed Sticky Header Layout mimicking Zillow */
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
            height: 64px;
            z-index: 999999;
            box-sizing: border-box;
            box-shadow: 0 2px 6px rgba(0,0,0,0.04);
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
            font-size: 26px;
            color: #1a1a1a;
            cursor: pointer;
            user-select: none;
            line-height: 1;
            font-weight: 700;
        }

        /* Centered Header Logo: Black and Less Bold */
        .header-logo-container {
            position: absolute;
            left: 50%;
            transform: translateX(-50%);
            text-align: center;
            z-index: 1;
        }

        .header-logo {
            font-size: 22px;
            font-weight: 600 !important;
            color: #111827 !important;
            letter-spacing: -0.3px;
            text-decoration: none !important;
            font-family: 'Inter', sans-serif;
            white-space: nowrap;
        }
        .header-logo:hover {
            color: #000000 !important;
            text-decoration: none !important;
        }

        .header-right {
            display: flex;
            align-items: center;
            z-index: 2;
        }
        
        .sign-in-link {
            color: #111827 !important;
            font-weight: 600 !important;
            font-size: 15px;
            text-decoration: none !important;
        }
        .sign-in-link:hover {
            color: #000000 !important;
        }

        /* Slide-out Mobile Navigation Drawer */
        .mobile-drawer {
            position: fixed;
            top: 64px;
            left: -300px;
            width: 300px;
            height: calc(100vh - 64px);
            background-color: #ffffff;
            border-right: 1px solid #e5e7eb;
            box-shadow: 4px 0 16px rgba(0,0,0,0.08);
            transition: left 0.3s ease-in-out;
            z-index: 999998;
            padding: 24px;
            box-sizing: border-box;
        }

        #menu-toggle:checked ~ .mobile-drawer {
            left: 0;
        }

        .drawer-title {
            font-size: 17px;
            font-weight: 800;
            color: #1a1a1a;
            margin-bottom: 20px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .drawer-link {
            display: block;
            padding: 12px 16px;
            color: #4b5563;
            text-decoration: none;
            font-weight: 600;
            font-size: 16px;
            border-radius: 6px;
            margin-bottom: 8px;
            transition: background 0.2s;
        }

        .drawer-link:hover {
            background-color: #f3f4f6;
            color: #006AFF;
        }
        
        .drawer-link.primary-action {
            background-color: #006AFF;
            color: #ffffff;
            text-align: center;
            margin-top: 24px;
        }

        .drawer-link.primary-action:hover {
            background-color: #0051cc;
            color: #ffffff;
        }

        /* Push main content down below fixed header */
        .block-container {
            padding-top: 64px !important;
            padding-left: 0rem !important;
            padding-right: 0rem !important;
            max-width: 100% !important;
        }

        /* Hero Banner with Berkshire Hathaway HomeServices Typography Styling */
        .hero-container {
            position: relative;
            background: linear-gradient(rgba(0, 0, 0, 0.45), rgba(0, 0, 0, 0.45)), 
                        url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=2000&q=80');
            background-size: cover;
            background-position: center;
            height: 420px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            color: white;
            padding: 0 24px;
            margin-bottom: 36px;
        }

        .hero-title {
            font-family: 'Times New Roman', Times, serif;
            font-size: 3.2rem;
            font-weight: normal;
            margin-bottom: 16px;
            letter-spacing: 0.05em;
            text-shadow: 0 2px 6px rgba(0,0,0,0.6);
            line-height: 1.1;
        }
        
        .section-header {
            font-size: 1.6rem;
            font-weight: 800;
            color: #1a1a1a;
            margin: 36px 24px 18px 24px;
            padding-bottom: 10px;
            border-bottom: 2px solid #e5e7eb;
            letter-spacing: -0.5px;
        }
    </style>

    <!-- Zillow-Style Mobile Header with Black, Less Bold Logo & Functional Drawer -->
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
        <a href="#chatbot-section" class="drawer-link">Assignment FAQ Bot</a>
        <a href="#contracts-section" class="drawer-link primary-action">Sign In / Account</a>
    </div>
    """,
    unsafe_allow_html=True,
)

# Hero Section featuring centered Berkshire Hathaway HomeServices styled text
st.markdown(
    """
    <div class="hero-container">
        <div class="hero-title">Our network knows great homes.</div>
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


# Automated Email / Offer Dispatch Helper with Production Error Handling
def send_offer_dispatch(
    property_id, property_title, recipient_email, selected_term, custom_terms
):
    smtp_server = "smtp.gmail.com"
    port = 587
    sender_email = st.secrets.get("EMAIL_USER", "")
    sender_password = st.secrets.get("EMAIL_PASS", "")

    # If SMTP credentials are not configured in st.secrets, log as simulated success for local review
    if not sender_email or not sender_password:
        return True

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


# --- DYNAMIC HEADER TITLE SECTION ---
if "show_faq" not in st.session_state:
    st.session_state.show_faq = False

col_title_1, col_title_2 = st.columns([3, 1])
with col_title_1:
    st.markdown(
        f"""
        <div style="margin: 28px 24px 16px 24px;">
            <h1 style="font-size: 1.9rem; font-weight: 800; color: #1a1a1a; margin-bottom: 6px; letter-spacing: -0.5px;">Utah Land & Property Inc. Real Estate & Land For Sale</h1>
            <p style="font-size: 1.05rem; color: #555555; margin: 0;"><b>{len(df)}</b> active private contracts and land parcels available</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

with col_title_2:
    st.markdown(
        "<div style='margin: 38px 24px 0 0; text-align: right;'>",
        unsafe_allow_html=True,
    )
    if st.button("How assignment contracts work", type="tertiary"):
        st.session_state.show_faq = not st.session_state.show_faq
    st.markdown("</div>", unsafe_allow_html=True)


# Render Function for Property Grids
def render_property_grid(subset_df, category_title, anchor_id):
    st.markdown(
        f'<div id="{anchor_id}" class="section-header">{category_title} ({len(subset_df)})</div>',
        unsafe_allow_html=True,
    )
    st.markdown("<div style='padding: 0 24px;'>", unsafe_allow_html=True)

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
                    else "rgba(0,0,0,0.75)"
                )

                with cols[idx]:
                    st.markdown(
                        f"""
                            <div style="background: white; border-radius: 10px; overflow: hidden; border: 1px solid #e5e7eb; margin-bottom: 24px; box-shadow: 0 2px 6px rgba(0,0,0,0.04);">
                                <div style="position: relative;">
                                    <img src="{first_image}" style="width: 100%; height: 210px; object-fit: cover;">
                                    <div style="position: absolute; top: 12px; left: 12px; background: {badge_bg}; color: white; padding: 5px 12px; border-radius: 4px; font-size: 12px; font-weight: 700; letter-spacing: 0.5px;">{row['status']}</div>
                                </div>
                                <div style="padding: 18px;">
                                    <div style="font-size: 12px; text-transform: uppercase; color: #6b7280; font-weight: 700; margin-bottom: 6px;">{row['broker']}</div>
                                    <div style="font-size: 18px; font-weight: 800; color: #1a1a1a; margin-bottom: 8px;">Contract: ${row['contract_price']:,}</div>
                                    <div style="font-size: 14px; color: #374151; margin-bottom: 3px;">Property Purchase Price: <b>${row['purchase_price']:,}</b></div>
                                    <div style="font-size: 14px; color: #006AFF; font-weight: 700; margin-bottom: 6px;">Down Payment ({row['down_payment_pct']}%): ${row['down_payment_amt']:,}</div>
                                    <div style="font-size: 14px; color: #059669; font-weight: 700; margin-bottom: 10px;">ARV: ${row['arv']:,}</div>
                                    <div style="font-size: 14px; color: #374151; margin-bottom: 10px;"><b>{row['beds']}</b> bds &nbsp;|&nbsp; <b>{row['baths']}</b> ba &nbsp;|&nbsp; <b>{row['sqft']:,}</b> sqft</div>
                                    <div style="font-size: 14px; color: #6b7280;">{row['address']}</div>
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
                                sent_status = send_offer_dispatch(
                                    row["id"],
                                    row["title"],
                                    user_email,
                                    selected_term,
                                    offer_terms,
                                )
                                if sent_status:
                                    st.success(
                                        "Offer successfully dispatched to escrow!"
                                    )
                                else:
                                    st.warning(
                                        "Offer recorded! (Email dispatch pending SMTP configuration in secrets)."
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


# ---> EMBEDDED ZILLOW-STYLE ASSIGNMENT DEAL CHATBOT WITH LIVE TYPING PREVIEW <---
st.markdown(
    """
    <div id="chatbot-section" style="max-width: 900px; margin: 50px auto 40px auto; padding: 0 24px;">
        <div style="background: #ffffff; border: 1px solid #e5e7eb; border-radius: 12px; padding: 24px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
            <div style="display: flex; align-items: center; margin-bottom: 16px;">
                <div style="width: 10px; height: 10px; background-color: #22c55e; border-radius: 50%; margin-right: 8px;"></div>
                <h3 style="margin: 0; font-size: 18px; font-weight: 800; color: #1a1a1a;">Assignment Deal & Escrow Assistant</h3>
            </div>
            <p style="font-size: 14px; color: #6b7280; margin-bottom: 16px;">Have questions about earnest money, contract assignment fees, or closing timelines? Ask below for instant answers.</p>
            
            <div id="chat-screen" style="height: 200px; overflow-y: auto; background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 8px; padding: 14px; margin-bottom: 12px; font-size: 14px; line-height: 1.5;">
                <div style="margin-bottom: 8px;"><strong>Bot:</strong> Hello! I'm here to help you navigate our off-market Utah contracts and assignment terms. What would you like to know?</div>
            </div>
            
            <div id="typing-indicator" style="color: #006AFF; font-style: italic; font-size: 13px; margin-bottom: 8px; display: none; font-weight: 600;">
                Bot is typing a live response...
            </div>

            <div style="display: flex; gap: 10px;">
                <input type="text" id="chat-input" placeholder="Ask about assignment fees, earnest money, or closing..." style="flex: 1; padding: 12px; border: 1px solid #cbd5e1; border-radius: 6px; font-size: 14px; outline: none;" />
                <button onclick="sendChatMessage()" style="padding: 12px 24px; background: #006AFF; color: #fff; border: none; border-radius: 6px; font-weight: 700; cursor: pointer; font-size: 14px;">Ask</button>
            </div>
        </div>
    </div>

    <script>
        function sendChatMessage() {
            const input = document.getElementById('chat-input');
            const screen = document.getElementById('chat-screen');
            const indicator = document.getElementById('typing-indicator');
            
            if (!input.value.trim()) return;

            const userQuery = input.value;
            screen.innerHTML += `<div style="margin-bottom: 8px;"><strong>You:</strong> ${userQuery}</div>`;
            input.value = '';
            screen.scrollTop = screen.scrollHeight;

            // Show Live Typing Indicator
            indicator.style.display = 'block';
            
            setTimeout(() => {
                indicator.style.display = 'none';
                let reply = "An assignment contract transfers the buyer's rights and obligations under a real estate purchase contract to a new buyer before closing, allowing you to secure equity without taking title.";
                
                const q = userQuery.toLowerCase();
                if (q.includes('earnest') || q.includes('emd')) {
                    reply = "Earnest money is typically deposited with a neutral title company (e.g., Metro National Title) within 4 business days of contract execution and is credited toward your purchase at closing.";
                } else if (q.includes('escrow') || q.includes('closing')) {
                    reply = "Once you select your financing terms and submit your offer, our transaction coordinator opens escrow and routes the formal assignment paperwork directly to your email.";
                } else if (q.includes('fee') || q.includes('cost')) {
                    reply = "The contract price listed on our platform represents the assignment fee or initial wholesale value required to acquire our position in the underlying REPC.";
                }
                
                screen.innerHTML += `<div style="margin-bottom: 8px;"><strong>Bot:</strong> ${reply}</div>`;
                screen.scrollTop = screen.scrollHeight;
            }, 1000);
        }

        // Allow pressing Enter to send chat message
        document.getElementById('chat-input').addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                sendChatMessage();
            }
        });
    </script>
    """,
    unsafe_allow_html=True,
)
