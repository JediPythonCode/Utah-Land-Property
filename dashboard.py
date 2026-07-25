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
        <a href="#contracts-section" class="drawer-link">Our Contracts</a>
        <a href="#contracts-section" class="drawer-link">Assignments</a>
        <a href="#contracts-section" class="drawer-link">Sell to Us</a>
        <a href="#contracts-section" class="drawer-link">Portfolio</a>
        <a href="#contracts-section" class="drawer-link">Manage Assets</a>
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

# Property Database including all prior listings plus the updated Elko County parcels with values
@st.cache_data
def load_utah_property_database():
    data = [
        {
            "id": "UT-MIL-0101",
            "title": "Millcreek Residential Condo Parcel",
            "type": "Contract for Sale / Land",
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
            "id": "010-59G-008",
            "title": "Elko County Rural Land Parcel with Power",
            "type": "Rural Land / Raw Land",
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
            "id": "010-749-036",
            "title": "Sawgrass Court Residential Lot 036",
            "type": "Residential Lot",
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
            "id": "010-749-037",
            "title": "Sawgrass Court Residential Lot 037",
            "type": "Residential Lot",
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
            "id": "010-749-039",
            "title": "Sawgrass Court Residential Lot 039",
            "type": "Residential Lot",
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
            "id": "010-749-040",
            "title": "Sawgrass Court Residential Lot 040",
            "type": "Residential Lot",
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
            "id": "010-81H-032",
            "title": "Elko County North Rural Acreage",
            "type": "Rural Land",
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
            "id": "UT-MIL-0102",
            "title": "Millcreek Elmwood Contract Assignment",
            "type": "Contract for Sale / House",
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
            "id": "UT-DRP-0201",
            "title": "Draper Commercial Land Parcel",
            "type": "Commercial Land",
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
            "id": "UT-CLK-0301",
            "title": "Park Meadows Townhomes Investment",
            "type": "Townhome",
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


filtered_df = df.copy()

# --- DYNAMIC HEADER TITLE SECTION ---
if "show_faq" not in st.session_state:
    st.session_state.show_faq = False

col_title_1, col_title_2 = st.columns([3, 1])
with col_title_1:
    st.markdown(
        f"""
        <div style="margin: 24px 20px 16px 20px;">
            <h1 style="font-size: 1.7rem; font-weight: 800; color: #111827; margin-bottom: 4px;">Utah Land & Property Inc. Real Estate & Land For Sale</h1>
            <p style="font-size: 0.95rem; color: #6b7280; margin: 0;"><b>{len(filtered_df)}</b> active private contracts and land parcels available</p>
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

# --- RESPONSIVE 3-COLUMN CARD GRID ---
st.markdown("<div style='padding: 0 20px;'>", unsafe_allow_html=True)
if filtered_df.empty:
    st.info("No real estate contracts match your criteria.")
else:
    cols_per_row = 3
    rows = [
        filtered_df.iloc[i : i + cols_per_row]
        for i in range(0, len(filtered_df), cols_per_row)
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
                "#b91c1c" if row["status"] == "UNDER CONTRACT" else "rgba(0,0,0,0.7)"
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

                with st.expander(f"Review Terms / Submit Offer ({row['id']})"):
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
                    if st.button("Submit Official Offer", key=f"p_btn_{row['id']}"):
                        if user_email:
                            send_offer_dispatch(
                                row["id"], row["title"], user_email, offer_terms
                            )
                            st.success(
                                "Offer successfully dispatched to escrow!"
                            )
                        else:
                            st.error("Please enter a valid email address.")
st.markdown("</div>", unsafe_allow_html=True)
