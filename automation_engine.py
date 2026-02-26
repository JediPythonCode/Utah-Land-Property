# automation_engine.py - Fixed Dynamic Utah Addendum Generator
from PyPDFForm import PdfWrapper
from library import SHIELD_LIBRARY
import os

def generate_utah_addendum(deal_data, selected_shield_keys):
    """
    Generates a Utah State-Approved Addendum with selectable shields.

    Parameters:
        deal_data (dict): {
            "seller_first": str,
            "seller_last": str,
            "address": str,
            "repc_date": str,
            "addendum_no": str,
            "acceptance_date": str,  # Optional, for REPC section 23
            "acceptance_time": str   # Optional
        }
        selected_shield_keys (list): List of keys from SHIELD_LIBRARY to include.

    Returns:
        str: Path to generated PDF or raises Exception if failed.
    """
    # 1️⃣ Compile selected shields
    compiled_provisions = "THE FOLLOWING TERMS are hereby incorporated as part of the REPC:\n\n"
    included_shields = [SHIELD_LIBRARY[k] for k in selected_shield_keys if k in SHIELD_LIBRARY]
    compiled_provisions += "\n\n".join(included_shields) if included_shields else "(No shields selected)"

    # 2️⃣ Map fields to PDF template
    seller_full_name = f"{deal_data.get('seller_first','')} {deal_data.get('seller_last','')}".strip()
    form_data = {
        "Addendum_No": deal_data.get("addendum_no", "1"),
        "REPC_Reference_Date": deal_data.get("repc_date", "02/26/2026"),
        "Buyer_Name": "Utah Land & Property Inc.",
        "Seller_Name": seller_full_name or "Unknown Seller",
        "Property_Address": deal_data.get("address", ""),
        "Provisions_Text": compiled_provisions,
        "Acceptance_Date": deal_data.get("acceptance_date", ""),
        "Acceptance_Time": deal_data.get("acceptance_time", "")
    }

    # 3️⃣ Load template
    template_path = "forms/utah_blank_addendum.pdf"
    if not os.path.exists(template_path):
        raise FileNotFoundError("Template not found at 'forms/utah_blank_addendum.pdf'")

    # 4️⃣ Fill PDF
    pdf = PdfWrapper(template_path).fill(form_data, flatten=True)

    # 5️⃣ Save filled PDF
    output_dir = "contracts/finalized"
    os.makedirs(output_dir, exist_ok=True)
    safe_name = seller_full_name.replace(" ", "_") or "Unknown_Seller"
    output_path = f"{output_dir}/{safe_name}_Addendum_{form_data['Addendum_No']}.pdf"
    pdf.write(output_path)

    if not os.path.exists(output_path):
        raise FileNotFoundError("PDF generation failed.")

    return output_path


# ----------------- Example Usage -----------------
if __name__ == "__main__":
    # Example deal
    example_deal = {
        "seller_first": "Owen",
        "seller_last": "Smith",
        "address": "123 Draper Town Center Way, Draper, UT",
        "repc_date": "02/26/2026",
        "addendum_no": "1",
        "acceptance_date": "03/01/2026",
        "acceptance_time": "5:00 PM"
    }

    shields_to_include = [
        "Legacy_Unit_SNDA",
        "FinCEN_2026",
        "As_Is_Condition",
        "Unrestricted_Assignment"
    ]

    try:
        pdf_path = generate_utah_addendum(example_deal, shields_to_include)
        print(f"✅ Success! PDF generated at: {pdf_path}")
    except Exception as e:
        print(f"❌ Error generating PDF: {e}")
