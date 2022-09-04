"""
DAG to train intial model, should only run once, and then be updated over time
"""
import airflow
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from src.models.initial_model_functions import load_preprocess, fit_model

# Constants for load preprocess
PATH_STREAM_SAMPLE = "/data/stream_sample.p"
PATH_TEST_SET = "/data/test_set.p"

# Constants for fitting model
INITIAL_MODEL_PATH = "/models/current_model/initial_model.H5"
BATCH_SIZE = 128
NUM_CLASSES = 10
EPOCHS = 4

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
    schedule_interval = "@once",
    catchup=False
)

# Create task to load preprocess data
task1 = PythonOperator(
    task_id="load_preprocess",
    python_callable=load_preprocess,
    op_kwargs = {
        "path_stream_sample": PATH_STREAM_SAMPLE,
        "path_test_set": PATH_TEST_SET
    },
    dag=dag
)

# Create task to fit the model using data
task2 = PythonOperator(
    task_id='fit_model',
    python_callable=fit_model,
    op_kwargs={
        'batch_size': BATCH_SIZE,
        'epochs': EPOCHS,
        'num_classes': NUM_CLASSES,
        'initial_model_path': INITIAL_MODEL_PATH
    },
    dag=dag
)

task1 >> task2
