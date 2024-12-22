import numpy as np
import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

def permissions_to_onehot(input_permissions,type):
    with open('predict_model/'+type+'_all_permissions.pkl', 'rb') as file:
        all_permissions = pickle.load(file)
    onehot = [0] * len(all_permissions)
    # 遍历输入的权限列表
    for perm in input_permissions:
        # 如果权限在所有权限的列表中，将对应的onehot位置设置为1
        if perm in all_permissions:
            index = all_permissions.index(perm)
            onehot[index] = 1
        else:
            print(f"Warning: '{perm}' is not a recognized permission.")
    
    return onehot

def get_permissions(lis):
    lis=eval(lis[0])
    x=[l.split('.')[-1] for l in lis]
    # vec=permissions_to_onehot(x)
    # print(sum(vec))
    return x
        
    
def text2float1():
    data_list=['Permissions']#,lable,'Package','Activities','Services','Receivers','Providers'

    xy = pd.read_csv('apk_feat_dataset/dataset_scg.csv')
    xy['FEAT_LABEL'] = xy['FEAT_LABEL'].replace(['sex', 'scam', 'gamble'], [0, 1, 2])
    xy = pd.DataFrame(xy)
    Y  = xy.iloc[:, -1]
    xs  = xy.iloc[:, :-1]

    for data_name in data_list:
        X=[]
        vecs=[]
        for x in xs.values:
            X.append(get_permissions(x))
        all_permissions= list(set([item for sublist in X for item in sublist]))
        with open('predict_model/'+'scg_all_permissions.pkl', 'wb') as file:
            pickle.dump(all_permissions, file)
        for x in X:
            vecs.append(permissions_to_onehot(x,'scg'))
        X= np.array(vecs)
        np.save('apk_feat_dataset/train_dataset/data_scg.npy',X)
        np.save('apk_feat_dataset/train_dataset/label_scg.npy',Y)
    
    print("already finished text2float function")


def text2float2():
    data_list=['Permissions']#,lable,'Package','Activities','Services','Receivers','Providers'

    xy = pd.read_csv('apk_feat_dataset/dataset_roy.csv')
    xy['FEAT_LABEL'] = xy['FEAT_LABEL'].replace(['red', 'orange', 'yellow'], [0, 1, 2])
    xy = pd.DataFrame(xy)
    Y  = xy.iloc[:, -1]
    xs  = xy.iloc[:, :-1]

    for data_name in data_list:
        X=[]
        vecs=[]
        for x in xs.values:
            X.append(get_permissions(x))
        all_permissions= list(set([item for sublist in X for item in sublist]))
        with open('predict_model/'+'roy_all_permissions.pkl', 'wb') as file:
            pickle.dump(all_permissions, file)
        for x in X:
            vecs.append(permissions_to_onehot(x,'roy'))
        X= np.array(vecs)
        np.save('apk_feat_dataset/train_dataset/data_roy.npy',X)
        np.save('apk_feat_dataset/train_dataset/label_roy.npy',Y)

    
    print("already finished text2float function")


def text2float3():
    data_list=['Permissions']#,lable,'Package','Activities','Services','Receivers','Providers'
    
    xy = pd.read_csv('apk_feat_dataset/dataset_scg.csv')
    xy['FEAT_LABEL'] = xy['FEAT_LABEL'].replace(['sex', 'scam', 'gamble','apk'], [0, 1, 2, 3])
    xy = pd.DataFrame(xy)
    Y  = xy.iloc[:, -1]
    x  = xy.iloc[:, :-1]
    data_df= pd.DataFrame()
    for data_name in data_list:
        # print(data_name)
        vectorizer = TfidfVectorizer()
        X= vectorizer.fit_transform(x[data_name])
        X= X.toarray().sum(axis=1)
        # X_df = list(map(lambda x: [float(i) for i in x], X))
        # new_columns =[str(i) for i in vectorizer.get_feature_names_out()]
        data_df[data_name]=X
        # data_df = pd.concat([data_df, X], ignore_index=True)
    data_df['FEAT_LABEL']=Y
    data_df.to_csv('apk_feat_dataset/'+'scg.csv', index=False)
    
    
    xy = pd.read_csv('apk_feat_dataset/train_dataset/dataset_roy.csv')
    xy['FEAT_LABEL'] = xy['FEAT_LABEL'].replace(['red', 'orange', 'yellow','apk'], [0, 1, 2, 3])
    xy = pd.DataFrame(xy)
    Y  = xy.iloc[:, -1]
    x  = xy.iloc[:, :-1]
    data_df= pd.DataFrame()
    for data_name in data_list:
        # print(data_name)
        vectorizer = TfidfVectorizer()
        X= vectorizer.fit_transform(x[data_name])
        X= X.toarray().sum(axis=1)
        # X_df = list(map(lambda x: [float(i) for i in x], X))
        # new_columns =[str(i) for i in vectorizer.get_feature_names_out()]
        data_df[data_name]=X
        # data_df = pd.concat([data_df, X], ignore_index=True)
    data_df['FEAT_LABEL']=Y
    data_df.to_csv('apk_feat_dataset/train_dataset/'+'roy.csv', index=False)
    
    print("already finished text2float function")

def load_data(featpath='Permissions',kind='scg'):
    path=os.path.join('apk_feat_dataset/train_dataset/', featpath+'_'+kind+'.csv')
    print("loading data...")
    xy = pd.read_csv(path)
    # xy = pd.DataFrame(xy)
    xy = xy[(xy['FEAT_LABEL'] == 0) | (xy['FEAT_LABEL'] == 1) | (xy['FEAT_LABEL'] == 2)]
    x_data = np.array(xy.iloc[:, :-1]) 
    y_data = np.array(xy.iloc[:, -1])
    # print(x_data.shape, y_data.shape)
    # print(x_data[:1], y_data[:1])
    return x_data, y_data

def load_predict_data(featpath='Permissions',kind='scg'):
    path=os.path.join('apk_feat_dataset/train_dataset/', featpath+'_'+kind+'.csv')
    print("loading predict data...")
    xy = pd.read_csv(path)
    xy = xy.query('FEAT_LABEL == 3')
    x_data = np.array(xy.iloc[:, :-1]) 
    return x_data
    
def load_data2(kind='scg'):
    path=os.path.join('apk_feat_dataset/train_dataset/', kind+'.csv')
    print("loading data...")
    xy = pd.read_csv(path)
    # xy = pd.DataFrame(xy)
    xy = xy[(xy['FEAT_LABEL'] == 0) | (xy['FEAT_LABEL'] == 1) | (xy['FEAT_LABEL'] == 2)]
    x_data = np.array(xy.iloc[:, :-1]) 
    y_data = np.array(xy.iloc[:, -1])
    # print(x_data.shape, y_data.shape)
    # print(x_data[:1], y_data[:1])
    return x_data, y_data

def load_predict_data2(kind='scg'):
    path=os.path.join('apk_feat_dataset/train_dataset/', kind+'.csv')
    print("loading predict data...")
    xy = pd.read_csv(path)
    xy = xy.query('FEAT_LABEL == 3')
    x_data = np.array(xy.iloc[:, :-1]) 
    return x_data
    
if __name__ == '__main__':
    text2float1()
    text2float2()
    # load_data()
    # pass