from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import re
import pandas as pd
import pydeck as pdk
import streamlit as st

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
