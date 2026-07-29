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

# ---> AUTHENTICATION SESSION STATE SETUP <---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

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

        /* Immersive Style Hero Banner */
        .hero-container {
            position: relative;
            background: linear-gradient(rgba(0, 0, 0, 0.45), rgba(0, 0, 0, 0.45)), 
                        url('https://images.unsplash.com/photo-1450133064473-71024230f91b?auto=format&fit=crop&w=2000&q=80');
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
            font-size: 55px;
            font-weight: 975;
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
        <a href="#residential-section" class="drawer-link">Residential Contracts</a>
        <a href="#raw-land-section" class="drawer-link">Raw Land Contracts</a>
        <a href="#commercial-section" class="drawer-link">Commercial Contracts</a>
        <a href="#contracts-section" class="drawer-link primary-action">Sign In / Account</a>
    </div>
    """,
    unsafe_allow_html=True,
)

# Hero Section Focused on Equitable Interest & Contract Assignment
st.markdown(
    """
    <div class="hero-container">
        <div class="hero-title">Utah Land & Property Inc.</div>
        <div class="hero-subtitle">Wholesale Real Estate Contract Assignments & Equitable Interest Opportunities in Utah</div>
        <div class="hero-subtitle">We are not real estate agents or brokers. We market our equitable interest in signed purchase contracts.</div>
        <div class="hero-subtitle">Enter your email and investor access code to review available contract assignments.</div>
    </div>
    <div id="contracts-section"></div>
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
    
    st.stop()  # Halts execution until authenticated

# Contract Assignment Database (Focusing strictly on contractual rights, no residential street addresses or property structural specs)
@st.cache_data
def load_utah_property_database():
    data = [
        # --- RESIDENTIAL CONTRACTS ---
        {
            "id": "UT-MIL-0101",
            "title": "ASSIGNMENT OF PURCHASE CONTRACT. Equitable Interest, Utah Land & Property Inc. is selling contractual rights to purchase a single family property, Millcreek 84117, Contract Purchase Price $165,000 and Assignment Fee: $10,000 Estimated ARV Price: $217,800",
            "category": "Residential",
            "city": "Millcreek, UT",
            "contract_price": 5000,
            "purchase_price": 165000,
            "arv": 217800,
            "status": "UNDER CONTRACT",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1450133064473-71024230f91b?auto=format&fit=crop&w=800&q=80",
            "lat": 40.6977,
            "lon": -111.8550,
        },
        {
            "id": "UT-MIL-0101-B",
            "title": "ASSIGNMENT OF PURCHASE CONTRACT. Equitable Interest, Utah Land & Property Inc. is selling contractual rights to purchase a single family property, Salt Lake City 84109, Contract Purchase Price $590,000 and Assignment Fee: $10,000 Estimated ARV Price: $796,500",
            "category": "Residential",
            "city": "Millcreek, UT",
            "contract_price": 27000,
            "purchase_price": 590000,
            "arv": 796500,
            "status": "UNDER CONTRACT",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?auto=format&fit=crop&w=800&q=80",
            "lat": 40.6979,
            "lon": -111.8552,
        },
        {
            "id": "UT-MIL-0101-C",
            "title": "ASSIGNMENT OF PURCHASE CONTRACT. Equitable Interest, Utah Land & Property Inc. is selling contractual rights to purchase a single family property, Millcreek 84109, Contract Purchase Price $210,000 and Assignment Fee: $10,000 Estimated ARV Price: $289,800",
            "category": "Residential",
            "city": "Millcreek, UT",
            "contract_price": 7500,
            "purchase_price": 210000,
            "arv": 289800,
            "status": "UNDER CONTRACT",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1450133064473-71024230f91b?auto=format&fit=crop&w=800&q=80",
            "lat": 40.6985,
            "lon": -111.8560,
        },
        {
            "id": "UT-MIL-0101-D",
            "title": "ASSIGNMENT OF PURCHASE CONTRACT. Equitable Interest, Utah Land & Property Inc. is selling contractual rights to purchase a single family property, Millcreek 84109, Contract Purchase Price $235,000 and Assignment Fee: $10,000 Estimated ARV Price: $329,000",
            "category": "Residential",
            "city": "Millcreek, UT",
            "contract_price": 8500,
            "purchase_price": 235000,
            "arv": 329000,
            "status": "Available",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?auto=format&fit=crop&w=800&q=80",
            "lat": 40.6990,
            "lon": -111.8570,
        },
        {
            "id": "UT-MIL-0102",
            "title": "ASSIGNMENT OF PURCHASE CONTRACT. Equitable Interest, Utah Land & Property Inc. is selling contractual rights to purchase a single family property, Millcreek 84109, Contract Purchase Price $420,000 and Assignment Fee: $10,000 Estimated ARV Price: $546,000",
            "category": "Residential",
            "city": "Millcreek, UT",
            "contract_price": 12000,
            "purchase_price": 420000,
            "arv": 546000,
            "status": "Available",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1450133064473-71024230f91b?auto=format&fit=crop&w=800&q=80",
            "lat": 40.7012,
            "lon": -111.8670,
        },
        {
            "id": "UT-MIL-0102-B",
            "title": "ASSIGNMENT OF PURCHASE CONTRACT. Equitable Interest, Utah Land & Property Inc. is selling contractual rights to purchase a single family property, Millcreek 84124, Contract Purchase Price $450,000 and Assignment Fee: $10,000 Estimated ARV Price: $598,500",
            "category": "Residential",
            "city": "Millcreek, UT",
            "contract_price": 14000,
            "purchase_price": 450000,
            "arv": 598500,
            "status": "Available",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?auto=format&fit=crop&w=800&q=80",
            "lat": 40.7015,
            "lon": -111.8675,
        },
        {
            "id": "UT-MIL-0102-C",
            "title": "ASSIGNMENT OF PURCHASE CONTRACT. Equitable Interest, Utah Land & Property Inc. is selling contractual rights to purchase a single family property, Millcreek 84124, Contract Purchase Price $480,000 and Assignment Fee: $10,000 Estimated ARV Price: $652,800",
            "category": "Residential",
            "city": "Millcreek, UT",
            "contract_price": 15000,
            "purchase_price": 480000,
            "arv": 652800,
            "status": "UNDER CONTRACT",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1450133064473-71024230f91b?auto=format&fit=crop&w=800&q=80",
            "lat": 40.7018,
            "lon": -111.8680,
        },
        {
            "id": "UT-MIL-0102-D",
            "title": "ASSIGNMENT OF PURCHASE CONTRACT. Equitable Interest, Utah Land & Property Inc. is selling contractual rights to purchase a single family property, Millcreek 84124, Contract Purchase Price $510,000 and Assignment Fee: $10,000 Estimated ARV Price: $708,900",
            "category": "Residential",
            "city": "Millcreek, UT",
            "contract_price": 16000,
            "purchase_price": 510000,
            "arv": 708900,
            "status": "Available",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?auto=format&fit=crop&w=800&q=80",
            "lat": 40.7020,
            "lon": -111.8685,
        },
        {
            "id": "UT-CLK-0301",
            "title": "ASSIGNMENT OF PURCHASE CONTRACT. Equitable Interest, Utah Land & Property Inc. is selling contractual rights to purchase a single family property, Clearfield 84015, Contract Purchase Price $285,000 and Assignment Fee: $10,000 Estimated ARV Price: $364,800",
            "category": "Residential",
            "city": "Clearfield, UT",
            "contract_price": 8000,
            "purchase_price": 285000,
            "arv": 364800,
            "status": "Available",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1450133064473-71024230f91b?auto=format&fit=crop&w=800&q=80",
            "lat": 41.1118,
            "lon": -112.2426,
        },
        {
            "id": "UT-CLK-0301-B",
            "title": "ASSIGNMENT OF PURCHASE CONTRACT. Equitable Interest, Utah Land & Property Inc. is selling contractual rights to purchase a single family property, Clearfield 84015, Contract Purchase Price $295,000 and Assignment Fee: $10,000 Estimated ARV Price: $386,450",
            "category": "Residential",
            "city": "Clearfield, UT",
            "contract_price": 8500,
            "purchase_price": 295000,
            "arv": 386450,
            "status": "UNDER CONTRACT",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?auto=format&fit=crop&w=800&q=80",
            "lat": 41.1120,
            "lon": -112.2430,
        },
        {
            "id": "UT-CLK-0301-C",
            "title": "ASSIGNMENT OF PURCHASE CONTRACT. Equitable Interest, Utah Land & Property Inc. is selling contractual rights to purchase a single family property, Clearfield 84015, Contract Purchase Price $310,000 and Assignment Fee: $10,000 Estimated ARV Price: $415,400",
            "category": "Residential",
            "city": "Clearfield, UT",
            "contract_price": 9000,
            "purchase_price": 310000,
            "arv": 415400,
            "status": "Available",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1450133064473-71024230f91b?auto=format&fit=crop&w=800&q=80",
            "lat": 41.1125,
            "lon": -112.2435,
        },
        {
            "id": "UT-CLK-0301-D",
            "title": "ASSIGNMENT OF PURCHASE CONTRACT. Equitable Interest, Utah Land & Property Inc. is selling contractual rights to purchase a single family property, Clearfield 84015, Contract Purchase Price $325,000 and Assignment Fee: $10,000 Estimated ARV Price: $445,250",
            "category": "Residential",
            "city": "Clearfield, UT",
            "contract_price": 9500,
            "purchase_price": 325000,
            "arv": 445250,
            "status": "UNDER CONTRACT",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?auto=format&fit=crop&w=800&q=80",
            "lat": 41.1130,
            "lon": -112.2440,
        },
        # --- RAW LAND CONTRACTS ---
        {
            "id": "010-59G-008",
            "title": "ASSIGNMENT OF PURCHASE CONTRACT. Equitable Interest, Utah Land & Property Inc. is selling contractual rights to purchase land, Elko County 89801, Contract Purchase Price $95,000 and Assignment Fee: $10,000 Estimated ARV Price: $123,500",
            "category": "Raw Land",
            "city": "Elko County, NV",
            "contract_price": 4500,
            "purchase_price": 95000,
            "arv": 123500,
            "status": "UNDER CONTRACT",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 41.5000,
            "lon": -115.5000,
        },
        {
            "id": "010-59G-008-B",
            "title": "ASSIGNMENT OF PURCHASE CONTRACT. Equitable Interest, Utah Land & Property Inc. is selling contractual rights to purchase land, Elko County 89801, Contract Purchase Price $98,000 and Assignment Fee: $10,000 Estimated ARV Price: $128,740",
            "category": "Raw Land",
            "city": "Elko County, NV",
            "contract_price": 4800,
            "purchase_price": 98000,
            "arv": 128740,
            "status": "Available",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 41.5002,
            "lon": -115.5002,
        },
        {
            "id": "010-59G-008-C",
            "title": "ASSIGNMENT OF PURCHASE CONTRACT. Equitable Interest, Utah Land & Property Inc. is selling contractual rights to purchase land, Elko County 89801, Contract Purchase Price $102,000 and Assignment Fee: $10,000 Estimated ARV Price: $137,700",
            "category": "Raw Land",
            "city": "Elko County, NV",
            "contract_price": 5000,
            "purchase_price": 102000,
            "arv": 137700,
            "status": "UNDER CONTRACT",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 41.5004,
            "lon": -115.5004,
        },
        {
            "id": "010-59G-008-D",
            "title": "ASSIGNMENT OF PURCHASE CONTRACT. Equitable Interest, Utah Land & Property Inc. is selling contractual rights to purchase land, Elko County 89801, Contract Purchase Price $105,000 and Assignment Fee: $10,000 Estimated ARV Price: $144,900",
            "category": "Raw Land",
            "city": "Elko County, NV",
            "contract_price": 5200,
            "purchase_price": 105000,
            "arv": 144900,
            "status": "Available",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 41.5006,
            "lon": -115.5006,
        },
        {
            "id": "010-749-036",
            "title": "ASSIGNMENT OF PURCHASE CONTRACT. Equitable Interest, Utah Land & Property Inc. is selling contractual rights to purchase land, Elko County 89801, Contract Purchase Price $115,000 and Assignment Fee: $10,000 Estimated ARV Price: $147,200",
            "category": "Raw Land",
            "city": "Elko County, NV",
            "contract_price": 4500,
            "purchase_price": 115000,
            "arv": 147200,
            "status": "Available",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 41.5010,
            "lon": -115.5010,
        },
        {
            "id": "010-749-036-B",
            "title": "ASSIGNMENT OF PURCHASE CONTRACT. Equitable Interest, Utah Land & Property Inc. is selling contractual rights to purchase land, Elko County 89801, Contract Purchase Price $118,000 and Assignment Fee: $10,000 Estimated ARV Price: $154,580",
            "category": "Raw Land",
            "city": "Elko County, NV",
            "contract_price": 4600,
            "purchase_price": 118000,
            "arv": 154580,
            "status": "UNDER CONTRACT",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 41.5011,
            "lon": -115.5011,
        },
        {
            "id": "010-749-037",
            "title": "ASSIGNMENT OF PURCHASE CONTRACT. Equitable Interest, Utah Land & Property Inc. is selling contractual rights to purchase land, Elko County 89801, Contract Purchase Price $115,000 and Assignment Fee: $10,000 Estimated ARV Price: $154,100",
            "category": "Raw Land",
            "city": "Elko County, NV",
            "contract_price": 4500,
            "purchase_price": 115000,
            "arv": 154100,
            "status": "Available",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 41.5012,
            "lon": -115.5012,
        },
        {
            "id": "010-749-037-B",
            "title": "ASSIGNMENT OF PURCHASE CONTRACT. Equitable Interest, Utah Land & Property Inc. is selling contractual rights to purchase land, Elko County 89801, Contract Purchase Price $120,000 and Assignment Fee: $10,000 Estimated ARV Price: $163,200",
            "category": "Raw Land",
            "city": "Elko County, NV",
            "contract_price": 4700,
            "purchase_price": 120000,
            "arv": 163200,
            "status": "Available",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 41.5013,
            "lon": -115.5013,
        },
        {
            "id": "010-749-039",
            "title": "ASSIGNMENT OF PURCHASE CONTRACT. Equitable Interest, Utah Land & Property Inc. is selling contractual rights to purchase land, Elko County 89801, Contract Purchase Price $115,000 and Assignment Fee: $10,000 Estimated ARV Price: $159,850",
            "category": "Raw Land",
            "city": "Elko County, NV",
            "contract_price": 4500,
            "purchase_price": 115000,
            "arv": 159850,
            "status": "UNDER CONTRACT",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 41.5015,
            "lon": -115.5015,
        },
        {
            "id": "010-749-039-B",
            "title": "ASSIGNMENT OF PURCHASE CONTRACT. Equitable Interest, Utah Land & Property Inc. is selling contractual rights to purchase land, Elko County 89801, Contract Purchase Price $122,000 and Assignment Fee: $10,000 Estimated ARV Price: $170,800",
            "category": "Raw Land",
            "city": "Elko County, NV",
            "contract_price": 4800,
            "purchase_price": 122000,
            "arv": 170800,
            "status": "Available",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 41.5016,
            "lon": -115.5016,
        },
        {
            "id": "010-749-040",
            "title": "ASSIGNMENT OF PURCHASE CONTRACT. Equitable Interest, Utah Land & Property Inc. is selling contractual rights to purchase land, Elko County 89801, Contract Purchase Price $115,000 and Assignment Fee: $10,000 Estimated ARV Price: $148,350",
            "category": "Raw Land",
            "city": "Elko County, NV",
            "contract_price": 4500,
            "purchase_price": 115000,
            "arv": 148350,
            "status": "Available",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 41.5018,
            "lon": -115.5018,
        },
        {
            "id": "010-749-040-B",
            "title": "ASSIGNMENT OF PURCHASE CONTRACT. Equitable Interest, Utah Land & Property Inc. is selling contractual rights to purchase land, Elko County 89801, Contract Purchase Price $125,000 and Assignment Fee: $10,000 Estimated ARV Price: $168,750",
            "category": "Raw Land",
            "city": "Elko County, NV",
            "contract_price": 4900,
            "purchase_price": 125000,
            "arv": 168750,
            "status": "UNDER CONTRACT",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 41.5019,
            "lon": -115.5019,
        },
        {
            "id": "010-81H-032",
            "title": "ASSIGNMENT OF PURCHASE CONTRACT. Equitable Interest, Utah Land & Property Inc. is selling contractual rights to purchase land, Elko County 89801, Contract Purchase Price $125,000 and Assignment Fee: $10,000 Estimated ARV Price: $162,500",
            "category": "Raw Land",
            "city": "Elko County, NV",
            "contract_price": 5000,
            "purchase_price": 125000,
            "arv": 162500,
            "status": "Available",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 41.5200,
            "lon": -115.4800,
        },
        {
            "id": "010-81H-032-B",
            "title": "ASSIGNMENT OF PURCHASE CONTRACT. Equitable Interest, Utah Land & Property Inc. is selling contractual rights to purchase land, Elko County 89801, Contract Purchase Price $128,000 and Assignment Fee: $10,000 Estimated ARV Price: $172,240",
            "category": "Raw Land",
            "city": "Elko County, NV",
            "contract_price": 5200,
            "purchase_price": 128000,
            "arv": 172240,
            "status": "UNDER CONTRACT",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 41.5202,
            "lon": -115.4802,
        },
        {
            "id": "010-81H-032-C",
            "title": "ASSIGNMENT OF PURCHASE CONTRACT. Equitable Interest, Utah Land & Property Inc. is selling contractual rights to purchase land, Elko County 89801, Contract Purchase Price $132,000 and Assignment Fee: $10,000 Estimated ARV Price: $179,520",
            "category": "Raw Land",
            "city": "Elko County, NV",
            "contract_price": 5500,
            "purchase_price": 132000,
            "arv": 179520,
            "status": "Available",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 41.5204,
            "lon": -115.4804,
        },
        {
            "id": "010-81H-032-D",
            "title": "ASSIGNMENT OF PURCHASE CONTRACT. Equitable Interest, Utah Land & Property Inc. is selling contractual rights to purchase land, Elko County 89801, Contract Purchase Price $135,000 and Assignment Fee: $10,000 Estimated ARV Price: $187,650",
            "category": "Raw Land",
            "city": "Elko County, NV",
            "contract_price": 5800,
            "purchase_price": 135000,
            "arv": 187650,
            "status": "UNDER CONTRACT",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 41.5206,
            "lon": -115.4806,
        },
        # --- COMMERCIAL CONTRACTS ---
        {
            "id": "UT-DRP-0201",
            "title": "ASSIGNMENT OF PURCHASE CONTRACT. Equitable Interest, Utah Land & Property Inc. is selling contractual rights to purchase commercial property, Draper 84020, Contract Purchase Price $310,000 and Assignment Fee: $10,000 Estimated ARV Price: $403,000",
            "category": "Commercial",
            "city": "Draper, UT",
            "contract_price": 15000,
            "purchase_price": 310000,
            "arv": 403000,
            "status": "UNDER CONTRACT",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=800&q=80",
            "lat": 40.5243,
            "lon": -111.8631,
        },
        {
            "id": "UT-DRP-0201-B",
            "title": "ASSIGNMENT OF PURCHASE CONTRACT. Equitable Interest, Utah Land & Property Inc. is selling contractual rights to purchase commercial property, Draper 84020, Contract Purchase Price $330,000 and Assignment Fee: $10,000 Estimated ARV Price: $438,900",
            "category": "Commercial",
            "city": "Draper, UT",
            "contract_price": 16500,
            "purchase_price": 330000,
            "arv": 438900,
            "status": "Available",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=800&q=80",
            "lat": 40.5,
            "lon": -111.86
        }
    ]
    return data
