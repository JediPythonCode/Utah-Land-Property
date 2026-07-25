from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re
import smtplib
import pandas as pd
import pydeck as pdk
import streamlit as st

# Page Configuration - Enterprise Real Estate Portal Layout
st.set_page_config(
    page_title="Utah Land & Property Inc. | Private Portfolio",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---> UPDATED STICKY HEADER & HERO WITH RENTLER-STYLE RED BACKGROUND <---
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Inter:wght@400;500;600;700;900&display=swap');

        /* Hide default Streamlit chrome */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        .stApp {
            background-color: #f4f5f7;
            color: #2c3e50;
            font-family: "Inter", -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* Fixed Sticky Header matching Rentler style (Red Background, White Bold Font) */
        .industry-header {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            background-color: #d92228;
            border-bottom: 1px solid #b51c22;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 40px;
            height: 70px;
            z-index: 999999;
            box-sizing: border-box;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        }
        
        .header-nav-left, .header-nav-right {
            display: flex;
            gap: 28px;
            align-items: center;
        }
        
        .header-nav-left a, .header-nav-right a {
            text-decoration: none;
            color: #ffffff !important;
            font-weight: 700 !important;
            font-size: 14px;
        }
        
        .header-nav-left a:hover, .header-nav-right a:hover {
            color: #f3f4f6 !important;
            text-decoration: underline;
        }
        
        /* Logo: White, bold, and clean */
        .header-logo {
            font-size: 21px;
            font-weight: 900 !important;
            color: #ffffff !important;
            letter-spacing: 0.5px;
            text-decoration: none !important;
            font-family: 'Playfair Display', Georgia, serif;
        }
        .header-logo span {
            color: #ffffff !important;
            font-weight: 900 !important;
        }
        .header-logo:hover {
            color: #ffffff !important;
            text-decoration: none !important;
        }
        
        .sign-in-btn {
            background-color: #ffffff !important;
            color: #d92228 !important;
            padding: 8px 20px;
            border-radius: 6px;
            font-weight: 700 !important;
            text-decoration: none !important;
        }
        .sign-in-btn:hover {
            background-color: #f9fafb !important;
        }

        /* Push main content down below fixed header */
        .block-container {
            padding-top: 70px !important;
            padding-left: 0rem !important;
            padding-right: 0rem !important;
            max-width: 100% !important;
        }

        /* Immersive Hero Banner with Xeriscaped Sustainable Landscape */
        .hero-container {
            position: relative;
            background: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)), 
                        url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=2000&q=80');
            background-size: cover;
            background-position: center;
            height: 400px;
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
            font-size: 38px;
            font-weight: 800;
            margin-bottom: 8px;
            letter-spacing: -0.5px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
            font-family: 'Inter', sans-serif;
        }

        .hero-subtitle {
            font-size: 16px;
            font-weight: 400;
            margin-bottom: 24px;
            text-shadow: 0 1px 3px rgba(0,0,0,0.3);
        }

        /* Standout Sticky Filter Bar Styling */
        .filter-container {
            background: linear-gradient(135deg, #ffffff 0%, #f9fafb 100%);
            padding: 16px 40px;
            border-bottom: 2px solid #e5e7eb;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
            position: sticky;
            top: 70px;
            z-index: 99998;
        }

        /* Professional styling wrapper for select boxes inside the filter bar */
        div[data-baseweb="select"] > div {
            border-radius: 6px !important;
            border-color: #d1d5db !important;
            background-color: #ffffff !important;
            min-height: 38px !important;
            box-shadow: 0 1px 2px rgba(0,0,0,0.02);
            transition: all 0.2s ease;
        }
        div[data-baseweb="select"] > div:hover {
            border-color: #d92228 !important;
            box-shadow: 0 0 0 3px rgba(217, 34, 40, 0.1) !important;
        }
    </style>

    <!-- Industry Sticky Header -->
    <div class="industry-header">
        <div class="header-nav-left">
            <a href="#">Buy Contracts</a>
            <a href="#">Assign</a>
            <a href="#">Sell</a>
            <a href="#">Portfolio</a>
        </div>
        <div>
            <a href="#" class="header-logo">UTAH LAND & PROPERTY</a>
        </div>
        <div class="header-nav-right">
            <a href="#">Manage Assets</a>
            <a href="#">Resources</a>
            <a href="#" class="sign-in-btn">Sign In</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Friendly Residential Hero Section with Xeriscaped Home
st.markdown(
    """
    <div class="hero-container">
        <div class="hero-title">Find your next Utah property & contract.</div>
        <div class="hero-subtitle">Explore verified REPC assignments, direct acquisitions, and water-efficient xeriscaped properties.</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# Expanded Utah Property Database with 15 Contracts for Sale (Private Market Only)
@st.cache_data
def load_utah_property_database():
    data = [
        {
            "id": "UT-MIL-0101",
            "title": "Millcreek Residential Condo Parcel",
            "type": "Contract for Sale / Land",
            "city": "Millcreek, UT",
            "contract_price": 28500,
            "underlying_price": 285000,
            "beds": 1,
            "baths": 1,
            "sqft": 750,
            "status": "Equitable Interest Assignable",
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
            "contract_price": 45000,
            "underlying_price": 625000,
            "beds": 5,
            "baths": 2,
            "sqft": 2446,
            "status": "Showcase",
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
            "contract_price": 52000,
            "underlying_price": 650000,
            "beds": 5,
            "baths": 2,
            "sqft": 2852,
            "status": "2 days on market",
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
            "contract_price": 15000,
            "underlying_price": 145000,
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
            "contract_price": 35000,
            "underlying_price": 410000,
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
            "contract_price": 38000,
            "underlying_price": 485000,
            "beds": 4,
            "baths": 3,
            "sqft": 3100,
            "status": "Price Improvement",
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
            "contract_price": 95000,
            "underlying_price": 1250000,
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
            "contract_price": 75000,
            "underlying_price": 890000,
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
            "contract_price": 60000,
            "underlying_price": 750000,
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
            "contract_price": 42000,
            "underlying_price": 540000,
            "beds": 3,
            "baths": 2,
            "sqft": 1850,
            "status": "New Listing",
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
            "contract_price": 12000,
            "underlying_price": 245000,
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
            "contract_price": 34000,
            "underlying_price": 460000,
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
            "contract_price": 28000,
            "underlying_price": 395000,
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
            "contract_price": 22000,
            "underlying_price": 290000,
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
            "contract_price": 49000,
            "underlying_price": 580000,
            "beds": 4,
            "baths": 3,
            "sqft": 2700,
            "status": "Exclusive",
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


# Standout Sticky Filter & Search Bar Container
st.markdown("<div class='filter-container'>", unsafe_allow_html=True)
f_col1, f_col2, f_col3, f_col4, f_col5, f_col6 = st.columns(
    [2.4, 1.1, 1.1, 1.1, 1.2, 1]
)

all_locations = [
    "All Utah Cities",
    "Salt Lake City, UT",
    "Provo, UT",
    "Ogden, UT",
    "St. George, UT",
    "Logan, UT",
    "Layton, UT",
    "Orem, UT",
    "Sandy, UT",
    "West Valley City, UT",
    "West Jordan, UT",
    "Millcreek, UT",
    "Draper, UT",
    "Park City, UT",
    "Lehi, UT",
    "Murray, UT",
    "Midvale, UT",
    "Bountiful, UT",
    "Cottonwood Heights, UT",
    "Holladay, UT",
    "Herriman, UT",
    "Riverton, UT",
    "South Jordan, UT",
    "South Salt Lake, UT",
    "Taylorsville, UT",
    "Bluffdale, UT",
    "Tooele, UT",
    "Eagle Mountain, UT",
    "Saratoga Springs, UT",
    "Kearns, UT",
    "Magna, UT",
    "White City, UT",
    "Emigration Canyon, UT",
    "Copperton, UT",
    "Cache, UT",
    "Brigham City, UT",
    "Cache Ward, UT",
    "Smithfield, UT",
    "Hyrum, UT",
    "Eden, UT",
    "Liberty, UT",
    "Huntsville, UT",
    "Alpine, UT",
    "American Fork, UT",
    "Cedar Hills, UT",
    "Highland, UT",
    "Lindon, UT",
    "Payson, UT",
    "Pleasant Grove, UT",
    "Salem, UT",
    "Sundance, UT",
    "Hobble Creek, UT",
    "East Basin, UT",
    "Hoytsville, UT",
    "Marion, UT",
    "Coalville, UT",
    "Heber City, UT",
    "Kamas, UT",
    "Kanab, UT",
    "Moab, UT",
    "Cedar City, UT",
    "Richfield, UT",
    "Vernal, UT",
    "Roosevelt, UT",
    "Bluff, UT",
    "Mexican Hat, UT",
    "Montezuma Creek, UT",
    "Dammeron Valley, UT",
    "Enterprise, UT",
    "Modena, UT",
    "Beryl Junction, UT",
    "Central, UT",
    "Ticaboo, UT",
]

with f_col1:
    st.markdown(
        "<p style='font-size: 11px; font-weight: 700; color: #4b5563; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;'>Location</p>",
        unsafe_allow_html=True,
    )
    selected_location = st.selectbox(
        "Utah City Search", all_locations, label_visibility="collapsed"
    )
with f_col2:
    st.markdown(
        "<p style='font-size: 11px; font-weight: 700; color: #4b5563; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;'>Status</p>",
        unsafe_allow_html=True,
    )
    status_filter = st.selectbox(
        "Status", ["Contracts for Sale", "All Statuses"], label_visibility="collapsed"
    )
with f_col3:
    st.markdown(
        "<p style='font-size: 11px; font-weight: 700; color: #4b5563; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;'>Price Range</p>",
        unsafe_allow_html=True,
    )
    price_filter = st.selectbox(
        "Contract Price",
        ["Any Price", "Under $30k", "$30k - $60k", "Over $60k"],
        label_visibility="collapsed",
    )
with f_col4:
    st.markdown(
        "<p style='font-size: 11px; font-weight: 700; color: #4b5563; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;'>Beds & Baths</p>",
        unsafe_allow_html=True,
    )
    beds_filter = st.selectbox(
        "Beds",
        ["Beds & baths", "2+ Beds", "3+ Beds", "4+ Beds"],
        label_visibility="collapsed",
    )
with f_col5:
    st.markdown(
        "<p style='font-size: 11px; font-weight: 700; color: #4b5563; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;'>Property Type</p>",
        unsafe_allow_html=True,
    )
    type_filter = st.selectbox(
        "Contract Type",
        ["Property type", "House", "Land", "Townhouse", "Condo"],
        label_visibility="collapsed",
    )
with f_col6:
    st.markdown(
        "<p style='font-size: 11px; font-weight: 700; color: transparent; text-transform: uppercase; margin-bottom: 4px;'>Action</p>",
        unsafe_allow_html=True,
    )
    save_search_btn = st.button("Save Search", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# --- FILTER EXECUTION ---
filtered_df = df.copy()
if selected_location != "All Utah Cities":
    filtered_df = filtered_df[
        filtered_df["city"].str.lower() == selected_location.lower()
    ]

if price_filter == "Under $30k":
    filtered_df = filtered_df[filtered_df["contract_price"] <= 30000]
elif price_filter == "$30k - $60k":
    filtered_df = filtered_df[
        (filtered_df["contract_price"] > 30000)
        & (filtered_df["contract_price"] <= 60000)
    ]
elif price_filter == "Over $60k":
    filtered_df = filtered_df[filtered_df["contract_price"] > 60000]

if beds_filter == "2+ Beds":
    filtered_df = filtered_df[filtered_df["beds"] >= 2]
elif beds_filter == "3+ Beds":
    filtered_df = filtered_df[filtered_df["beds"] >= 3]
elif beds_filter == "4+ Beds":
    filtered_df = filtered_df[filtered_df["beds"] >= 4]

if type_filter != "Property type":
    filtered_df = filtered_df[
        filtered_df["type"].str.contains(type_filter, case=False, na=False)
    ]

# --- DYNAMIC HEADER TITLE SECTION ---
location_title = (
    selected_location
    if selected_location != "All Utah Cities"
    else "Utah Land & Property Inc."
)

if "show_faq" not in st.session_state:
    st.session_state.show_faq = False

col_title_1, col_title_2 = st.columns([3, 1])
with col_title_1:
    st.markdown(
        f"""
        <div style="margin: 24px 40px 16px 40px;">
            <h1 style="font-size: 1.7rem; font-weight: 800; color: #111827; margin-bottom: 4px;">{location_title} Real Estate & Land For Sale</h1>
            <p style="font-size: 0.95rem; color: #6b7280; margin: 0;"><b>{len(filtered_df)}</b> active private contracts available for acquisition</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

with col_title_2:
    st.markdown(
        "<div style='margin: 36px 40px 0 0; text-align: right;'>",
        unsafe_allow_html=True,
    )
    if st.button("How private contract assignment works & FAQ", type="tertiary"):
        st.session_state.show_faq = not st.session_state.show_faq
    st.markdown("</div>", unsafe_allow_html=True)

# --- EXPANDABLE FAQ & EXPLANATION SECTION ---
if st.session_state.show_faq:
    st.markdown(
        """
        <div style="background-color: #ffffff; border: 1px solid #e5e7eb; border-left: 4px solid #d92228; padding: 24px; border-radius: 8px; margin: 0 40px 30px 40px; box-shadow: 0 4px 12px rgba(0,0,0,0.03);">
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
st.markdown("<div style='padding: 0 40px;'>", unsafe_allow_html=True)
if filtered_df.empty:
    st.info("No real estate contracts match your filter criteria in this region.")
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

            with cols[idx]:
                st.markdown(
                    f"""
                        <div style="background: white; border-radius: 8px; overflow: hidden; border: 1px solid #e5e7eb; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                            <div style="position: relative;">
                                <img src="{first_image}" style="width: 100%; height: 200px; object-fit: cover;">
                                <div style="position: absolute; top: 12px; left: 12px; background: rgba(0,0,0,0.7); color: white; padding: 4px 10px; border-radius: 4px; font-size: 12px; font-weight: 600;">{row['status']}</div>
                            </div>
                            <div style="padding: 16px;">
                                <div style="font-size: 11px; text-transform: uppercase; color: #6b7280; font-weight: 700; margin-bottom: 4px;">{row['broker']}</div>
                                <div style="font-size: 18px; font-weight: 800; color: #111827; margin-bottom: 4px;">Contract: ${row['contract_price']:,}</div>
                                <div style="font-size: 13px; color: #4b5563; margin-bottom: 8px;">Property Value: ${row['underlying_price']:,}</div>
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
                            st.success("Offer successfully dispatched to escrow!")
                        else:
                            st.error("Please enter a valid email address.")
st.markdown("</div>", unsafe_allow_html=True)
