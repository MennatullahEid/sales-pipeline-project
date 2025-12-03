from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

scripts_path = '/home/kiwilytics/Desktop/sales-pipeline-project/scripts'
sys.path.insert(0, scripts_path)

from process_sales import extract_sales_data, visualize_revenue

def run_sales_pipeline():
    """Execute the sales data pipeline"""
    print("Starting sales pipeline...")
    
    # Extract data
    df = extract_sales_data()
    
    # Create output directory
    output_dir = '/home/kiwilytics/Desktop/sales-pipeline-project/output'
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate visualization
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_path = os.path.join(output_dir, f'daily_revenue_{timestamp}.png')
    visualize_revenue(df, output_path)
    
    print("Sales pipeline completed!")

# Default arguments for the DAG
default_args = {
    'owner': 'kiwilytics',
    'depends_on_past': False,
    'start_date': datetime(2024, 12, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'sales_revenue_pipeline',
    default_args=default_args,
    description='Daily sales revenue analysis pipeline',
    schedule_interval='@daily',  # Run daily
    catchup=False,
)

# Define the task
sales_pipeline_task = PythonOperator(
    task_id='run_sales_pipeline',
    python_callable=run_sales_pipeline,
    dag=dag,
)