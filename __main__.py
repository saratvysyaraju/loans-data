import db
import logging

from db.tables import Member, Loan


def main():
    """
    Method to run during the initialization of this application/module
    """
    conn = db.connect()
    # Creates the dim_member and fct_loan table at the beginning of the application
    for table in [Member, Loan]:
        logging.info("Creating table {table_name}".format(table_name=table.__tablename__))
        table.__table__.create(conn)
    init_dim_member()
    init_fct_loan()


def init_dim_member():
    """
    Initialisation script for dim_member table
    """

    # Once the table is created, insert_members_sql is run
    # We insert all relevant member info for all historic data
    insert_members_sql = """
INSERT OR REPLACE INTO dim_member (member_id, emp_title, emp_length, home_ownership, annual_inc, zip_code, addr_state)
SELECT DISTINCT member_id,
    emp_title,
    emp_length,
    home_ownership,
    annual_inc,
    zip_code,
    addr_state
FROM loan
    """

    db.run(insert_members_sql)


def init_fct_loan():
    """
    Initialisation script for fct_loan table
    """

    # Once the table is created, insert_loans_sql is run
    # We insert all loans with fewer important columns info for all historic data
    insert_loans_sql = """
INSERT OR REPLACE INTO fct_loan (id, member_id, loan_amnt, funded_amnt, term, int_rate, installment, grade, sub_grade, verification_status, issue_d, payment_plan, revol_bal, total_pymnt)
SELECT id,
       member_id,
       loan_amnt,
       funded_amnt,
       term,
       int_rate,
       installment,
       grade,
       sub_grade,
       verification_status,
       issue_d,
       pymnt_plan,
       revol_bal,
       total_pymnt
FROM loan
    """

    db.run(insert_loans_sql)


if __name__ == '__main__':
    main()
