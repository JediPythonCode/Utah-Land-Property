from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import pandas as pd
import pydeck as pdk
import streamlit as st

# Page Configuration - Enterprise Real Estate Portal Layout
st.set_page_config(
    page_title="Utah Real Estate & Land for Sale | Utah Land & Property",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 1. Page Configuration (Must always be first)
st.set_page_config(
    page_title="Utah Land & Property Inc. | Private Portfolio",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 2. ---> UPDATED INDUSTRY-GRADE STICKY HEADER & FRIENDLY RESIDENTIAL HERO <---
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
        
        .header-logo {
            font-size: 20px;
            font-weight: 700;
            color: #1a1a1a;
            letter-spacing: -0.5px;
            text-decoration: none;
            font-family: 'Playfair Display', Georgia, serif;
        }
        
        .sign-in-btn {
            background-color: #006aff !important;
            color: white !important;
            padding: 8px 20px;
            border-radius: 6px;
            font-weight: 600 !important;
        }

        /* Push main content down below fixed header */
        .block-container {
            padding-top: 70px !important;
            padding-left: 0rem !important;
            padding-right: 0rem !important;
            max-width: 100% !important;
        }

        /* Immersive Friendly Residential Hero Banner (Zillow-style, not a huge commercial mega-home) */
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

# 3. Friendly Residential Hero Section
st.markdown(
    
    <div class="hero-container">
    <h1 class="hero-title">Utah Investment Properties & Real Estate Contracts For Sale</h1>
    <p class="hero-subtitle">Access verified REPC assignments, wholesale equity, off-market real estate, and commercial land packages across Salt Lake City, Draper, Millcreek, and Utah.</p>
</div>
    ,
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


# --- STICKY HEADER WRAPPER (Locks to Top on Scroll) ---
st.markdown("<div class='sticky-header-wrapper'>", unsafe_allow_html=True)

# Top Navigation Bar
st.markdown(
    """
    <div class="portal-navbar">
        <div class="portal-nav-left">
            <span>Buy Contracts</span>
            <span>Assign</span>
            <span>Sell</span>
            <span>Portfolio</span>
            <span style="color: #d92228; font-weight: 700;">Submit an Offer</span>
        </div>
        <div class="portal-logo">
            UTAH LAND & PROPERTY INC.
        </div>
        <div class="portal-nav-right">
            <span>Private Assets</span>
            <span>Help</span>
            <span style="background-color: #d92228; color: white; padding: 8px 18px; border-radius: 6px; font-weight: 600;">Sign In</span>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

# Sticky Filter & Search Bar
st.markdown("<div class='filter-bar-container'>", unsafe_allow_html=True)
f_col1, f_col2, f_col3, f_col4, f_col5, f_col6 = st.columns(
    [2.4, 1.1, 1.1, 1.1, 1.2, 1]
)

all_locations = [
    "All Utah Cities",
    # Major Urban & Regional Centers
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
    
    # Wasatch Front & Salt Lake County Suburbs / Municipalities
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
    
    # Recently Incorporated & Transitioned Communities (e.g., former Metro Townships)
    "Kearns, UT",
    "Magna, UT",
    "White City, UT",
    "Emigration Canyon, UT",
    "Copperton, UT",
    
    # Northern Utah & Cache Valley
    "Cache, UT",
    "Brigham City, UT",
    "Cache Ward, UT",
    "Smithfield, UT",
    "Hyrum, UT",
    "Eden, UT",
    "Liberty, UT",
    "Huntsville, UT",
    
    # Utah County & Mountain Suburbs
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
    
    # Summit & Wasatch Back
    "East Basin, UT",
    "Hoytsville, UT",
    "Marion, UT",
    "Coalville, UT",
    "Heber City, UT",
    "Kamas, UT",
    
    # Southern & Rural Utah CDPs / Unincorporated Areas
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
    selected_location = st.selectbox(
        "Utah City Search", all_locations, label_visibility="collapsed"
    )
with f_col2:
    status_filter = st.selectbox(
        "Status", ["Contracts for Sale", "All Statuses"], label_visibility="collapsed"
    )
with f_col3:
    price_filter = st.selectbox(
        "Contract Price",
        ["Any Price", "Under $30k", "$30k - $60k", "Over $60k"],
        label_visibility="collapsed",
    )
with f_col4:
    beds_filter = st.selectbox(
        "Beds",
        ["Beds & baths", "2+ Beds", "3+ Beds", "4+ Beds"],
        label_visibility="collapsed",
    )
with f_col5:
    type_filter = st.selectbox(
        "Contract Type",
        ["Property type", "House", "Land", "Townhouse", "Condo"],
        label_visibility="collapsed",
    )
with f_col6:
    save_search_btn = st.button("Save Search", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)  # End filter-bar-container
st.markdown("</div>", unsafe_allow_html=True)  # End sticky-header-wrapper

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

# Using Streamlit container and query params / session state to handle the interactive FAQ modal toggle cleanly
if "show_faq" not in st.session_state:
    st.session_state.show_faq = False

col_title_1, col_title_2 = st.columns([3, 1])
with col_title_1:
    st.markdown(
        f"""
        <div style="margin-top: 24px; margin-bottom: 16px;">
            <h1 style="font-size: 1.7rem; font-weight: 800; color: #111827; margin-bottom: 4px;">{location_title} Utah Real Estate & Land For Sale</h1>
            <p style="font-size: 0.95rem; color: #6b7280; margin: 0;"><b>{len(filtered_df)}</b> active private contracts available for acquisition</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

with col_title_2:
    st.markdown("<div style='margin-top: 36px; text-align: right;'>", unsafe_allow_html=True)
    if st.button("🛈 How private contract assignment works & FAQ", type="tertiary"):
        st.session_state.show_faq = not st.session_state.show_faq
    st.markdown("</div>", unsafe_allow_html=True)

# --- EXPANDABLE FAQ & EXPLANATION SECTION ---
if st.session_state.show_faq:
    st.markdown(
        """
        <div style="background-color: #ffffff; border: 1px solid #e5e7eb; border-left: 4px solid #d92228; padding: 24px; border-radius: 8px; margin-bottom: 30px; box-shadow: 0 4px 12px rgba(0,0,0,0.03);">
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
            with cols[idx]:
                st.markdown(
                    f"""
                        <div class="property-card">
                            <div class="card-img-container">
                                <img src="{row['image']}" class="card-img">
                                <div class="card-status-badge">{row['status']}</div>
                            </div>
                            <div class="card-body">
                                <div class="card-broker">{row['broker']}</div>
                                <div class="card-contract-price">Contract: ${row['contract_price']:,}</div>
                                <div class="card-underlying-price">Property Value: ${row['underlying_price']:,}</div>
                                <div class="card-metrics"><b>{row['beds']}</b> bds &nbsp;|&nbsp; <b>{row['baths']}</b> ba &nbsp;|&nbsp; <b>{row['sqft']:,}</b> sqft</div>
                                <div class="card-address">{row['address']}</div>
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
                        placeholder=(
                            "Enter contract purchase price, assignment fee, or escrow"
                            " contingencies..."
                        ),
                    )
                    if st.button("Submit Official Offer", key=f"p_btn_{row['id']}"):
                        if user_email:
                            send_offer_dispatch(row["id"], row["title"], user_email, offer_terms)
                            st.success("Offer successfully dispatched to escrow!")
                        else:
                            st.error("Please enter a valid email address.")

# --- MAP SECTION (Placing the Interactive PyDeck Map Below Listings, matching reference layout) ---
st.markdown(
    """
    <div style="margin-top: 40px; margin-bottom: 16px; border-top: 1px solid #e5e7eb; padding-top: 24px;">
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
    get_position="[longitude, latitude]",
    get_color="[217, 34, 40, 230]",
    get_radius=1000,
    pickable=True,
    auto_highlight=True,
)

lat_center = filtered_df["lat"].mean() if not filtered_df.empty else 40.6977
lon_center = filtered_df["lon"].mean() if not filtered_df.empty else -111.8550
zoom_level = 10 if selected_location != "All Utah Cities" else 7

view_state = pdk.ViewState(
    latitude=lat_center, longitude=lon_center, zoom=zoom_level, pitch=0
)

r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    map_style="light",
    tooltip={"text": "Utah Land & Property Equitable Interest Contract"},
)
st.pydeck_chart(r, use_container_width=True)

# --- FOOTER SECTION (Exemption & Private Investment Notice) ---
st.markdown(
    """
    <div style="font-size: 0.8rem; color: #6b7280; text-align: center; margin-top: 40px; padding-top: 24px; border-top: 1px solid #e5e7eb; padding-bottom: 40px; line-height: 1.6;">
        Notice: Utah Land & Property Inc. is a private investment firm and is not a licensed real estate broker or agent.<br>
        We do not represent third parties in the purchase, sale, or management of outside real estate.<br>
        Pursuant to the exemption under Utah Code § 61-2f-202, all property management functions are executed solely by individuals,<br>
        operating as regular salaried employees of the specific legal entities that own the underlying real estate assets.
    </div>
""",
    unsafe_allow_html=True,
)
