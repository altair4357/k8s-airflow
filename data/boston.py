# 2023.07.11 13:00

from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDRegressor
from sklearn.metrics import mean_squared_error
import numpy as np
import joblib

def preprocess_data():
    X, y = datasets.load_boston(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)
    np.save('/mnt/nfs_share/x_train.npy', X_train)
    np.save('/mnt/nfs_share/x_test.npy', X_test)
    np.save('/mnt/nfs_share/y_train.npy', y_train)
    np.save('/mnt/nfs_share/y_test.npy', y_test)

def train_model():
    x_train_data = np.load('/mnt/nfs_share/x_train.npy')
    y_train_data = np.load('/mnt/nfs_share/y_train.npy')
    model = SGDRegressor(verbose=1)
    model.fit(x_train_data, y_train_data)
    joblib.dump(model, '/mnt/nfs_share/model.pkl')

def deploy_model():
    print('deploying model...')

def test_model():
    x_test_data = np.load('/mnt/nfs_share/x_test.npy')
    y_test_data = np.load('/mnt/nfs_share/y_test.npy')
    model = joblib.load('/mnt/nfs_share/model.pkl')
    y_pred = model.predict(x_test_data)
    err = mean_squared_error(y_test_data, y_pred)
    with open('/mnt/nfs_share/output.txt', 'a') as f:
        f.write(str(err))

# Using a DAG context manager, you don't have to specify the dag property of each task
with DAG('machine_learning_workflow',
         description='A simple ml workflow',
         schedule_interval='0 12 * * *',
         start_date=datetime(2023, 7, 11), catchup=False) as dag:
    
    preprocess_data_task = PythonOperator(
        task_id='preprocess_data',
        python_callable=preprocess_data)

    train_model_task = PythonOperator(
        task_id='train_model',
        python_callable=train_model)

    deploy_model_task = PythonOperator(
        task_id='deploy_model',
        python_callable=deploy_model)

    test_model_task = PythonOperator(
        task_id='test_model',
        python_callable=test_model)

    # Define task dependencies
    preprocess_data_task >> train_model_task >> deploy_model_task >> test_model_task
