# KafkaPipelineTutorial
---------------------------
I haven't had a chance to play with Kafka professionally. Time to change that. Following the tutorial here, to create Kafka Events that drive an Airflow DAG for keeping ML Models up to date: https://www.vantage-ai.com/en/blog/keeping-your-ml-model-in-shape-with-kafka-airflow-and-mlflow

The main technologies used here are:
1. Docker Compose (to manage containers for Airflow, Kafka, MLFlow, PostgreSQL and Zookeeper)
2. Airflow DAGs (to handle interacting with the AI Model)
3. Apache Kafka to emulate new data coming into the DAG for training/testing
4. MLFlow for continued monitoring and integration of the model
