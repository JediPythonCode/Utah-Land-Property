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
        <div class="hero-subtitle">Private Utah Real Estate Transactions.</div>
    </div>
    <div id="contracts-section"></div>
    """,
    unsafe_allow_html=True,
)

# Expanded Utah Property Database with Deal Structure (Contract Price, Purchase Price, ARV)
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
            "id": "UT-SLC-0103",
            "title": "Millbert Avenue Purchase Agreement",
            "type": "Contract for Sale / House",
            "city": "Salt Lake City, UT",
            "contract_price": 15000,
            "purchase_price": 440000,
            "arv": 650000,
            "beds": 5,
            "baths": 2,
            "sqft": 2852,
            "status": "UNDER CONTRACT",
            "address": "1010 E Millbert Ave S, Salt Lake City, UT 84106",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=800&q=80",
            "lat": 40.7045,
            "lon": -111.8590,
        },
        {
            "id": "UT-DRP-0204",
            "title": "Draper Commercial Buffer REPC Assignment",
            "type": "Contract for Sale / Commercial",
            "city": "Draper, UT",
            "contract_price": 8500,
            "purchase_price": 110000,
            "arv": 145000,
            "beds": 0,
            "baths": 0,
            "sqft": 4791,
            "status": "Direct Acquisition",
            "address": "12300 S Fort St, Draper, UT 84020",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 40.5243,
            "lon": -111.8631,
        },
        {
            "id": "UT-PRO-0301",
            "title": "Provo Riverfront Purchase Contract",
            "type": "Contract for Sale / Land",
            "city": "Provo, UT",
            "contract_price": 10000,
            "purchase_price": 310000,
            "arv": 410000,
            "beds": 0,
            "baths": 0,
            "sqft": 12500,
            "status": "New Listing",
            "address": "1850 N University Pkwy, Provo, UT 84604",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 40.2542,
            "lon": -111.6608,
        },
        {
            "id": "UT-OGD-0401",
            "title": "Ogden Historic Bench REPC",
            "type": "Contract for Sale / House",
            "city": "Ogden, UT",
            "contract_price": 11000,
            "purchase_price": 365000,
            "arv": 485000,
            "beds": 4,
            "baths": 3,
            "sqft": 3100,
            "status": "UNDER CONTRACT",
            "address": "1420 25th St, Ogden, UT 84401",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80",
            "lat": 41.2230,
            "lon": -111.9738,
        },
        {
            "id": "UT-PARK-0501",
            "title": "Park City Mountain View Townhome Contract",
            "type": "Contract for Sale / Townhouse",
            "city": "Park City, UT",
            "contract_price": 25000,
            "purchase_price": 950000,
            "arv": 1250000,
            "beds": 3,
            "baths": 4,
            "sqft": 2400,
            "status": "Exclusive",
            "address": "Park Meadows Townhomes, Park City, UT 84060",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=800&q=80",
            "lat": 40.6461,
            "lon": -111.4980,
        },
        {
            "id": "UT-STG-0601",
            "title": "St. George Red Rock Master REPC",
            "type": "Contract for Sale / Commercial",
            "city": "St. George, UT",
            "contract_price": 20000,
            "purchase_price": 680000,
            "arv": 890000,
            "beds": 0,
            "baths": 0,
            "sqft": 45000,
            "status": "Entitled Land",
            "address": "SunRiver Pkwy, St. George, UT 84790",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 37.0952,
            "lon": -113.5610,
        },
        {
            "id": "UT-LEH-0701",
            "title": "Lehi Silicon Slopes Purchase Agreement",
            "type": "Contract for Sale / Mixed-Use",
            "city": "Lehi, UT",
            "contract_price": 14000,
            "purchase_price": 570000,
            "arv": 750000,
            "beds": 4,
            "baths": 3,
            "sqft": 3400,
            "status": "Active",
            "address": "3300 N Ashton Blvd, Lehi, UT 84043",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=800&q=80",
            "lat": 40.4153,
            "lon": -111.8398,
        },
        {
            "id": "UT-SLC-0801",
            "title": "Sugar House Bungalow Assignment",
            "type": "Contract for Sale / House",
            "city": "Salt Lake City, UT",
            "contract_price": 12500,
            "purchase_price": 410000,
            "arv": 540000,
            "beds": 3,
            "baths": 2,
            "sqft": 1850,
            "status": "UNDER CONTRACT",
            "address": "2100 S Highland Dr, Salt Lake City, UT 84106",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80",
            "lat": 40.7215,
            "lon": -111.8565,
        },
        {
            "id": "UT-MUR-0901",
            "title": "Murray Metro Condominium REPC",
            "type": "Contract for Sale / Condo",
            "city": "Murray, UT",
            "contract_price": 6000,
            "purchase_price": 190000,
            "arv": 245000,
            "beds": 2,
            "baths": 1,
            "sqft": 950,
            "status": "Equitable Interest Available",
            "address": "4800 S State St, Murray, UT 84107",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=800&q=80",
            "lat": 40.6678,
            "lon": -111.8902,
        },
        {
            "id": "UT-WVC-1001",
            "title": "West Valley Family Estate Contract",
            "type": "Contract for Sale / House",
            "city": "West Valley City, UT",
            "contract_price": 9500,
            "purchase_price": 350000,
            "arv": 460000,
            "beds": 4,
            "baths": 2,
            "sqft": 2100,
            "status": "Active",
            "address": "3600 S Redwood Rd, West Valley City, UT 84119",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=800&q=80",
            "lat": 40.6970,
            "lon": -111.9380,
        },
        {
            "id": "UT-SAN-1101",
            "title": "Sandy Foothills Townhome REPC",
            "type": "Contract for Sale / Townhouse",
            "city": "Sandy, UT",
            "contract_price": 8000,
            "purchase_price": 305000,
            "arv": 395000,
            "beds": 3,
            "baths": 2,
            "sqft": 1650,
            "status": "Price Improvement",
            "address": "10000 S State St, Sandy, UT 84070",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=800&q=80",
            "lat": 40.5820,
            "lon": -111.8900,
        },
        {
            "id": "UT-MID-1201",
            "title": "Midvale Central Station Land Contract",
            "type": "Contract for Sale / Land",
            "city": "Midvale, UT",
            "contract_price": 7000,
            "purchase_price": 225000,
            "arv": 290000,
            "beds": 0,
            "baths": 0,
            "sqft": 6500,
            "status": "Direct Acquisition",
            "address": "7500 S State St, Midvale, UT 84047",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 40.6120,
            "lon": -111.8904,
        },
        {
            "id": "UT-BOV-1301",
            "title": "Bountiful Bench View REPC Assignment",
            "type": "Contract for Sale / House",
            "city": "Bountiful, UT",
            "contract_price": 13000,
            "purchase_price": 440000,
            "arv": 580000,
            "beds": 4,
            "baths": 3,
            "sqft": 2700,
            "status": "UNDER CONTRACT",
            "address": "500 S Main St, Bountiful, UT 84010",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80",
            "lat": 40.8870,
            "lon": -111.8800,
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
            <p style="font-size: 0.95rem; color: #6b7280; margin: 0;"><b>{len(filtered_df)}</b> active private contracts available for acquisition</p>
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

# --- EXPANDABLE FAQ & EXPLANATION SECTION ---
if st.session_state.show_faq:
    st.markdown(
        """
        <div style="background-color: #ffffff; border: 1px solid #e5e7eb; border-left: 4px solid #d92228; padding: 24px; border-radius: 8px; margin: 0 20px 30px 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.03);">
            <h3 style="margin-top: 0; color: #111827; font-size: 1.3rem;">Understanding Private Contract & REPC Assignments</h3>
            <p style="color: #4b5563; line-height: 1.6; font-size: 0.95rem;">
                A private contract assignment—frequently utilized in creative real estate transactions—involves transferring the equitable rights and interests held under a Real Estate Purchase Contract (REPC) or private agreement to a third party rather than executing a direct title sale of the physical property itself.
            </p>
            <h4 style="color: #111827; margin-bottom: 8px; font-size: 1.05rem;">Frequently Asked Questions</h4>
            <ul style="color: #4b5563; line-height: 1.6; font-size: 0.95rem; padding-left: 20px;">
                <li><b>What is being sold in an assignment?</b> The assignor transfers only their equitable interest and contractual rights to buy the property, allowing the assignee to step directly into the shoes of the original buyer.</li>
                <li><b>How does closing function?</b> The transaction typically involves an assignment fee paid to the original buyer, while the ultimate buyer fulfills the underlying obligations defined in the primary contract at closing.</li>
                <li><b>Why utilize this structure?</b> It provides a flexible mechanism for structuring real estate transactions, managing asset portfolios, and facilitating creative financing without immediate traditional title transfers.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

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

            # Dynamic badge coloring for UNDER CONTRACT vs others
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
