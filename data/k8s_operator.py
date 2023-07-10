from datetime import timedelta, datetime
from airflow import DAG
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'ml_pipeline',
    default_args=default_args,
    description='A simple ML pipeline',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 7, 5),
)

volume_config = {
    'name': 'data-volume',
    'persistentVolumeClaim': {
        'claimName': 'airflow-pvc'
    },
}

volume_mount = {
    'mountPath': '/home/env/airflow/dags_pvc',
    'name': 'data-volume',
}

tasks = ["preprocess_data", "train_model", "test_model", "deploy_model"]

for i, task in enumerate(tasks):
    task = KubernetesPodOperator(
        namespace='default',
        image="python:3.8",
        cmds=["python3"],
        arguments=[f"/home/env/airflow/dags_pvc/{task}.py"],
        name=task,
        task_id=task,
        volumes=[volume_config],
        volume_mounts=[volume_mount],
        is_delete_operator_pod=True,
        in_cluster=True,
        config_file='/path/to/kubeconfig',
        dag=dag,
    )

    if i != 0:
        tasks[i-1] >> task
