from sqlalchemy import Column, Integer, String, Float, Boolean, JSON, ForeignKey
from app.database import Base


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer, nullable=False)
    state = Column(String, nullable=False)
    district = Column(String, nullable=False)
    annual_income = Column(Float, nullable=False)
    requested_amount = Column("project_cost", Float, nullable=True)
    category = Column(String, nullable=False)
    purpose = Column(String, nullable=False)
    business_education = Column(String, nullable=False)


class Scheme(Base):
    __tablename__ = "schemes"

    id = Column(Integer, primary_key=True, index=True)

    scheme_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    implementing_body = Column(String, nullable=False)
    channel = Column(String)

    project_cost_max = Column(Float)
    loan_min = Column(Float)
    loan_max = Column(Float)
    financing_percent_of_project = Column(Float)

    interest_rate_beneficiary_percent = Column(Float)
    interest_rate_via_channel_percent = Column(Float)

    tenure_years_max = Column(Float)
    moratorium_months = Column(Integer)
    repayment_frequency = Column(String)

    income_limit_annual = Column(Float)

    category_required = Column(JSON)
    gender_requirement = Column(String)

    purpose = Column(JSON)
    hard_filters = Column(JSON)

    eligibility_conditions = Column(String)

    documents_required = Column(JSON)   


    source_url = Column(String)
    data_verified = Column(Boolean, default=False)
    last_verified = Column(String)


class ChannelPartner(Base):
    __tablename__ = "channel_partners"

    id = Column(Integer, primary_key=True, index=True)

    partner_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)

    supported_scheme_types = Column(JSON)
    supported_scheme_ids = Column(JSON)

    state = Column(String)
    district = Column(String)
    address = Column(String)

    contact_number = Column(String)
    email = Column(String)
    navigation_link = Column(String)

    active = Column(Boolean, default=True)

    fund_utilization_status = Column(String)
    npa_percentage = Column(Float)

    eligible_for_new_applications = Column(Boolean, default=True)


class MatchResult(Base):
    __tablename__ = "match_results"

    id = Column(Integer, primary_key=True, index=True)

    profile_id = Column(Integer, ForeignKey("profiles.id"))
    scheme_id = Column(String)

    score = Column(Float)
    explanation = Column(String)