from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import randomfrom email import encoders
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

        /* Immersive Zillow-Style Hero Banner with Bolder, Larger Text */
        .hero-container {
            position: relative;
            background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), 
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
            padding: 0 20px;
            margin-bottom: 30px;
        }

        .hero-title {
            font-size: 56px;
            font-weight: 900;
            margin-bottom: 16px;
            letter-spacing: -0.5px;
            text-shadow: 0 4px 12px rgba(0,0,0,0.7);
            font-family: 'Inter', sans-serif;
            line-height: 1.1;
            color: #ffffff;
        }

        .hero-subtitle {
            font-size: 24px;
            font-weight: 800;
            margin-bottom: 24px;
            text-shadow: 0 3px 8px rgba(0,0,0,0.7);
            letter-spacing: 0.5px;
            color: #f3f4f6;
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

# Friendly Zillow-Inspired Hero Section with Bolder, Larger Text
st.markdown(
    """
    <div class="hero-container">
        <div class="hero-title">Investments. Land. Utah Real Estate.</div>
        <div class="hero-subtitle">Assignment of Contracts & Off-Market Properties</div>
    </div>
    <div id="contracts-section"></div>
    """,
    unsafe_allow_html=True,
)

# --- MINI CHATBOT FOR ASSIGNMENT OF CONTRACTS & OFF-MARKET PROPERTIES ---
st.markdown(
    "<div style='padding: 0 20px;'><h3 style='font-weight: 800; color: #111827;'>💬 Contract & Property Assistant</h3>"
    "<p style='color: #4b5563; font-size: 14px;'>Ask any question about assignment fees, earnest money, off-market property vetting, or Utah contract procedures!</p></div>",
    unsafe_allow_html=True
)

if "chatbot_messages" not in st.session_state:
    st.session_state.chatbot_messages = [
        {"role": "assistant", "content": "Hello! I am your Utah Real Estate Assistant. How can I help you understand our off-market properties or assignment of contracts today?"}
    ]

chat_container = st.container()
with chat_container:
    chat_box = st.container(height=250)
    with chat_box:
        for msg in st.session_state.chatbot_messages:
            if msg["role"] == "user":
                st.markdown(f"**You:** {msg['content']}")
            else:
                st.markdown(f"**Bot:** {msg['content']}")

# User input widget for the mini chatbot
user_chat_input = st.text_input("Ask a question about contracts or off-market deals...", key="contract_chat_input")

if st.button("Send Query", key="send_chat_btn"):
    if user_chat_input.strip():
        user_query = user_chat_input.strip()
        st.session_state.chatbot_messages.append({"role": "user", "content": user_query})
        
        # Rule-based intelligent responses for assignment of contracts and off-market deals
        query_lower = user_query.lower()
        if "assignment" in query_lower or "contract" in query_lower:
            bot_reply = "An assignment of contract allows you to transfer your rights and obligations under a purchase agreement to an end buyer for an assignment fee. All our contracts feature clean title documentation and transparent earnest money terms."
        elif "off-market" in query_lower or "property" in query_lower:
            bot_reply = "Our off-market properties (including Millcreek residential parcels and Utah land tracts) are secured under exclusive purchase contracts, offering strong appreciation potential and flexible down payment options (20-25%)."
        elif "earnest" in query_lower or "deposit" in query_lower:
            bot_reply = "Earnest money deposits are securely held in title/escrow as outlined in the specific purchase agreement terms for each parcel."
        else:
            bot_reply = f"Thanks for asking about '{user_query}!' Our team specializes in exclusive Utah real estate contracts. Feel free to review our active inventory below or reach out directly for full disclosures!"
            
        st.session_state.chatbot_messages.append({"role": "assistant", "content": bot_reply})
        st.rerun()

st.markdown("<hr style='margin: 30px 0; border: none; border-top: 1px solid #e5e7eb;'>", unsafe_allow_html=True)


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
        }
    ]
    return data

properties = load_utah_property_database()

# Display Property Feed
st.markdown("<div class='section-header' id='residential-section'>Active Exclusive Contracts & Properties</div>", unsafe_allow_html=True)

for prop in properties:
    with st.container():
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(prop["image"], use_column_width=True)
        with col2:
            st.subheader(prop["title"])
            st.markdown(f"**Address:** {prop['address']}")
            st.markdown(f"**Purchase Price:** ${prop['purchase_price']:,} | **Down Payment ({prop['down_payment_pct']}%):** ${prop['down_payment_amt']:,}")
            st.markdown(f"**Assignment Fee / Contract Price:** ${prop['contract_price']:,} | **Status:** `{prop['status']}`")
            st.markdown(f"*Beds:* {prop.get('beds', 'N/A')} | *Baths:* {prop.get('baths', 'N/A')} | *SqFt:* {prop.get('sqft', 'N/A')}")
        st.markdown("<hr style='margin: 20px 0; border: none; border-top: 1px solid #e5e7eb;'>", unsafe_allow_html=True)
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

        /* Immersive Zillow-Style Hero Banner */
        .hero-container {
            position: relative;
            background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), 
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
            font-size: 50px;
            font-weight: 900;
            margin-bottom: 14px;
            letter-spacing: -0.5px;
            text-shadow: 0 4px 8px rgba(0,0,0,0.6);
            font-family: 'Inter', sans-serif;
            line-height: 1.1;
            color: #ffffff;
        }

        .hero-subtitle {
            font-size: 22px;
            font-weight: 800;
            margin-bottom: 24px;
            text-shadow: 0 3px 6px rgba(0,0,0,0.6);
            letter-spacing: 0.5px;
            color: #f3f4f6;
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

# Friendly Zillow-Inspired Hero Section with Bolder, Larger Text
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

# --- MINI CHATBOT FOR ASSIGNMENT OF CONTRACTS & OFF-MARKET PROPERTIES ---
st.markdown(
    "<div style='padding: 0 20px;'><h3 style='font-weight: 800; color: #111827;'>💬 Contract & Property Assistant</h3>"
    "<p style='color: #4b5563; font-size: 14px;'>Ask any question about assignment fees, earnest money, off-market property vetting, or Utah contract procedures!</p></div>",
    unsafe_allow_html=True
)

if "chatbot_messages" not in st.session_state:
    st.session_state.chatbot_messages = [
        {"role": "assistant", "content": "Hello! I am your Utah Real Estate Assistant. How can I help you understand our off-market properties or assignment of contracts today?"}
    ]

chat_container = st.container()
with chat_container:
    chat_box = st.container(height=250)
    with chat_box:
        for msg in st.session_state.chatbot_messages:
            if msg["role"] == "user":
                st.markdown(f"**You:** {msg['content']}")
            else:
                st.markdown(f"**Bot:** {msg['content']}")

# User input widget for the mini chatbot
user_chat_input = st.text_input("Ask a question about contracts or off-market deals...", key="contract_chat_input")

if st.button("Send Query", key="send_chat_btn"):
    if user_chat_input.strip():
        user_query = user_chat_input.strip()
        st.session_state.chatbot_messages.append({"role": "user", "content": user_query})
        
        # Simple rule-based intelligent responses for assignment of contracts and off-market deals
        query_lower = user_query.lower()
        if "assignment" in query_lower or "contract" in query_lower:
            bot_reply = "An assignment of contract allows you to transfer your rights and obligations under a purchase agreement to an end buyer for an assignment fee. All our contracts feature clean title documentation and transparent earnest money terms."
        elif "off-market" in query_lower or "property" in query_lower:
            bot_reply = "Our off-market properties (including Millcreek residential parcels and Elko County land tracts) are secured under exclusive purchase contracts, offering strong appreciation potential and flexible down payment options (20-25%)."
        elif "earnest" in query_lower or "deposit" in query_lower:
            bot_reply = "Earnest money deposits are securely held in title/escrow as outlined in the specific purchase agreement terms for each parcel."
        else:
            bot_reply = f"Thanks for asking about '{user_query}!' Our team specializes in exclusive Utah and Nevada real estate contracts. Feel free to review our active inventory below or reach out directly for full disclosures!"
            
        st.session_state.chatbot_messages.append({"role": "assistant", "content": bot_reply})
        st.rerun()

st.markdown("<hr style='margin: 30px 0; border: none; border-top: 1px solid #e5e7eb;'>", unsafe_allow_html=True)


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
        }
    ]
    return data
