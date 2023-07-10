from datetime import timedelta, datetime
from airflow import DAG
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from kubernetes.client import V1VolumeMount, V1PersistentVolumeClaimVolumeSource, V1Volume

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'k8s_operator',
    default_args=default_args,
    description='A simple ML pipeline',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 7, 5),
)

volume_mount = V1VolumeMount(
    mount_path='/home/env/airflow/dags_pvc',
    name='data-volume',
)

volume_config = V1Volume(
    name='data-volume',
    persistent_volume_claim=V1PersistentVolumeClaimVolumeSource(claim_name='airflow-pvc')
)

task_names = ["preprocess_data", "train_model", "test_model", "deploy_model"]
tasks = []

for i, task_name in enumerate(task_names):
    task = KubernetesPodOperator(
        namespace='default',
        image="python:3.8",
        cmds=["python3"],
        arguments=[f"/home/env/airflow/dags_pvc/{task_name}.py"],
        name=task_name,
        task_id=task_name,
        volumes=[volume_config],
        volume_mounts=[volume_mount],
        is_delete_operator_pod=True,
        in_cluster=True,
        config_file='/path/to/kubeconfig',
        dag=dag,
    )
    
    tasks.append(task)
    
    if i != 0:
        tasks[i-1] >> task
