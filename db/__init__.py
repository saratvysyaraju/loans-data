import logging
import pandas as pd
from sqlalchemy import create_engine


def connect(db_file='/Users/svysyara/Downloads/database.sqlite'):
    """
    Method that returns a connection object to the sqlite db

    :param db_file: Path to the sqlite database file
    :type db_file: string
    :returns: Connection object to the sqlite database
    :rtype: connection object
    """
    # For simplicity assuming that the database is always sqlite
    engine = create_engine('sqlite:///{sqlite_file_name}'.format(sqlite_file_name=db_file))
    conn = engine.connect()
    return conn


def run(sql):
    """
    Given a sql statement, runs it on the sqlite db and commits the transaction
    :param sql: SQL to run on the SQLite db
    :type sql: string
    """
    conn = connect()
    transaction = conn.begin()
    logging.info("Executing sql:\n{sql}".format(sql=sql))
    conn.execute(sql)
    transaction.commit()


def add_data(table_name, source_file, insert_type='append'):
    """
    Method to add more rows of data to the specified sqlite table

    :param table_name: Name of the table to which rows of data are to be added
    :type table_name: string
    :param source_file: Path to the csv file for data to be added
    :type source_file: string
    :param insert_type: Type of insert operation. Default: append
        {'append', 'replace'}
    :type insert_type: string
    """
    db_conn = connect()
    logging.info("Loading data from file: {file}".format(file=source_file))
    new_data = pd.read_csv(source_file, sep=',', error_bad_lines=False, low_memory=False)
    new_data.to_sql(name=table_name, con=db_conn, if_exists=insert_type)
    logging.info("Added {rows} rows of data to the {table_name} table".format(rows=len(new_data.index),
                                                                              table_name=table_name))
