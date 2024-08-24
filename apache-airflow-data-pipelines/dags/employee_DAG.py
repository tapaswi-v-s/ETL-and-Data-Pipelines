import datetime, pendulum, os, requests
from datetime import timedelta
import employee_dag_SQL_Statements

from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.utils.dates import days_ago

@dag(
    dag_id = 'process_employee',
    schedule_interval="0 0 * * *",
    start_date=days_ago(0),
    catchup=False,
    dagrun_timeout=timedelta(minutes=60),
)
def ProcessEmployees():
    output_dir = '/opt/airflow/data'
    employee_csv_file = 'employees.csv'
    url = 'https://raw.githubusercontent.com/apache/airflow/main/docs/apache-airflow/tutorial/pipeline_example.csv'
    
    @task
    def create_output_directory():
        os.makedirs(output_dir, exist_ok=True)


    create_employee_table = SQLExecuteQueryOperator(
        task_id = 'create_employee_table',
        conn_id = 'employee_db_conn',
        sql = employee_dag_SQL_Statements.CREATE_EMPLOYEE_TABLE
    )

    create_employees_temp_table = SQLExecuteQueryOperator(
        task_id="create_employees_temp_table",
        conn_id = 'employee_db_conn',
        sql = employee_dag_SQL_Statements.CREATE_EMPLOYEE_TEMP_TABLE
    )

    @task
    def get_data():
        response = requests.get(url)

        with open(f'{output_dir}/{employee_csv_file}', 'w') as file:
            if response.status_code == 200:
                file.write(response.text)
            else:
                file.write("Something went wrong...")
        
        postgres_hook = PostgresHook(postgres_conn_id="employee_db_conn")
        conn = postgres_hook.get_conn()
        cur = conn.cursor()

        with open(f'{output_dir}/{employee_csv_file}', "r") as file:
            cur.copy_expert(
                "COPY EMPLOYEES_TEMP FROM STDIN WITH CSV HEADER DELIMITER AS ',' QUOTE '\"'",
                file
            )
        conn.commit()
    
    @task
    def merge_data():
        try:
            pg_hook = PostgresHook(postgres_conn_id="employee_db_conn")
            conn = pg_hook.get_conn()
            cur = conn.cursor()
            cur.execute(employee_dag_SQL_Statements.MERGE_DATA_QUERY)
            conn.commit()
            return 0
        except Exception as e:
            return 1
        
    [create_output_directory(), create_employee_table, create_employees_temp_table] >> \
        get_data() >> merge_data()

dag = ProcessEmployees()