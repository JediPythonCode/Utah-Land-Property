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

# Custom Enterprise Styling: Modern Realtor/Zillow UI, Sticky Headers, Clean Card Grids
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@400;500;600;700;800;900&display=swap');

    :root {
        --brand-red: #d92228;
        --brand-red-hover: #b51b20;
        --bg-main: #f8f9fa;
        --bg-card: #ffffff;
        --border-color: #e5e7eb;
        --text-main: #1f2937;
        --text-muted: #6b7280;
    }
    
    .stApp {
        background-color: var(--bg-main) !important;
        color: var(--text-main) !important;
        font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }
    .main {
        background-color: var(--bg-main) !important;
        color: var(--text-main) !important;
        padding-top: 0px !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }

    /* Professional Property Card Grid Styling */
    .property-card {
        background-color: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 10px;
        overflow: hidden;
        margin-bottom: 24px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        transition: all 0.2s ease-in-out;
    }
    .property-card:hover {
        box-shadow: 0 10px 20px rgba(0,0,0,0.08);
        transform: translateY(-2px);
    }
    .card-img-container {
        position: relative;
        width: 100%;
        height: 220px;
    }
    .card-img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    .card-status-badge {
        position: absolute;
        top: 12px;
        left: 12px;
        background-color: rgba(17, 24, 39, 0.85);
        color: white;
        padding: 5px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.3px;
    }
    .card-body {
        padding: 16px;
    }
    .card-broker {
        font-size: 0.75rem;
        font-weight: 700;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }
    .card-contract-price {
        font-size: 1.4rem;
        font-weight: 800;
        color: var(--text-main);
        margin-bottom: 2px;
    }
    .card-underlying-price {
        font-size: 0.88rem;
        font-weight: 600;
        color: var(--brand-red);
        margin-bottom: 8px;
    }
    .card-metrics {
        font-size: 0.9rem;
        color: #374151;
        margin-bottom: 8px;
        font-weight: 500;
    }
    .card-address {
        font-size: 0.85rem;
        color: var(--text-muted);
        margin-bottom: 12px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .faq-link-style {
        color: #d92228 !important;
        font-weight: 600;
        text-decoration: none;
        cursor: pointer;
    }
    .faq-link-style:hover {
        text-decoration: underline;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Expanded Utah Property Database with Contracts for Sale
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

# List of Utah Locations
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


# --- REALTOR.COM HERO HEADER & SEARCH COMPONENT ---
st.markdown(
    """
    <style>
    .hero-container {
        position: relative;
        width: 100vw;
        left: calc(-50vw + 50%);
        margin-top: -60px;
        margin-bottom: 30px;
        height: 520px;
        background-image: linear-gradient(rgba(0, 0, 0, 0.35), rgba(0, 0, 0, 0.55)), url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=2000&q=85');
        background-size: cover;
        background-position: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        box-sizing: border-box;
        padding: 0 20px;
    }
    
    .hero-navbar {
        width: 100%;
        max-width: 1280px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 18px 0px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.15);
    }
    .hero-nav-left, .hero-nav-right {
        display: flex;
        gap: 22px;
        align-items: center;
        font-size: 0.9rem;
        font-weight: 600;
        color: #ffffff;
    }
    .hero-nav-left span, .hero-nav-right span {
        cursor: pointer;
        transition: opacity 0.15s ease;
    }
    .hero-nav-left span:hover, .hero-nav-right span:hover {
        opacity: 0.75;
    }
    .hero-logo {
        font-size: 1.6rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        color: #ffffff;
        text-decoration: none;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .hero-logo span {
        color: #d92228;
        background: white;
        padding: 1px 6px;
        border-radius: 4px;
    }
    
    .hero-content {
        text-align: center;
        margin-top: 65px;
        margin-bottom: 25px;
    }
    .hero-title-main {
        font-size: 2.8rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 0px;
        letter-spacing: -0.5px;
        font-family: 'Inter', sans-serif;
    }
    .hero-title-sub {
        font-size: 2.8rem;
        font-weight: 800;
        color: #ffffff;
        margin-top: 2px;
        margin-bottom: 20px;
        letter-spacing: -0.5px;
        font-family: 'Inter', sans-serif;
    }
    
    .hero-tabs {
        display: flex;
        justify-content: center;
        gap: 28px;
        margin-bottom: 14px;
        font-size: 0.95rem;
        font-weight: 600;
        color: rgba(255, 255, 255, 0.85);
    }
    .hero-tab-active {
        color: #ffffff;
        border-bottom: 3px solid #ffffff;
        padding-bottom: 4px;
    }
    
    .hero-browse-footer {
        width: 100%;
        max-width: 1280px;
        display: flex;
        justify-content: flex-start;
        margin-top: auto;
        padding-bottom: 24px;
        color: #ffffff;
        font-size: 0.95rem;
        font-weight: 500;
        text-shadow: 0 1px 3px rgba(0,0,0,0.4);
    }
    </style>

    <div class="hero-container">
        <div class="hero-navbar">
            <div class="hero-logo">
                <span>realtor</span>.com
            </div>
            <div class="hero-nav-left">
                <span>Buy</span>
                <span>Sell</span>
                <span>Rent</span>
                <span>Mortgage</span>
                <span>Find an Agent</span>
                <span>My Home</span>
                <span>News & Insights</span>
            </div>
            <div class="hero-nav-right">
                <span>Manage rentals</span>
                <span>Advertise</span>
                <span>Log in</span>
                <span style="background-color: #ffffff; color: #111827; padding: 7px 16px; border-radius: 20px; font-weight: 700;">Sign up</span>
            </div>
        </div>

        <div class="hero-content">
            <div class="hero-title-main">#1 real estate site</div>
            <div class="hero-title-sub">REALTOR® agents recommend*</div>
            
            <div class="hero-tabs">
                <span class="hero-tab-active">Buy</span>
                <span>Rent</span>
                <span>Sell</span>
                <span>Pre-approval</span>
                <span>Just sold</span>
                <span>Home value</span>
            </div>
        </div>

        <div class="hero-browse-footer">
            Browse homes in Millcreek, UT
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- FILTER BAR ---
f_col1, f_col2, f_col3, f_col4, f_col5, f_col6 = st.columns([2, 1.2, 1.2, 1, 1.2, 1])

with f_col1:
    selected_location = st.selectbox(
        "Utah City Search", all_locations, index=11, label_visibility="collapsed"
    )  # Defaults to Millcreek, UT
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
        <div style="margin-top: 24px; margin-bottom: 16px;">
            <h1 style="font-size: 1.7rem; font-weight: 800; color: #111827; margin-bottom: 4px;">{location_title} Utah Real Estate & Land For Sale</h1>
            <p style="font-size: 0.95rem; color: #6b7280; margin: 0;"><b>{len(filtered_df)}</b> active private contracts available for acquisition</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

with col_title_2:
    st.markdown(
        "<div style='margin-top: 36px; text-align: right;'>",
        unsafe_allow_html=True,
    )
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
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

# --- PROPERTY GRID DISPLAY ---
cols = st.columns(3)
for idx, row in filtered_df.reset_index(drop=True).iterrows():
    col = cols[idx % 3]
    with col:
        st.markdown(
            f"""
            <div class="property-card">
                <div class="card-img-container">
                    <img src="{row['image']}" class="card-img" />
                    <div class="card-status-badge">{row['status']}</div>
                </div>
                <div class="card-body">
                    <div class="card-broker">{row['broker']}</div>
                    <div class="card-contract-price">${row['contract_price']:,} <span style="font-size: 0.8rem; font-weight: 500; color: #6b7280;">(Contract Fee)</span></div>
                    <div class="card-underlying-price">Underlying Value: ${row['underlying_price']:,}</div>
                    <div class="card-metrics">{row['beds']} bds | {row['baths']} ba | {row['sqft']} sqft | {row['type']}</div>
                    <div class="card-address">{row['address']}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
