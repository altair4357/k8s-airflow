from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from sklearn import datasets
from sklearn.model_selection import train_test_split
import numpy as np
import joblib
from sklearn.linear_model import SGDRegressor
from sklearn.metrics import mean_squared_error


from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDRegressor
from sklearn.metrics import mean_squared_error
import joblib
import numpy as np

def preprocess_data(**kwargs):
    X, y = datasets.load_boston(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)

    kwargs['ti'].xcom_push(key='X_train', value=X_train)
    kwargs['ti'].xcom_push(key='X_test', value=X_test)
    kwargs['ti'].xcom_push(key='y_train', value=y_train)
    kwargs['ti'].xcom_push(key='y_test', value=y_test)

def train_model(**kwargs):
    ti = kwargs['ti']

    X_train = ti.xcom_pull(key='X_train')
    y_train = ti.xcom_pull(key='y_train')

    model = SGDRegressor(verbose=1)
    model.fit(X_train, y_train)

    kwargs['ti'].xcom_push(key='model', value=model)

def test_model(**kwargs):
    ti = kwargs['ti']

    X_test = ti.xcom_pull(key='X_test')
    y_test = ti.xcom_pull(key='y_test')
    model = ti.xcom_pull(key='model')

    y_pred = model.predict(X_test)
    err = mean_squared_error(y_test, y_pred)

    with open('output.txt', 'a') as f:
        f.write(str(err))

def deploy_model():
    print('deploying model...')


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

t1 = PythonOperator(
    task_id='preprocess_data',
    python_callable=preprocess_data,
    provide_context=True,
    dag=dag,
)

t2 = PythonOperator(
    task_id='train_model',
    python_callable=train_model,
    provide_context=True,
    dag=dag,
)

t3 = PythonOperator(
    task_id='test_model',
    python_callable=test_model,
    provide_context=True,
    dag=dag,
)

t4 = PythonOperator(
    task_id='deploy_model',
    python_callable=deploy_model,
    dag=dag,
)
t1 >> t2 >> t3 >> t4
