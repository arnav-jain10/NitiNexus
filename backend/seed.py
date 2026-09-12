from app.database import SessionLocal
from app.models import Scheme


schemes = [
    {
        "scheme_id": "SCH001",
        "name": "Micro Finance Scheme (MFS)",
        "type": "Micro Finance",
        "implementing_body": "NSFDC",
        "channel": None,
        "loan_min": None,
        "loan_max": 125000,
        "financing_percent_of_project": 90,
        "interest_rate_beneficiary_percent": 6.5,
        "interest_rate_via_channel_percent": 2.5,
        "tenure_years_max": 3,
        "moratorium_months": 3,
        "repayment_frequency": "Quarterly",
        "income_limit_annual": 500000,
        "category_required": ["SC"],
        "gender_requirement": "Any",
        "purpose": ["small-scale income-generating activity"],
        "hard_filters": {
            "category_required": ["SC"],
            "income_max": 500000,
            "gender_requirement": "Any"
        },        
        
        "eligibility_conditions": "Applicant must belong to Scheduled Caste (SC) and annual family income must not exceed Rs 5 lakh.",
        "documents_required": ["Aadhaar Card / valid identity proof", "Caste Certificate", "Income Certificate", "Address / Residence Proof", "Passport-size Photograph", "Bank Account / Passbook", "Project / Business Proposal", "Proof of business/activity, if applicable", "Quotation for equipment/assets, if applicable"],
        "source_url": "https://nsfdc.nic.in/",
        "data_verified": False,
        "last_verified": "Pending official source verification"
    },
    {
        "scheme_id": "SCH002",
        "name": "Term Loan",
        "type": "Term Loan",
        "implementing_body": "NSFDC",
        "channel": None,
        "project_cost_max": 5000000,
        "loan_min": None,
        "loan_max": 4500000,
        "financing_percent_of_project": 90,
        "interest_rate_beneficiary_percent": 8,
        "interest_rate_via_channel_percent": 4,
        "tenure_years_max": 7,
        "moratorium_months": 6,
        "repayment_frequency": "Quarterly",
        "income_limit_annual": 500000,
        "category_required": ["SC"],
        "gender_requirement": "Any",
        "purpose": ["business setup", "business expansion"],
        "hard_filters": {
            "category_required": ["SC"],
            "income_max": 500000,
            "gender_requirement": "Any"
        },
        "eligibility_conditions": "Applicant must belong to Scheduled Caste (SC), annual family income must not exceed Rs 5 lakh, and the proposed activity must be eligible under the scheme.",
        "documents_required": ["Aadhaar Card / valid identity proof", "Caste Certificate", "Income Certificate", "Address / Residence Proof", "Passport-size Photograph", "Bank Account / Passbook", "Detailed Project Report (DPR)", "Business / Activity Proposal", "Machinery or Equipment Quotations", "Proof of business premises, if applicable", "Relevant registration/licence, if applicable"],
        "source_url": "https://nsfdc.nic.in/",
        "data_verified": False,
        "last_verified": "Pending official source verification"
    },
    {
        "scheme_id": "SCH003",
        "name": "Aajeevika Micro-Finance Yojana (AMY)",
        "type": "Micro Finance",
        "implementing_body": "NSFDC",
        "channel": "NBFC-MFI",
        "loan_min": None,
        "loan_max": 125000,
        "financing_percent_of_project": 90,
        "interest_rate_beneficiary_percent": 15,
        "interest_rate_via_channel_percent": 5,
        "tenure_years_max": 3,
        "moratorium_months": 3,
        "repayment_frequency": "Quarterly",
        "income_limit_annual": 500000,
        "category_required": ["SC"],
        "gender_requirement": "Any",
        "purpose": ["small/micro business activities"],
        "hard_filters": {
            "category_required": ["SC"],
            "income_max": 500000,
            "gender_requirement": "Any"
        },
        
        "eligibility_conditions": "Applicant must belong to Scheduled Caste (SC), annual family income must not exceed Rs 5 lakh, and the loan is delivered through NBFC-MFIs.",
        "documents_required": ["Aadhaar Card / valid identity proof", "Caste Certificate", "Income Certificate", "Address / Residence Proof", "Passport-size Photograph", "Bank Account / Passbook", "Self-help group / group membership proof, where applicable", "Business / Income-generating Activity Proposal", "Project / Activity Cost Estimate", "Relevant registration/licence, if applicable"],
        "source_url": "https://nsfdc.nic.in/",
        "data_verified": False,
        "last_verified": "Pending official source verification"
    },
    {
        "scheme_id": "SCH004",
        "name": "Udyam Nidhi Yojana (UNY)",
        "type": "Micro Finance",
        "implementing_body": "NSFDC",
        "channel": "Cooperative Societies / Cooperative Banks / Small Finance Banks (SFBs)",
        "project_cost_max": 500000,
        "loan_min": None,
        "loan_max": 450000,
        "financing_percent_of_project": 90,
        "interest_rate_beneficiary_percent": 13,
        "interest_rate_via_channel_percent": 5,
        "tenure_years_max": 5,
        "moratorium_months": 3,
        "repayment_frequency": "Quarterly or half-yearly",
        "income_limit_annual": 500000,
        "category_required": ["SC"],
        "gender_requirement": "Any",
        "purpose": ["small/micro business activities"],
        "hard_filters": {
            "category_required": ["SC"],
            "income_max": 500000,
            "gender_requirement": "Any"
        },

        "eligibility_conditions": "Applicant must belong to Scheduled Caste (SC), annual family income must not exceed Rs 5 lakh. Interest varies by channel: 13% through Cooperative Banks/Societies and 15% through Small Finance Banks.",
        "documents_required": ["Aadhaar Card / valid identity proof", "Caste Certificate", "Income Certificate", "Address / Residence Proof", "Passport-size Photograph", "Bank Account / Passbook", "Detailed Project Report (DPR)", "Business Plan", "Machinery / Equipment Quotations", "Proof of business premises, if applicable", "Udyam Registration / business registration, if applicable", "Relevant licence/permit, if applicable"],
        "source_url": "https://nsfdc.nic.in/",
        "data_verified": False,
        "last_verified": "Pending official source verification"
    },
    {
        "scheme_id": "SCH005",
        "name": "Educational Loan Scheme (ELS)",
        "type": "Education",
        "implementing_body": "NSFDC",
        "channel": None,
        "project_cost_max": 4000000,
        "loan_min": None,
        "loan_max": 4000000,
        "financing_percent_of_project": 90,
        "interest_rate_beneficiary_percent": 6.5,
        "interest_rate_via_channel_percent": 2.5,
        "tenure_years_max": 12,
        "moratorium_months": 6,
        "repayment_frequency": None,
        "income_limit_annual": 500000,
        "category_required": ["SC"],
        "gender_requirement": "Any",
        "purpose": ["full-time professional/technical courses"],
        "hard_filters": {
            "category_required": ["SC"],
            "income_max": 500000,
            "gender_requirement": "Any"
        },
        
        "eligibility_conditions": "Applicant must belong to Scheduled Caste (SC), annual family income must not exceed Rs 5 lakh, and the course must be a full-time professional or technical course.",
        "documents_required": ["Aadhaar Card / valid identity proof", "Caste Certificate", "Income Certificate", "Address / Residence Proof", "Passport-size Photograph", "Bank Account / Passbook", "Admission / Offer Letter from the educational institution", "Course / Programme details", "Fee Structure / Fee Demand Letter", "Previous academic marksheets/certificates", "Bonafide / student certificate, where applicable", "Education institution recognition/approval details, where applicable"],
        "source_url": "https://nsfdc.nic.in/",
        "data_verified": False,
        "last_verified": "Pending official source verification"
    }
]


db = SessionLocal()

try:
    # Remove old seed records
    db.query(Scheme).delete()

    # Add latest scheme dataset
    for data in schemes:
        db.add(Scheme(**data))

    db.commit()

    print("5 SCHEMES ADDED SUCCESSFULLY")

finally:
    db.close()