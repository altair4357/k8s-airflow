import numpy as np
import joblib
from sklearn.linear_model import SGDRegressor

def train_model():
    x_train_data = np.load('/mnt/nfs_share/default-nfs-pvc-pvc-504ae414-e42f-4ac6-b8fc-cc51cadf8ccc/x_train.npy')
    y_train_data = np.load('/mnt/nfs_share/default-nfs-pvc-pvc-504ae414-e42f-4ac6-b8fc-cc51cadf8ccc/y_train.npy')

    model = SGDRegressor(verbose=1)
    model.fit(x_train_data, y_train_data)

    joblib.dump(model, '/mnt/nfs_share/default-nfs-pvc-pvc-504ae414-e42f-4ac6-b8fc-cc51cadf8ccc/model.pkl')

if __name__ == "__main__":
    train_model()
