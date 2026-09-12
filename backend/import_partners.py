import csv
from app.database import SessionLocal
from app.models import ChannelPartner


SCHEME_TYPE_TO_ID = {
    "Micro Finance Scheme (MFS)": "SCH001",
    "Term Loan": "SCH002",
    "Aajeevika Micro-Finance Yojana (AMY)": "SCH003",
    "Udyam Nidhi Yojana (UNY)": "SCH004",
    "Educational Loan Scheme (ELS)": "SCH005",
}


CITY_TO_DISTRICT = {
    "tadepalli": "Guntur", "amaravathi": "Guntur", "vijayawada": "Krishna",
    "guntur": "Guntur", "guwahati": "Kamrup Metropolitan", "dispur": "Kamrup Metropolitan",
    "patna": "Patna", "chandigarh": "Chandigarh", "naya raipur": "Raipur", "nava raipur": "Raipur",
    "silvassa": "Dadra and Nagar Haveli", "rohini": "North West Delhi", "dwarka": "South West Delhi",
    "rajendra place": "Central Delhi", "gandhinagar": "Gandhinagar", "vadodara": "Vadodara",
    "bharuch": "Bharuch", "ahmedabad": "Ahmedabad", "panaji": "North Goa", "solan": "Solan",
    "mandi": "Mandi", "ranchi": "Ranchi", "srinagar": "Srinagar", "jammu": "Jammu",
    "bengaluru": "Bengaluru Urban", "mysuru": "Mysuru", "thrissur": "Thrissur", "malappuram": "Malappuram",
    "bhopal": "Bhopal", "indore": "Indore", "mumbai": "Mumbai City", "juhu": "Mumbai Suburban",
    "chembur": "Mumbai Suburban", "nariman point": "Mumbai City", "pune": "Pune", "aurangabad": "Aurangabad",
    "latur": "Latur", "imphal east": "Imphal East", "imphal": "Imphal West", "shillong": "East Khasi Hills",
    "aizwal": "Aizawl", "aizawl": "Aizawl", "bhubaneshwar": "Khordha", "bhubaneswar": "Khordha",
    "puducherry": "Puducherry", "jalandhar": "Jalandhar", "kapurthala": "Kapurthala",
    "jaipur": "Jaipur", "jodhpur": "Jodhpur", "gangtok": "Gangtok", "chennai": "Chennai",
    "royapetta": "Chennai", "salem": "Salem", "hyderabad": "Hyderabad", "agartala": "West Tripura",
    "dehradun": "Dehradun", "lucknow": "Lucknow", "gomti nagar": "Lucknow", "kolkata": "Kolkata",
    "salt lake": "North 24 Parganas", "bidhannagar": "North 24 Parganas", "howrah": "Howrah",
    "kamrup": "Kamrup", "chhaygaon": "Kamrup", "ratu road": "Ranchi", "rohtak": "Rohtak",
    "gurugram": "Gurugram", "jalandhar": "Jalandhar", "sunderpada": "Khordha",
}

def infer_district(state, address):
    if not address:
        return None
    text = str(address).lower()
    for city, district in CITY_TO_DISTRICT.items():
        if city in text:
            return district
    return None


def parse_bool(value):
    if value is None or str(value).strip() == "":
        return None

    return str(value).strip().lower() in {
        "true",
        "1",
        "yes",
        "y",
    }


def parse_float(value):
    if value is None or str(value).strip() == "":
        return None

    try:
        return float(str(value).replace(",", "").strip())
    except ValueError:
        return None


def parse_scheme_types(value):
    if not value:
        return []

    return [
        item.strip()
        for item in str(value).split(";")
        if item.strip()
    ]


def main():
    db = SessionLocal()

    try:
        with open(
            "partners_seed.csv",
            "r",
            encoding="utf-8-sig",
            newline=""
        ) as file:

            reader = csv.DictReader(file)

            imported = 0
            updated = 0
            warnings = 0

            for row in reader:

                partner_id = row["partner_id"].strip()

                scheme_types = parse_scheme_types(
                    row.get("supported_scheme_types")
                )

                scheme_ids = []

                for scheme_type in scheme_types:
                    scheme_id = SCHEME_TYPE_TO_ID.get(scheme_type)

                    if scheme_id:
                        scheme_ids.append(scheme_id)
                    else:
                        print(
                            f"WARNING: Unknown scheme type "
                            f"'{scheme_type}' for {partner_id}"
                        )
                        warnings += 1

                existing = db.query(ChannelPartner).filter(
                    ChannelPartner.partner_id == partner_id
                ).first()

                data = {
                    "partner_id": partner_id,
                    "name": row.get("name"),
                    "type": row.get("type"),
                    "state": row.get("state"),
                    "district": row.get("district") or infer_district(row.get("state"), row.get("address")),
                    "address": row.get("address"),
                    "contact_number": row.get("contact_number"),
                    "email": row.get("email"),
                    "navigation_link": row.get("navigation_link") or None,
                    "active": parse_bool(row.get("active")),
                    "supported_scheme_types": scheme_types,
                    "supported_scheme_ids": scheme_ids,
                    "fund_utilization_status":
                        row.get("fund_utilization_status") or None,
                    "npa_percentage":
                        parse_float(row.get("npa_percentage")),
                    "eligible_for_new_applications":
                        parse_bool(
                            row.get("eligible_for_new_applications")
                        ),
                }

                if existing:
                    for key, value in data.items():
                        setattr(existing, key, value)

                    updated += 1

                else:
                    partner = ChannelPartner(**data)
                    db.add(partner)
                    imported += 1

            db.commit()

            print()
            print("===================================")
            print("PARTNER IMPORT COMPLETED")
            print("===================================")
            print(f"New partners : {imported}")
            print(f"Updated      : {updated}")
            print(f"Warnings     : {warnings}")
            print("===================================")

    finally:
        db.close()


if __name__ == "__main__":
    main()