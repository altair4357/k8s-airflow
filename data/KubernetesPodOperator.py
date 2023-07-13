# 2023.07.13 1000

from datetime import datetime
from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator

with DAG('KubernetesPodOperator',
         description='A simple ml workflow',
         schedule_interval=None,
         start_date=datetime(2023, 7, 13), catchup=False) as dag:
    
    preprocess_data_task = KubernetesPodOperator(
        task_id='preprocess_data',
        name='preprocess_data',
        cmds=['python', '/usr/src/app/preprocess_data.py'],
        namespace='default',
        image='altair4357/custom-airflow:0.3')

    train_model_task = KubernetesPodOperator(
        task_id='train_model',
        name='train_model',
        cmds=['python', '/usr/src/app/train_model.py'],
        namespace='default',
        image='altair4357/custom-airflow:0.3')

    deploy_model_task = KubernetesPodOperator(
        task_id='deploy_model',
        name='deploy_model',
        cmds=['python', '/usr/src/app/deploy_model.py'],
        namespace='default',
        image='altair4357/custom-airflow:0.3')

    test_model_task = KubernetesPodOperator(
        task_id='test_model',
        name='test_model',
        cmds=['python', '/usr/src/app/test_model.py'],
        namespace='default',
        image='altair4357/custom-airflow:0.3')

    # Define task dependencies
    preprocess_data_task >> train_model_task >> deploy_model_task >> test_model_task
