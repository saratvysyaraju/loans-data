from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, String, Numeric, ForeignKey, Date

import datetime

Base = declarative_base()


class Member(Base):
    """
    Mapping class for the dim_member table
    """
    __tablename__ = 'dim_member'

    # Created the dimension table to reduce repetitive info about the member/borrower
    member_id = Column(Numeric, primary_key=True)
    emp_title = Column(String)
    emp_length = Column(String)
    home_ownership = Column(String)
    annual_inc = Column(Numeric)
    zip_code = Column(String)
    addr_state = Column(String)
    last_updated = Column(DateTime, default=datetime.datetime.utcnow)


class Loan(Base):
    """
    Mapping class for the fct_loan table
    """
    __tablename__ = 'fct_loan'

    # Established the ForeignKey relationship and added not null condition for same data validation
    # Designed the schema with fewer columns to improve query speed and showcase cleaner data
    id = Column(Numeric, primary_key=True)
    member_id = Column(Numeric, ForeignKey('dim_member.member_id'))
    loan_amnt = Column(Numeric, nullable=False)
    funded_amnt = Column(Numeric, nullable=False)
    term = Column(String, nullable=False)
    int_rate = Column(String, nullable=False)
    installment = Column(Numeric, nullable=False)
    grade = Column(String)
    sub_grade = Column(String)
    verification_status = Column(String, nullable=False)
    issue_d = Column(Date, nullable=False)
    payment_plan = Column(String)
    revol_bal = Column(Numeric, nullable=False)
    total_pymnt = Column(Numeric, nullable=False)
    last_updated = Column(DateTime, default=datetime.datetime.utcnow)
