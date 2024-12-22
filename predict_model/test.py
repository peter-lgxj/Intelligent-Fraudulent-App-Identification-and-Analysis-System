from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
import joblib
import numpy as np
try:
    from predict_model.utils.dataset import load_predict_data,load_data,permissions_to_onehot,get_permissions
except:
    from utils.dataset import load_predict_data,load_data,permissions_to_onehot,get_permissions


def apk_predict(type,Permissions):
    Permissions=[l.split('.')[-1] for l in Permissions]
    vec=permissions_to_onehot(Permissions,type)
    vec=np.array(vec).reshape(1,-1)
    print('predicting...')
    loaded_model = joblib.load('predict_model/'+type+'_saved_model.pkl')
    y_pred = loaded_model.predict(vec)
    print("预测结果：", y_pred)
    return y_pred

if __name__ == '__main__':
    apk_predict('scg')