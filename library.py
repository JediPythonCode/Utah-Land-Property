# library.py - 2026 Wholesaler Shield Logic (EXPANDED & COMPLETE v2.0)
# Updated February 2026 - Now 27 shields across 9 categories
# Covers creative finance, assignment, subject-to, Utah licensing, FinCEN/BOI,
# property condition, title/equitable interest, default limitations, and general enforcement.

SHIELD_LIBRARY = {
    # --- 1. THE "PACE MORBY" SPECIALS (Creative Finance & Assignment) ---
    "Assignment_Gator": (
        "ASSIGNMENT & PROFIT DISCLOSURE: Seller acknowledges that Buyer is a professional investor "
        "and intends to assign this contract to an end-buyer for a substantial fee. Buyer is not "
        "purchasing the property to reside in it. Seller acknowledges the purchase price was negotiated "
        "at arm's length and waives any claim to the assignment fee or future profit realized by Buyer."
    ),
    "Marketing_Rights": (
        "MARKETING & ACCESS: Seller grants Buyer the right to market Buyer’s equitable interest in this "
        "contract, which includes professional photography, virtual tours, and listing on investor "
        "platforms. Seller shall provide access to the property within 24 hours' notice for 'Partner Walkthroughs'."
    ),
    "SubTo_Disclosure": (
        "SUBJECT-TO ACKNOWLEDGMENT: Seller understands that the existing loan will remain in Seller's name "
        "after closing. Seller acknowledges the risk of the 'Due on Sale' clause and confirms they have "
        "consulted with independent counsel regarding the impact on their credit and future borrowing power."
    ),

    # --- 2. THE "ATTORNEY-APPROVED" UTAH SHIELDS (Licensing & Agency) ---
    "Non_Agency_61_2f": (
        "UTAH CODE § 61-2f DISCLOSURE: Buyer is acting solely as a Principal and NOT as a real estate "
        "agent, broker, or fiduciary. Buyer does not represent the Seller. Seller is advised that "
        "Utah Land & Property Inc. is unlicensed and is only selling its 'Equitable Interest' in "
        "the contract, not the real property itself."
    ),
    "Market_Value_Disclaimer": (
        "MARKET VALUE ACKNOWLEDGMENT: Seller acknowledges that the Purchase Price may be significantly "
        "above or below the current fair market value. Buyer has not provided an appraisal. Seller relies "
        "solely on their own research to determine if the price is acceptable."
    ),

    # --- 3. THE 2026 COMPLIANCE SHIELDS (FinCEN & BOI) ---
    "FinCEN_2026": (
        "RESIDENTIAL REAL ESTATE RULE (FINCEN): Per the March 1, 2026 mandate, Seller agrees to cooperate "
        "with the Title Company/Reporting Person by providing all necessary 'Beneficial Ownership' data. "
        "Both parties acknowledge that non-financed transfers to legal entities trigger mandatory "
        "federal reporting."
    ),
    "BOI_Compliance": (
        "BOI WARRANTY: Buyer warrants that it is in full compliance with the Corporate Transparency Act. "
        "Any failure by Buyer to maintain valid BOI filings with FinCEN shall not constitute a Seller default."
    ),

    # --- 4. THE "DOUGLAS STEWART" DEAL-MAKERS (Specific to Owen's Lot) ---
    "Legacy_Unit_SNDA": (
        "SNDA FOR LIFE LEASE: Buyer/Assignee shall provide a recorded Subordination, Non-Disturbance, "
        "and Attornment Agreement (SNDA) ensuring Seller’s Life Lease survives any future foreclosure "
        "or transfer of the property."
    ),
    "Shared_Parking_REA": (
        "REA COOPERATION: Seller agrees to execute a Reciprocal Easement Agreement (REA) for shared "
        "parking and access as required by Draper City to facilitate the 18,000 sq ft mixed-use build."
    ),

    # --- 5. PROPERTY CONDITION & INSPECTION SHIELDS ---
    "As_Is_Condition": (
        "AS-IS CONDITION ACKNOWLEDGMENT: Seller understands and agrees that the Property is sold "
        "'AS-IS, WHERE-IS, WITH ALL FAULTS'. Buyer and any assignee make no representations or warranties "
        "whatsoever regarding the condition, habitability, environmental status, or code compliance of the Property. "
        "Seller has had full opportunity to inspect or has knowingly and voluntarily waived inspection."
    ),
    "Condition_Claims_Release": (
        "CONDITION CLAIMS RELEASE: Seller hereby fully and forever releases Buyer, its principals, "
        "assignees, and successors from any and all claims, liabilities, or demands related to the physical, "
        "environmental, structural, or latent condition of the Property, whether known or unknown, "
        "discovered before or after closing."
    ),
    "Seller_Defect_Disclosure": (
        "SELLER DEFECT DISCLOSURE: Seller warrants that they have disclosed in writing all known material "
        "defects, repairs needed, or code violations. Seller shall indemnify Buyer against any undisclosed defects."
    ),

    # --- 6. TITLE, EQUITABLE INTEREST & CLOSING SHIELDS ---
    "Equitable_Interest_Only": (
        "EQUITABLE INTEREST ONLY: Buyer is acquiring and conveying only its equitable interest under this Agreement. "
        "Buyer provides no warranty of title, marketability, possession, or absence of liens beyond what Seller warrants. "
        "Any title policy or guarantees shall be the responsibility of the ultimate end-buyer at final closing."
    ),
    "Recording_Prohibition": (
        "RECORDING PROHIBITED: Neither this Agreement nor any memorandum or notice thereof shall be recorded "
        "in the public records without the prior written consent of Buyer. Any unauthorized recording by Seller "
        "shall constitute a material default and grounds for immediate termination."
    ),
    "Seller_Title_Warranty": (
        "SELLER TITLE WARRANTY: Seller represents and warrants that they are the sole lawful owner, have full authority "
        "to contract, and the Property is free of all undisclosed liens, judgments, taxes, assessments, or encumbrances."
    ),
    "Closing_Cooperation": (
        "CLOSING COOPERATION: Seller agrees to promptly deliver all requested documents, affidavits, tax forms, "
        "payoff statements, and information to the Title Company and Buyer within 48 hours of any request to ensure "
        "clear title and timely closing."
    ),

    # --- 7. ASSIGNMENT EXPANSION & DEFAULT PROTECTIONS ---
    "Unrestricted_Assignment": (
        "UNRESTRICTED ASSIGNMENT RIGHTS: Buyer may assign or transfer this Agreement or its equitable interest "
        "to any third party at any time without Seller's consent, notice, or approval. Seller shall cooperate fully "
        "with any assignee and shall not interfere with Buyer's marketing or assignment activities."
    ),
    "Closing_Extension_Option": (
        "CLOSING EXTENSION OPTION: Buyer may extend the Closing Date for up to 90 cumulative days by delivering "
        "written notice and paying a non-refundable extension fee of $1,000 per 30-day period. Each extension is "
        "at Buyer's sole discretion."
    ),
    "Buyer_Default_Limited_Remedy": (
        "BUYER DEFAULT - LIMITED REMEDY: In the event of Buyer default, Seller's sole and exclusive remedy shall be "
        "retention of the earnest money deposit as liquidated damages. Seller expressly waives specific performance, "
        "actual damages, consequential damages, or any other legal or equitable relief against Buyer or its assignees."
    ),
    "Seller_Indemnification": (
        "SELLER INDEMNIFICATION: Seller shall defend, indemnify, and hold harmless Buyer, its officers, members, "
        "assignees, and agents from any and all claims, losses, damages, costs, attorney fees, or liabilities "
        "arising from Seller's breach of any representation, warranty, covenant, or from any pre-closing condition of title or property."
    ),

    # --- 8. GENERAL LEGAL & ENFORCEMENT SHIELDS ---
    "Governing_Law_Utah": (
        "GOVERNING LAW & VENUE: This Agreement shall be governed exclusively by the laws of the State of Utah. "
        "Exclusive venue for any dispute shall be the state or federal courts sitting in Salt Lake County, Utah."
    ),
    "Prevailing_Party_Attorney_Fees": (
        "ATTORNEY FEES: The prevailing party in any litigation, arbitration, or other proceeding arising from "
        "this Agreement shall be entitled to recover its reasonable attorney fees, costs, and expenses from the non-prevailing party."
    ),
    "Entire_Agreement": (
        "ENTIRE AGREEMENT & MERGER CLAUSE: This Agreement, together with any attached exhibits or addenda, "
        "constitutes the entire agreement between the parties and supersedes all prior understandings, "
        "representations, or agreements, whether oral or written."
    ),
    "Severability": (
        "SEVERABILITY: If any provision of this Agreement is held invalid or unenforceable, the remaining provisions "
        "shall remain in full force and effect."
    ),
    "Time_Is_Essence": (
        "TIME IS OF THE ESSENCE: All dates, timelines, and performance obligations in this Agreement are of the essence "
        "and strictly enforceable."
    ),
    "Electronic_Signatures": (
        "ELECTRONIC SIGNATURES & DELIVERY: The parties agree that electronic signatures (including via DocuSign, "
        "Adobe Sign, or email) and electronic delivery shall have the same legal effect as original signatures "
        "pursuant to the Utah Uniform Electronic Transactions Act and the federal ESIGN Act."
    ),
    "Force_Majeure_2026": (
        "FORCE MAJEURE: Neither party shall be liable for any delay or failure to perform caused by events beyond "
        "its reasonable control, including (but not limited to) new or amended FinCEN rules, state real estate regulations, "
        "government orders, natural disasters, or pandemics."
    ),
    "Bankruptcy_Warranty": (
        "BANKRUPTCY & AUTHORITY WARRANTY: Seller warrants that they are not a debtor in any bankruptcy or insolvency "
        "proceeding and that execution of this Agreement will not violate any court order or automatic stay."
    ),
    "Commission_Waiver": (
        "COMMISSION WAIVER: Seller acknowledges that no real estate brokerage commission or fee is owed to any broker "
        "unless separately disclosed and agreed in writing. Seller waives any claim against Buyer for brokerage fees."
    )
}

# Usage example:
# def get_shield(key: str) -> str:
#     return SHIELD_LIBRARY.get(key, "SHIELD NOT FOUND - Add to library")
