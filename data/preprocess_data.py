from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
import numpy as np

def preprocess_data():
    housing = fetch_california_housing()
    X, y = housing.data, housing.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)
    np.save('/mnt/nfs_share/default-nfs-pvc-pvc-504ae414-e42f-4ac6-b8fc-cc51cadf8ccc/x_train.npy', X_train)
    np.save('/mnt/nfs_share/default-nfs-pvc-pvc-504ae414-e42f-4ac6-b8fc-cc51cadf8ccc/x_test.npy', X_test)
    np.save('/mnt/nfs_share/default-nfs-pvc-pvc-504ae414-e42f-4ac6-b8fc-cc51cadf8ccc/y_train.npy', y_train)
    np.save('/mnt/nfs_share/default-nfs-pvc-pvc-504ae414-e42f-4ac6-b8fc-cc51cadf8ccc/y_test.npy', y_test)

if __name__ == "__main__":
    preprocess_data()
