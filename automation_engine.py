# automation_engine.py - Dynamic Utah Addendum Generator
from PyPDFForm import PdfWrapper
from library import SHIELD_LIBRARY
import os

def generate_utah_addendum(deal_data, selected_shield_keys):
    """
    Generates a Utah State-Approved Addendum with selectable shields.
    
    deal_data dict should include:
        seller_first, seller_last, address, repc_date, addendum_no,
        acceptance_date, acceptance_time
    selected_shield_keys: list of SHIELD_LIBRARY keys to include
    
    Returns PDF path if successful.
    """
    # 1. Assemble the selected shields with header
    compiled_provisions = "THE FOLLOWING TERMS are hereby incorporated as part of the REPC:\n\n"
    included_shields = [
        SHIELD_LIBRARY[k] for k in selected_shield_keys if k in SHIELD_LIBRARY
    ]
    compiled_provisions += "\n\n".join(included_shields)
    if not included_shields:
        compiled_provisions += "(No shields selected)"

    # 2. Map fields to the PDF form
    seller_full_name = f"{deal_data.get('seller_first', '')} {deal_data.get('seller_last', '')}".strip()
    form_data = {
        "Addendum_No": deal_data.get("addendum_no", "1"),
        "REPC_Reference_Date": deal_data.get("repc_date", "02/26/2026"),
        "Buyer_Name": "Utah Land & Property Inc.",
        "Seller_Name": seller_full_name,
        "Property_Address": deal_data.get("address", ""),
        "Provisions_Text": compiled_provisions,
        "Acceptance_Date": deal_data.get("acceptance_date", ""),
        "Acceptance_Time": deal_data.get("acceptance_time", "")
    }

    # 3. Fill the PDF
    template_path = "forms/utah_blank_addendum.pdf"
    if not os.path.exists(template_path):
        return "Error: Template not found. Place utah_blank_addendum.pdf in forms/ folder."

    pdf = PdfWrapper(template_path).fill(form_data, flatten=True)

    # 4. Save the filled PDF
    output_dir = "contracts/finalized"
    os.makedirs(output_dir, exist_ok=True)
    output_filename = f"{output_dir}/{seller_full_name.replace(' ', '_')}_Addendum_{form_data['Addendum_No']}.pdf"

    pdf.write(output_filename)
    return output_filename
