# automation_engine.py - Automated Deal Flow
from PyPDFForm import PdfWrapper
from library import SHIELD_LIBRARY

def generate_utah_addendum(deal_data, selected_shield_keys):
    # 1. Compile the text from your v3.0 Shield Library
    compiled_text = "\n\n".join([SHIELD_LIBRARY[k] for k in selected_shield_keys if k in SHIELD_LIBRARY])

    # 2. Map data to the Utah State-Approved Addendum fields
    # NOTE: You must inspect your PDF to get the exact field names (e.g., "Text1", "SellerName")
    form_data = {
        "Property_Address": deal_data['address'],
        "Seller_Name": deal_data['seller'],
        "Buyer_Name": "Utah Land & Property Inc.",
        "Addendum_Number": deal_data['addendum_no'],
        "Main_Text_Area": compiled_text  # This injects the 2026 Shields
    }

    # 3. Fill the State PDF
    template_path = "forms/utah_addendum_template.pdf"
    filled_pdf = PdfWrapper(template_path).fill(form_data)
    
    # 4. Save the finalized document
    output_filename = f"contracts/{deal_data['seller']}_Addendum_{deal_data['addendum_no']}.pdf"
    filled_pdf.write(output_filename)
    return output_filename

# Example Deal Trigger
my_deal = {
    "address": "Draper, UT .21 Acre Lot",
    "seller": "Owen [Last Name]",
    "addendum_no": "1"
}

# The "Surgical" Shield Selection for Owen
shields_to_use = [
    "Capacity_Sovereignty", 
    "Independent_Counsel", 
    "Legacy_Unit_SNDA", 
    "FinCEN_BOI_2026",
    "Non_Recourse_Entity"
]

generate_utah_addendum(my_deal, shields_to_use)
