from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import re
import pandas as pd
import pydeck as pdk
import streamlit as st
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
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

# ---> UPDATED STICKY HEADER & ENHANCED STICKY FILTER BAR <---
st.markdown(
    """
    <style>
        /* Hide default Streamlit chrome */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        .stApp {
            background-color: #f4f5f7;
            color: #2c3e50;
            font-family: "Inter", -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* Fixed Sticky Header matching Zillow/Realtor */
        .industry-header {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            background-color: #ffffff;
            border-bottom: 1px solid #e0e0e0;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 40px;
            height: 70px;
            z-index: 999999;
            box-sizing: border-box;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        }
        
        .header-nav-left, .header-nav-right {
            display: flex;
            gap: 28px;
            align-items: center;
        }
        
        .header-nav-left a, .header-nav-right a {
            text-decoration: none;
            color: #333333;
            font-weight: 500;
            font-size: 14px;
        }
        
        .header-nav-left a:hover, .header-nav-right a:hover {
            color: #d92228;
        }
        
        /* Logo: Elegant Black with subtle red accent dot, bold, NOT underlined, NOT blue */
        .header-logo {
            font-size: 20px;
            font-weight: 700;
            color: #111111;
            letter-spacing: -0.5px;
            text-decoration: none !important;
            font-family: 'Playfair Display', Georgia, serif;
        }
        .header-logo span {
            color: #d92228;
        }
        .header-logo:hover {
            color: #111111;
            text-decoration: none !important;
        }
        
        .sign-in-btn {
            background-color: #006aff !important;
            color: white !important;
            padding: 8px 20px;
            border-radius: 6px;
            font-weight: 600 !important;
            text-decoration: none !important;
        }

        /* Push main content down below fixed header */
        .block-container {
            padding-top: 70px !important;
            padding-left: 0rem !important;
            padding-right: 0rem !important;
            max-width: 100% !important;
        }

        /* Immersive Friendly Residential Hero Banner */
        .hero-container {
            position: relative;
            background: linear-gradient(rgba(0, 0, 0, 0.35), rgba(0, 0, 0, 0.35)), 
                        url('https://images.unsplash.com/photo-1564013799919-ab600027ffc6?auto=format&fit=crop&w=2000&q=80');
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
            padding: 20px 40px;
            border-bottom: 2px solid #e5e7eb;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
            position: sticky;
            top: 70px;
            z-index: 99998;
        }

        /* Custom styling wrapper for select boxes inside the filter bar */
        div[data-baseweb="select"] > div {
            border-radius: 8px !important;
            border-color: #d1d5db !important;
            background-color: #ffffff !important;
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
            <a href="#" class="header-logo">UTAH LAND & PROPERTY<span>.</span></a>
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

# Friendly Residential Hero Section
st.markdown(
    """
    <div class="hero-container">
        <div class="hero-title">Find your next Utah property & contract.</div>
        <div class="hero-subtitle">Explore verified REPC assignments, direct acquisitions, and wholesale equity.</div>
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
    
    # Update the first listing to use the first image property pattern if needed, 
    # ensuring all records use valid Unsplash listing images properly mapped.
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
    st.markdown("<p style='font-size: 11px; font-weight: 700; color: #d92228; text-transform: uppercase; margin-bottom: 2px;'>📍 All Utah Cities</p>", unsafe_allow_html=True)
    selected_location = st.selectbox(
        "Utah City Search", all_locations, label_visibility="collapsed"
    )
with f_col2:
    st.markdown("<p style='font-size: 11px; font-weight: 700; color: #d92228; text-transform: uppercase; margin-bottom: 2px;'>🏷️ Contracts for Sale</p>", unsafe_allow_html=True)
    status_filter = st.selectbox(
        "Status", ["Contracts for Sale", "All Statuses"], label_visibility="collapsed"
    )
with f_col3:
    st.markdown("<p style='font-size: 11px; font-weight: 700; color: #d92228; text-transform: uppercase; margin-bottom: 2px;'>💲 Any Price</p>", unsafe_allow_html=True)
    price_filter = st.selectbox(
        "Contract Price",
        ["Any Price", "Under $30k", "$30k - $60k", "Over $60k"],
        label_visibility="collapsed",
    )
with f_col4:
    st.markdown("<p style='font-size: 11px; font-weight: 700; color: #d92228; text-transform: uppercase; margin-bottom: 2px;'>🛏️ Beds & Bath</p>", unsafe_allow_html=True)
    beds_filter = st.selectbox(
        "Beds",
        ["Beds & baths", "2+ Beds", "3+ Beds", "4+ Beds"],
        label_visibility="collapsed",
    )
with f_col5:
    st.markdown("<p style='font-size: 11px; font-weight: 700; color: #d92228; text-transform: uppercase; margin-bottom: 2px;'>🏠 Property Type</p>", unsafe_allow_html=True)
    type_filter = st.selectbox(
        "Contract Type",
        ["Property type", "House", "Land", "Townhouse", "Condo"],
        label_visibility="collapsed",
    )
with f_col6:
    st.markdown("<p style='font-size: 11px; font-weight: 700; color: transparent; text-transform: uppercase; margin-bottom: 2px;'>Action</p>", unsafe_allow_html=True)
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
    selected_location if selected_location != "All Utah Cities" else "Utah Land & Property Inc."
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
    st.markdown("<div style='margin: 36px 40px 0 0; text-align: right;'>", unsafe_allow_html=True)
    if st.button("🛈 How private contract assignment works & FAQ", type="tertiary"):
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
            # Use the first image from each listing row explicitly
            listing_images = row['image'].split(',') if isinstance(row['image'], str) else [row['image']]
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
                            send_offer_dispatch(row["id"], row["title"], user_email, offer_terms)
                            st.success("Offer successfully dispatched to escrow!")
                        else:
                            st.error("Please enter a valid email address.")
st.markdown("</div>", unsafe_allow_html=True)

# --- MAP SECTION ---
st.markdown(
    """
    <div style="margin: 40px 40px 16px 40px; border-top: 1px solid #e5e7eb; padding-top: 24px;">
        <h2 style="font-size: 1.4rem; font-weight: 800; color: #111827; margin-bottom: 4px;">Interactive Regional Contract Map</h2>
        <p style="font-size: 0.9rem; color: #6b7280;">Geographic distribution of active equitable interest assignments across Utah.</p>
    </div>
""",
    unsafe_allow_html=True,
)

map_data = filtered_df[["lat", "lon"]].rename(
    columns={"lat": "latitude", "lon": "longitude"}
)

layer = pdk.Layer(
    "ScatterplotLayer",
    data=map_data,
    get_position=["longitude", "latitude"],
    get_color=[217, 34, 40, 160],
    get_radius=3000,
    pickable=True,
)

view_state = pdk.ViewState(
    latitude=filtered_df["lat"].mean() if not filtered_df.empty else 40.7608,
    longitude=filtered_df["lon"].mean() if not filtered_df.empty else -111.8910,
    zoom=8,
    pitch=0,
)

r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": "Active Utah Contract Location"}
)

st.pydeck_chart(r)
# ---------------------------------------------------------------------------
# Phone validation helpers
# ---------------------------------------------------------------------------
def is_valid_us_phone(phone: str) -> bool:
    """Basic but robust US phone validation."""
    if not phone:
        return False
    digits = re.sub(r"\D", "", phone)
    if len(digits) == 10:
        return True
    if len(digits) == 11 and digits.startswith("1"):
        return True
    return False


def format_phone(phone: str) -> str:
    digits = re.sub(r"\D", "", phone)
    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    return phone


# ---------------------------------------------------------------------------
# Email helper – routes to douglas@utahlandproperty.com + attaches POF
# ---------------------------------------------------------------------------
def send_offer_dispatch(
    property_id: str,
    property_title: str,
    user_name: str,
    user_email: str,
    user_phone: str,
    investor_type: str,
    proposed_fee: str,
    contingencies: str,
    closing_timeline: str,
    additional_notes: str,
    pof_file,
):
    smtp_server = "smtp.gmail.com"
    port = 587
    sender_email = st.secrets.get("EMAIL_USER")
    sender_password = st.secrets.get("EMAIL_PASS")
    recipient = "douglas@utahlandproperty.com"

    if not sender_email or not sender_password:
        return False, "Email credentials not configured in secrets."

    subject = f"New Assignment Interest / Offer – {property_id}"
    body = f"""
NEW ASSIGNMENT DEAL INTEREST (Verified User)
============================================
Property ID     : {property_id}
Asset Title     : {property_title}

SUBMITTER DETAILS
-----------------
Name            : {user_name}
Email           : {user_email}
Phone           : {user_phone}
Investor Type   : {investor_type or "Not specified"}

DEAL STRUCTURE OFFERED
----------------------
Proposed Assignment Fee / Offer : {proposed_fee}
Contingencies / Conditions      : {contingencies or "None stated"}
Preferred Closing Timeline      : {closing_timeline or "Flexible"}
Additional Notes                : {additional_notes or "None"}

Proof of Funds  : {"Attached" if pof_file else "Not provided"}

----------------------------
Utah Land & Property Inc.
Active Assignment Marketplace
"""

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient
    msg["Cc"] = user_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Attach Proof of Funds if provided
    if pof_file is not None:
        try:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(pof_file.getvalue())
            encoders.encode_base64(part)
            filename = pof_file.name or "proof_of_funds.pdf"
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={filename}",
            )
            msg.attach(part)
        except Exception as e:
            return False, f"Could not attach Proof of Funds: {e}"

    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, [recipient, user_email], msg.as_string())
        return True, "Your verified offer / interest has been sent to Douglas at Utah Land & Property."
    except Exception as e:
        return False, f"Failed to send: {str(e)}"


# ---------------------------------------------------------------------------
# Stronger Sign-up / Authentication Gate
# ---------------------------------------------------------------------------
if "user_signed_up" not in st.session_state:
    st.session_state.user_signed_up = False
    st.session_state.user_name = ""
    st.session_state.user_email = ""
    st.session_state.user_phone = ""
    st.session_state.investor_type = ""

st.markdown("<div class='responsive-content-pad'>", unsafe_allow_html=True)

if not st.session_state.user_signed_up:
    st.markdown(
        """
        <div style="background:#fff; border:1px solid #e5e7eb; border-left:4px solid #d92228;
                    padding:20px; border-radius:8px; margin:20px 0; box-shadow:0 4px 12px rgba(0,0,0,0.04);">
            <h3 style="margin-top:0; color:#111827;">Investor Verification Required</h3>
            <p style="color:#4b5563; font-size:0.9rem; margin-bottom:12px;">
                This is a private active-assignment marketplace. Complete the short verification below
                to unlock live deals and submit offers directly to Douglas.
            </p>
            <ul style="color: #4b5563; font-size: 0.85rem; padding-left: 18px; margin-bottom: 0;">
                <li>Valid name, email & US phone required</li>
                <li>Proof of Funds will be required on every offer</li>
                <li>All submissions go to douglas@utahlandproperty.com</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("signup_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            name_in = st.text_input("Full Name *", placeholder="Jane Investor")
            email_in = st.text_input("Email *", placeholder="you@domain.com")
        with col2:
            phone_in = st.text_input("Mobile Phone *", placeholder="(801) 555-1234")
            investor_type = st.selectbox(
                "Investor Type",
                [
                    "Select…",
                    "Individual Investor",
                    "Fix & Flip",
                    "Buy & Hold",
                    "Wholesaler",
                    "Fund / Syndicate",
                    "Other",
                ],
            )

        st.caption("Phone must be a valid US number. Used strictly for deal follow-up.")

        submitted = st.form_submit_button(
            "Verify & Unlock Deals",
            type="primary",
            use_container_width=True,
        )

        if submitted:
            errors = []
            if not name_in.strip() or len(name_in.strip()) < 3:
                errors.append("Please enter your full name.")
            if not email_in.strip() or "@" not in email_in or "." not in email_in.split("@")[-1]:
                errors.append("Please enter a valid email address.")
            if not is_valid_us_phone(phone_in):
                errors.append("Please enter a valid US phone number (10 digits).")

            if errors:
                for e in errors:
                    st.error(e)
            else:
                st.session_state.user_signed_up = True
                st.session_state.user_name = name_in.strip()
                st.session_state.user_email = email_in.strip().lower()
                st.session_state.user_phone = format_phone(phone_in)
                st.session_state.investor_type = (
                    investor_type if investor_type != "Select…" else ""
                )
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ---- User is verified – status bar ----
st.markdown(
    f"""
    <div style="background:#f0fdf4; border:1px solid #bbf7d0; color:#166534;
                padding:10px 16px; border-radius:6px; margin-bottom:16px; font-size:0.9rem;">
        Verified as <b>{st.session_state.user_name}</b> 
        &nbsp;·&nbsp; {st.session_state.user_email} 
        &nbsp;·&nbsp; {st.session_state.user_phone}
        &nbsp;|&nbsp; Offers → douglas@utahlandproperty.com
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Title + FAQ toggle section
# ---------------------------------------------------------------------------
location_title = (
    selected_location if selected_location != "All Utah Cities" else "Utah Land & Property Inc."
)

if "show_faq" not in st.session_state:
    st.session_state.show_faq = False

st.markdown("<div class='responsive-content-pad'>", unsafe_allow_html=True)
col_title_1, col_title_2 = st.columns([3, 1])
with col_title_1:
    st.markdown(
        f"""
        <div style="margin: 12px 0 16px 0;">
            <h1 style="font-size: 1.5rem; font-weight: 800; color: #111827; margin-bottom: 4px;">
                {location_title} – Active Assignment Deals
            </h1>
            <p style="font-size: 0.9rem; color: #6b7280; margin: 0;">
                <b>{len(filtered_df)}</b> private contracts available for assignment
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col_title_2:
    st.markdown("<div style='margin: 18px 0 0 0; text-align: right;'>", unsafe_allow_html=True)
    if st.button("🛈 FAQ", type="tertiary"):
        st.session_state.show_faq = not st.session_state.show_faq
    st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

if st.session_state.show_faq:
    st.markdown("<div class='responsive-content-pad'>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="background-color: #ffffff; border: 1px solid #e5e7eb; border-left: 4px solid #d92228;
                    padding: 20px; border-radius: 8px; margin-bottom: 24px; box-shadow: 0 4px 12px rgba(0,0,0,0.03);">
            <h3 style="margin-top: 0; color: #111827; font-size: 1.2rem;">
                How Assignment Deals Work
            </h3>
            <p style="color: #4b5563; line-height: 1.6; font-size: 0.9rem;">
                You are purchasing the <b>equitable interest</b> (the right to buy) under an existing REPC,
                not the property title itself. At closing you step into the original buyer’s shoes and
                pay an assignment fee to the current contract holder.
            </p>
            <ul style="color: #4b5563; line-height: 1.5; font-size: 0.9rem; padding-left: 18px; margin-bottom: 0;">
                <li><b>Contract Price</b> = the assignment fee you negotiate / pay to take over the deal.</li>
                <li><b>Underlying Price</b> = the price the end seller will receive at closing.</li>
                <li>All offers are routed directly to Douglas at Utah Land & Property.</li>
                <li><b>Proof of Funds</b> is required with every offer submission.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Interactive listing cards + verified offer form (with POF)
# ---------------------------------------------------------------------------
st.markdown("<div class='responsive-content-pad'>", unsafe_allow_html=True)

if filtered_df.empty:
    st.info("No active assignment contracts match your current filters.")
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
                row["image"].split(",") if isinstance(row["image"], str) else [row["image"]]
            )
            first_image = listing_images[0].strip()

            spread = row["underlying_price"] - row["contract_price"]
            spread_pct = (spread / row["underlying_price"] * 100) if row["underlying_price"] else 0

            with cols[idx]:
                st.markdown(
                    f"""
                    <div style="background: white; border-radius: 8px; overflow: hidden;
                                border: 1px solid #e5e7eb; margin-bottom: 12px;
                                box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                        <div style="position: relative;">
                            <img src="{first_image}"
                                 style="width: 100%; height: 180px; object-fit: cover;"
                                 alt="{row['title']}">
                            <div style="position: absolute; top: 10px; left: 10px;
                                        background: rgba(0,0,0,0.75); color: white;
                                        padding: 3px 8px; border-radius: 4px;
                                        font-size: 11px; font-weight: 600;">
                                {row['status']}
                            </div>
                        </div>
                        <div style="padding: 14px;">
                            <div style="font-size: 11px; text-transform: uppercase; color: #6b7280;
                                        font-weight: 700; margin-bottom: 4px;">
                                {row['broker']} · {row['type']}
                            </div>
                            <div style="font-size: 15px; font-weight: 700; color: #111827; margin-bottom: 8px;">
                                {row['title']}
                            </div>

                            <!-- Deal Structure Block -->
                            <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:6px;
                                        padding:10px; margin-bottom:10px; font-size:12px;">
                                <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                                    <span style="color:#64748b;">Assignment Fee (asking)</span>
                                    <span style="font-weight:700; color:#d92228;">${row['contract_price']:,}</span>
                                </div>
                                <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                                    <span style="color:#64748b;">Underlying Purchase Price</span>
                                    <span style="font-weight:600;">${row['underlying_price']:,}</span>
                                </div>
                                <div style="display:flex; justify-content:space-between; border-top:1px dashed #cbd5e1; padding-top:4px;">
                                    <span style="color:#64748b;">Equity / Spread</span>
                                    <span style="font-weight:600; color:#166534;">
                                        ${spread:,.0f} ({spread_pct:.0f}%)
                                    </span>
                                </div>
                            </div>

                            <div style="font-size: 12px; color: #374151; margin-bottom: 4px;">
                                <b>{row['beds']}</b> bds · <b>{row['baths']}</b> ba · <b>{row['sqft']:,}</b> sqft
                            </div>
                            <div style="font-size: 12px; color: #6b7280;">{row['address']}</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                with st.expander(f"Submit Verified Offer – {row['id']}", expanded=False):
                    st.caption("All offers + Proof of Funds are sent to douglas@utahlandproperty.com")

                    with st.form(key=f"offer_form_{row['id']}"):
                        st.write(f"**Deal:** {row['title']}")
                        st.write(f"Asking Assignment Fee: **${row['contract_price']:,}**")

                        proposed_fee = st.text_input(
                            "Your Proposed Assignment Fee / Offer *",
                            placeholder=f"e.g. {max(0, row['contract_price'] - 2000)} or 'asking'",
                            key=f"fee_{row['id']}",
                        )
                        contingencies = st.text_area(
                            "Contingencies / Conditions",
                            placeholder="Inspection, financing, title review, etc.",
                            key=f"cont_{row['id']}",
                            height=70,
                        )
                        closing_timeline = st.selectbox(
                            "Preferred Closing Timeline",
                            [
                                "ASAP / within 7 days",
                                "7–14 days",
                                "15–30 days",
                                "Flexible / seller’s timeline",
                                "Other (note below)",
                            ],
                            key=f"close_{row['id']}",
                        )
                        additional_notes = st.text_area(
                            "Additional Notes",
                            placeholder="Anything else Douglas should know…",
                            key=f"notes_{row['id']}",
                            height=60,
                        )

                        st.markdown("**Proof of Funds ***")
                        pof_file = st.file_uploader(
                            "Upload bank statement, LOI, or POF letter (PDF, PNG, JPG)",
                            type=["pdf", "png", "jpg", "jpeg"],
                            key=f"pof_{row['id']}",
                            label_visibility="collapsed",
                        )
                        st.caption("Required. Max recommended size ~10 MB.")

                        submitted = st.form_submit_button(
                            "Send Verified Offer to Douglas",
                            type="primary",
                            use_container_width=True,
                        )

                        if submitted:
                            errors = []
                            if not proposed_fee.strip():
                                errors.append("Please enter a proposed assignment fee or offer amount.")
                            if pof_file is None:
                                errors.append("Proof of Funds upload is required.")

                            if errors:
                                for e in errors:
                                    st.error(e)
                            else:
                                success, message = send_offer_dispatch(
                                    property_id=row["id"],
                                    property_title=row["title"],
                                    user_name=st.session_state.user_name,
                                    user_email=st.session_state.user_email,
                                    user_phone=st.session_state.user_phone,
                                    investor_type=st.session_state.investor_type,
                                    proposed_fee=proposed_fee,
                                    contingencies=contingencies,
                                    closing_timeline=closing_timeline,
                                    additional_notes=additional_notes,
                                    pof_file=pof_file,
                                )
                                if success:
                                    st.success(message)
                                    st.balloons()
                                else:
                                    st.error(message)

st.markdown("</div>", unsafe_allow_html=True)
