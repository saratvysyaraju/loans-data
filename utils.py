from __future__ import print_function

import logging
import os
from pathlib import Path

import db


def check_loans_file_exists(ds, **kwargs):
    """
    Given a dataset date the method returns True if loans file exists
    Assuming that a file be uploaded to the /tmp/loans/{dataset_date} directory
    with name 'loans.csv'

    :param ds: Dataset date
    :type ds: string
    :param kwargs: context arguments
    :param kwargs: dict
    :return: True if file found
    :rtype: bool
    """
    loans_file = Path('/tmp/loans/{dataset_date}/loan.csv'.format(dataset_date=ds))
    logging.info("Looking for file: {file_name}".format(file_name=loans_file))
    if loans_file.exists():
        return True


def load_loans(ds, **kwargs):
    """
    Method to load the loans data daily for a given dataset date
    Each day the job fetches a file from an expected location
    If an empty file is found, no records are added else new records
    are appended to the loans table

    :param ds: Dataset date
    :type ds: string
    :param kwargs: context arguments
    :param kwargs: dict
    """
    loans_file = Path('/tmp/loans/{dataset_date}/loan.csv'.format(dataset_date=ds))
    if not os.stat(loans_file).st_size == 0:
        db.add_data(table_name='loan',
                    source_file=loans_file,
                    insert_type='append')
        return True
    else:
        logging.info("Found empty file {file_name}, added zero rows".format(file_name=loans_file))
        return False


def update_members(ds, **kwargs):
    """
    Method to discover new/update Member records found daily from the loan table

    :param ds: Dataset date
    :type ds: string
    :param kwargs: context arguments
    :param kwargs: dict
    """

    # SQL to source distinct member ids and the relevant attributes found in loans data for a given dataset date
    # Assuming each day(dateset_date) loans issued on that day are added to the new file with issue_d as dataset date
    merge_new_members = """
INSERT OR REPLACE INTO dim_member (member_id, emp_title, emp_length, home_ownership, annual_inc, zip_code, addr_state)
SELECT DISTINCT member_id,
    emp_title,
    emp_length,
    home_ownership,
    annual_inc,
    zip_code,
    addr_state
FROM loan
WHERE issue_d = '{dataset_date}'
    """.format(dataset_date=ds)

    db.run(merge_new_members)


def add_loans(ds, **kwargs):
    """
    Method to discover and add new Loan records found daily from the loan table

    :param ds: Dataset date
    :type ds: string
    :param kwargs: context arguments
    :param kwargs: dict
    """

    # SQL to source new loans found with fewer attributes and load them into fct table for better query speed and also to isolate the source
    add_new_loans = """
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
WHERE issue_d = '{dataset_date}'
    """.format(dataset_date=ds)

    db.run(add_new_loans)
