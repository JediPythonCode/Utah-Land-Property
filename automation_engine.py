# automation_engine.py - REVISED for Utah State Form Mapping
from PyPDFForm import PdfWrapper
from library import SHIELD_LIBRARY
import os

def generate_utah_addendum(deal_data, selected_shield_keys):
    """
    Automates the creation of a Utah State-Approved Addendum.
    Mapping is based on the standard 'blank-addendum.pdf' from commerce.utah.gov.
    """
    # 1. Logic Layer: Assemble selected shields with a 2026 Legal Header
    compiled_provisions = "THE FOLLOWING TERMS are hereby incorporated as part of the REPC:\n\n"
    compiled_provisions += "\n\n".join([SHIELD_LIBRARY[k] for k in selected_shield_keys if k in SHIELD_LIBRARY])

    # 2. Field Mapping for the Utah "Blank Addendum" (Standard Field Names)
    # Developer Note: These names must match the PDF's internal 'AcroForm' keys.
    form_data = {
        "Addendum_No": deal_data.get('addendum_no', "1"),
        "REPC_Reference_Date": deal_data.get('repc_date', "February 23, 2026"),
        "Buyer_Name": "Utah Land & Property Inc.",
        "Seller_Name": deal_data['seller'],
        "Property_Address": deal_data['address'],
        "Provisions_Text": compiled_provisions  # The bulk 'Shield' injection
    }

    # 3. Execution Layer: Fill and Flatten (Flattening prevents future edits)
    template_path = "forms/utah_blank_addendum.pdf"
    if not os.path.exists(template_path):
        return "Error: Template not found. Download from commerce.utah.gov"

    filled_pdf = PdfWrapper(template_path).fill(form_data, flatten=True)
    
    # 4. Output Management
    output_dir = "contracts/finalized"
    os.makedirs(output_dir, exist_ok=True)
    output_filename = f"{output_dir}/{deal_data['seller'].replace(' ', '_')}_Addendum_{deal_data['addendum_no']}.pdf"
    
    filled_pdf.write(output_filename)
    return f"Success! Addendum generated at: {output_filename}"

# --- AUTOMATED DEAL TRIGGER ---
owen_deal = {
    "address": "123 Draper Town Center Way, Draper, UT",
    "seller": "Owen [Last Name]",
    "repc_date": "02/26/2026",
    "addendum_no": "1"
}

# Shields that exist in your SHIELD_LIBRARY
shields = [
    "SubTo_Disclosure",          # Subject-To disclosure
    "Legacy_Unit_SNDA",          # Owen's Lot SNDA shield
    "FinCEN_2026",               # FinCEN compliance
    "BOI_Compliance",            # Beneficial Ownership compliance
    "As_Is_Condition",           # Property sold as-is
    "Condition_Claims_Release",  # Releases claims on property condition
    "Equitable_Interest_Only",   # Buyer only gets equitable interest
    "Closing_Cooperation"        # Seller must cooperate for closing
]

print(generate_utah_addendum(owen_deal, shields))
