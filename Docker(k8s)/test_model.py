import numpy as np
import joblib
from sklearn.metrics import mean_squared_error

def test_model():
    x_test_data = np.load('/mnt/nfs_share/default-nfs-pvc-pvc-504ae414-e42f-4ac6-b8fc-cc51cadf8ccc/x_test.npy')
    y_test_data = np.load('/mnt/nfs_share/default-nfs-pvc-pvc-504ae414-e42f-4ac6-b8fc-cc51cadf8ccc/y_test.npy')

    model = joblib.load('/mnt/nfs_share/default-nfs-pvc-pvc-504ae414-e42f-4ac6-b8fc-cc51cadf8ccc/model.pkl')
    y_pred = model.predict(x_test_data)

    err = mean_squared_error(y_test_data, y_pred)

    with open('/mnt/nfs_share/default-nfs-pvc-pvc-504ae414-e42f-4ac6-b8fc-cc51cadf8ccc/output.txt', 'a') as f:
        f.write(str(err))
    
    print(y_pred)

if __name__ == "__main__":
    test_model()
