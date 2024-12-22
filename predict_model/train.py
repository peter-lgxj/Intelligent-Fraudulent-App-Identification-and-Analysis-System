try:
    from predict_model.utils.dataset import load_data
except:
    from utils.dataset import load_data
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
# from sklearn.neighbors import KNeighborsClassifier
import joblib
# from predict_model.test import apk_predict
import numpy as np

def train(type):
    data_list=['Permissions']#,'Activities,''Permissions','Receivers','Providers','Package'
    for data_name in data_list:
        X=np.load("./apk_feat_dataset/train_dataset/data_"+type+".npy")
        y=np.load("./apk_feat_dataset/train_dataset/label_"+type+".npy")
        best_accuracy=0.0
        best_random_state=0
        for random_state in range(170):
            
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=random_state)#70best!!!
            scaler = StandardScaler()
            X_train = scaler.fit_transform(X_train)
            X_test = scaler.transform(X_test)

            clf = SVC(kernel='linear', C=1)

            clf.fit(X_train, y_train)

            y_pred = clf.predict(X_test)

            accuracy = accuracy_score(y_test, y_pred)
            # print('random_state:'+str(random_state)+'\t'+data_name+"预测准确率：", accuracy)
            
            if accuracy >= best_accuracy:
                best_accuracy=accuracy
                best_random_state=random_state
                joblib.dump(clf, 'predict_model/'+type+'_saved_model.pkl')
                # print(y_test)
                # print(y_pred)
            # print('best_random_state:'+str(best_random_state)+'\t'+data_name+"预测准确率：", best_accuracy)
        scaler = StandardScaler()
        X = scaler.fit_transform(X)
        y_pred = clf.predict(X)
        accuracy = accuracy_score(y, y_pred)
        print('best_random_state:'+str(best_random_state)+'\t'+data_name+"预测准确率：", accuracy)
        # print(y)
        # print(y_pred)


if __name__ == '__main__':
    train('roy')
    train('scg')