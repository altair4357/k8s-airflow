from datetime import datetime
from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.kubernetes.volume import Volume
from airflow.kubernetes.volume_mount import VolumeMount

volume_mount = VolumeMount('nfs-dags',
                           mount_path='/mnt/nfs_share/default-nfs-pvc-pvc-504ae414-e42f-4ac6-b8fc-cc51cadf8ccc',
                           sub_path=None,
                           read_only=False)

volume_config= {
    'persistentVolumeClaim':
      {
        'claimName': 'nfs-pvc'
      }
    }
volume = Volume(name='nfs-dags', configs=volume_config)

with DAG('KubernetesPodOperator',
         description='A simple ml workflow',
         schedule_interval=None,
         start_date=datetime(2023, 7, 11), catchup=False) as dag:
    
    preprocess_data_task = KubernetesPodOperator(
        task_id='preprocess_data',
        name='preprocess_data',
        cmds=['python', '/usr/src/app/preprocess_data.py'],
        namespace='default',
        image='altair4357/custom-airflow:0.5',
        volumes=[volume],
        volume_mounts=[volume_mount])

    train_model_task = KubernetesPodOperator(
        task_id='train_model',
        name='train_model',
        cmds=['python', '/usr/src/app/train_model.py'],
        namespace='default',
        image='altair4357/custom-airflow:0.5',
        volumes=[volume],
        volume_mounts=[volume_mount])

    test_model_task = KubernetesPodOperator(
        task_id='test_model',
        name='test_model',
        cmds=['python', '/usr/src/app/test_model.py'],
        namespace='default',
        image='altair4357/custom-airflow:0.5',
        volumes=[volume],
        volume_mounts=[volume_mount])

    # Define task dependencies
    preprocess_data_task >> train_model_task >> test_model_task
