import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Utah Land & Property Inc. | Wholesale Portals",
    page_icon="🏢",
    layout="wide",
)

# --- GLOBAL STYLING ---
st.markdown(
    """
    <style>
        .main {
            background-color: #f8fafc;
        }
        .section-header {
            font-size: 24px;
            font-weight: 800;
            color: #1e293b;
            margin-top: 30px;
            margin-bottom: 15px;
            padding-bottom: 8px;
            border-bottom: 2px solid #e2e8f0;
            letter-spacing: -0.5px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# --- PROPERTY DATABASE LOADER (TILA REGULATION Z COMPLIANT) ---
def load_utah_property_database():
    data = [
        # --- RESIDENTIAL ---
        {
            "id": "UT-RES-0101",
            "title": "Millcreek Condominium Asset",
            "category": "Residential",
            "city": "Millcreek, UT",
            "contract_price": 5000,
            "purchase_price": 150000,
            "arv": 210000,
            "beds": 1,
            "baths": 1,
            "sqft": 750,
            "status": "Available",
            "address": "4629 S Quail Vista Cove, Millcreek, UT 84117",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?auto=format&fit=crop&w=800&q=80",
            "lat": 40.6782,
            "lon": -111.8385,
        },
        {
            "id": "UT-RES-0102",
            "title": "Herriman Townhouse Opportunity",
            "category": "Residential",
            "city": "Herriman, UT",
            "contract_price": 7500,
            "purchase_price": 385000,
            "arv": 465000,
            "beds": 3,
            "baths": 2,
            "sqft": 1820,
            "status": "Available",
            "address": "5186 W Koppers Ln, Herriman, UT 84096",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1580587771525-78b9dba3b914?auto=format&fit=crop&w=800&q=80",
            "lat": 40.5283,
            "lon": -112.0194,
        },
        # --- RAW LAND ---
        {
            "id": "UT-LND-0201",
            "title": "Montello Desert Acreage Parcel",
            "category": "Raw Land",
            "city": "Montello, NV",
            "contract_price": 4000,
            "purchase_price": 45000,
            "arv": 85000,
            "beds": 0,
            "baths": 0,
            "sqft": 304920,  # 7 Acres
            "status": "Available",
            "address": "7-Acre Desert Parcel, Montello, NV 89830",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1509316975850-ff9c5deb0cd9?auto=format&fit=crop&w=800&q=80",
            "lat": 41.2589,
            "lon": -114.2156,
        },
        {
            "id": "UT-LND-0202",
            "title": "St. George Airport Development Tract",
            "category": "Raw Land",
            "city": "St. George, UT",
            "contract_price": 25000,
            "purchase_price": 1850000,
            "arv": 3200000,
            "beds": 0,
            "baths": 0,
            "sqft": 20037600,  # 460+ Acres
            "status": "UNDER CONTRACT",
            "address": "SGU Regional Growth Corridor, St. George, UT 84790",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 37.0965,
            "lon": -113.5184,
        },
        # --- COMMERCIAL ---
        {
            "id": "UT-COM-0301",
            "title": "Draper Town Center Commercial Infill",
            "category": "Commercial",
            "city": "Draper, UT",
            "contract_price": 15000,
            "purchase_price": 620000,
            "arv": 950000,
            "beds": 0,
            "baths": 0,
            "sqft": 15240,
            "status": "Available",
            "address": "12614 S Fort Street, Draper, UT 84020",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=800&q=80",
            "lat": 40.5273,
            "lon": -111.8591,
        },
        # --- INDUSTRIAL / SPECIAL USE ---
        {
            "id": "UT-IND-0401",
            "title": "North Salt Lake Industrial Off-Market Yard",
            "category": "Industrial",
            "city": "North Salt Lake, UT",
            "contract_price": 12500,
            "purchase_price": 480000,
            "arv": int(480000 * 1.32),
            "beds": 0,
            "baths": 0,
            "sqft": 21780,
            "status": "Available",
            "address": "Off-Market Industrial Way, North Salt Lake, UT 84054",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 40.8351,
            "lon": -111.9132,
        },
        {
            "id": "UT-IND-0401-B",
            "title": "North Salt Lake Fleet Storage Yard",
            "category": "Industrial",
            "city": "North Salt Lake, UT",
            "contract_price": 14000,
            "purchase_price": 510000,
            "arv": int(510000 * 1.35),
            "beds": 0,
            "baths": 0,
            "sqft": 32670,
            "status": "UNDER CONTRACT",
            "address": "Off-Market Industrial Way Parcel B, North Salt Lake, UT 84054",
            "broker": "Utah Land & Property Inc.",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "lat": 40.8355,
            "lon": -111.9138,
        },
    ]
    return pd.DataFrame(data)


df = load_utah_property_database()


# --- AUTOMATED EMAIL / OFFER DISPATCH HELPER ---
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


# --- RENDER FUNCTION FOR PROPERTY GRIDS (TILA REGULATION Z COMPLIANT) ---
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
                                    <div style="font-size: 16px; font-weight: 800; color: #111827; margin-bottom: 6px;">Contract Assignment Fee: ${row['contract_price']:,}</div>
                                    <div style="font-size: 13px; color: #374151; margin-bottom: 2px;">Property Purchase Price: <b>${row['purchase_price']:,}</b></div>
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

                        contract_terms_options = [
                            "Standard Cash Purchase (14-Day Close)",
                            "Subject-To Existing Mortgage Takeover",
                            "Seller Financing Options",
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
render_property_grid(
    df[df["category"] == "Industrial"], "Industrial", "industrial-section"
)

# --- RENDER LEGAL NOTICE FOOTER ---
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
