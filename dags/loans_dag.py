"""
Daily DAG to load, process and transform the loans data
"""
from __future__ import print_function

import datetime
import utils

from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator, ShortCircuitOperator
from airflow.contrib.sensors.python_sensor import PythonSensor

# Set of default arguments predefined for each task/job in this DAG
default_args = {
    'owner': 'Sarat Vysyaraju',
    'start_date': datetime.datetime(2019, 1, 1, 0, 0),
    'depends_on_past': False,                                # Ensure present run waits for previous dag run
    'email': ['saratchandra9494@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': datetime.timedelta(minutes=5)
}

dag = DAG(
    dag_id='loans_dag',
    default_args=default_args,
    schedule_interval='@daily'                              # Assuming we want to run the ETL daily expecting new data
)
dag.catchup = True
dag.doc_md = __doc__

wait_for_loans_sensor = PythonSensor(
    task_id='wait_for_loans',
    dag=dag,
    python_callable=utils.check_loans_file_exists,
    provide_context=True
)

# If the daily loan records file is empty, no new records are inserted into source table
# and the downstream tasks are skipped using the ShortCircuitOperator
load_job = ShortCircuitOperator(
    task_id='load_loans',
    dag=dag,
    python_callable=utils.load_loans,
    provide_context=True
)

update_members_job = PythonOperator(
    task_id='update_dim_member',
    dag=dag,
    python_callable=utils.update_members,
    provide_context=True
)

add_new_loans_job = PythonOperator(
    task_id='update_fct_loan',
    dag=dag,
    python_callable=utils.add_loans,
    provide_context=True
)


wait_for_loans_sensor >> load_job >> (update_members_job, add_new_loans_job)
