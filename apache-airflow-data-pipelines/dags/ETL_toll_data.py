import requests, tarfile
import pandas as pd
from datetime import timedelta
from airflow.decorators import dag, task
from airflow.models import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator

tar_file_name = 'tolldata.tgz'
output_dir = '/opt/airflow/data'
csv_path = f'{output_dir}/{tar_file_name.split('.')[0]}'
csv_output_file_name = 'csv_data.csv'
tsv_output_file_name = 'tsv_data.csv'
fixed_width_output_file_name = 'fixed_width_data.csv'
extracted_output_file_name = 'extracted_data.csv'
transformed_file_name = 'transformed_data.csv'

def download_dataset():
    """To download the tar file"""
    url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Final%20Assignment/tolldata.tgz'
    response = requests.get(url)
    
    with open(f'{output_dir}/{tar_file_name}', 'wb') as file:
        file.write(response.content)

def untar_dataset():
    """To extract the tarball"""
    with tarfile.open(f'{output_dir}/{tar_file_name}') as tar:
        tar.extractall(f'{output_dir}/{tar_file_name.split('.')[0]}')

def extract_data_from_csv():
    """Extract data from the vehicle-data.csv"""
    vehicle_file_name = 'vehicle-data.csv'
    df = pd.read_csv(f'{csv_path}/{vehicle_file_name}', names=['Rowid', 'Timestamp', 'Anonymized Vehicle number', 'Vehicle type', 'Number of axles', 'Vehicle code'])
    new_df = df[['Rowid', 'Timestamp', 'Anonymized Vehicle number', 'Vehicle type']]
    new_df.to_csv(f'{csv_path}/{csv_output_file_name}', index=False)

def extract_data_from_tsv():
    """Extract the from tab separated file from the tollplaza-data.tsv"""
    toll_plaza_csv_file = 'tollplaza-data.tsv'

    df = pd.read_csv(f'{csv_path}/{toll_plaza_csv_file}', delimiter='\t', names=['Rowid', 'Timestamp', 'Anonymized Vehicle number', 'Vehicle type', 'Number of axles', 'Tollplaza id', 'Tollplaza code'])
    new_df = df[['Number of axles', 'Tollplaza id', 'Tollplaza code']]    
    new_df.to_csv(f'{csv_path}/{tsv_output_file_name}', index=False)

def extract_data_from_fixed_width():
    """Extracts data from fixed-width file payment-data.txt"""
    txt_file_name = 'payment-data.txt'
    
    with open(f'{csv_path}/{txt_file_name}', 'r', ) as file:
        file_content = file.read()
        file_content = file_content.split('\n')[:-1]
    
    # Type of Payment code: -2, Vehicle Code: -1
    data = []
    for line in file_content:
        chunks = line.strip().split(' ')
        data.append({'Type of Payment code':chunks[-2].strip(),
                      'Vehicle Code': chunks[-1].strip()})
    
    pd.DataFrame(data).to_csv(f'{csv_path}/{fixed_width_output_file_name}', index=False)

def consolidate_data():
    """ Creates a single csv file named extracted_data.csv by combining data 
    from the following files:
    csv_data.csv
    tsv_data.csv
    fixed_width_data.csv"""

    csv_df = pd.read_csv(f'{csv_path}/{csv_output_file_name}')
    tsv_df = pd.read_csv(f'{csv_path}/{tsv_output_file_name}')
    fix_width_df = pd.read_csv(f'{csv_path}/{fixed_width_output_file_name}')

    final_df = pd.concat([csv_df, tsv_df, fix_width_df], axis=1)
    final_df = final_df[['Rowid', 'Timestamp', 'Anonymized Vehicle number', 'Vehicle type', 
                         'Number of axles', 'Tollplaza id', 'Tollplaza code', 'Type of Payment code',
                         'Vehicle Code']]
    final_df.to_csv(f'{csv_path}/{extracted_output_file_name}', index=False)

def transform_data():
    df = pd.read_csv(f'{csv_path}/{extracted_output_file_name}')
    df['Vehicle type'] = df['Vehicle type'].apply(str.upper)
    df.to_csv(f'{csv_path}/{transformed_file_name}', index=False)

default_args = {
    'owner': 'Tapaswi',
    'start_date': days_ago(0),
    'email': ['satyapanthi.t@northeastern.edu'],
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'ETL_toll_data',
    default_args=default_args,
    description='Apache Airflow Final Assignment',
    schedule_interval=timedelta(days=1),
)

download_data = PythonOperator(
    task_id='download_data',
    python_callable=download_dataset,
    dag=dag
)

unzip_data = PythonOperator(
    task_id='unzip_data',
    python_callable=untar_dataset,
    dag=dag
)

extract_data_from_csv_task = PythonOperator(
    task_id='extract_data_from_csv',
    python_callable=extract_data_from_csv,
    dag=dag
)

extract_data_from_tsv_task = PythonOperator(
    task_id='extract_data_from_tsv',
    python_callable=extract_data_from_tsv,
    dag=dag
)

extract_data_from_fixed_width_task = PythonOperator(
    task_id='extract_data_from_fixed_width',
    python_callable=extract_data_from_fixed_width,
    dag=dag
)

consolidate_data_task = PythonOperator(
    task_id='consolidate_data',
    python_callable=consolidate_data,
    dag=dag
)

transform_data_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    dag=dag
)

download_data >> unzip_data >> extract_data_from_csv_task >> extract_data_from_tsv_task >> \
    extract_data_from_fixed_width_task >> consolidate_data_task >> transform_data_task