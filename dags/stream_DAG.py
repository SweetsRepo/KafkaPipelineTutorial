"""
DAG to emulate periodic update of data. Each hour, a new set of samples will be "produced"
"""
import airflow
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator

from src.data.kafka_producer import generate_stream

PATH_STREAM_SAMPLE = "/data/stream_sample.p"

# Set airflow as owner of DAG, make sure that DAG is triggered from current date onwards, pass variables from one task to another
args = {
    "owner": "airflow",
    "start_date": airflow.utils.dates.days_ago(1),
    "provide_context": True
}

# Since this is just the initial model, we only need to run once
dag = DAG(
    dag_id = "intial_model_DAG",
    default_args = args,
    schedule_interval = "@hourly",
    catchup=False
)

task = PythonOperator(
    task_id = "generate_stream",
    python_callable = generate_stream,
    op_kwargs = {
        "path_stream_sample": PATH_STREAM_SAMPLE
    },
    dag = dag
)
