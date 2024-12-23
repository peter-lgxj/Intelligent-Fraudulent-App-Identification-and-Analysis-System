import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd


def load_json_files(folder):
    folder=os.path.join('extract_data',folder)
    data = []
    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        with open(file_path, 'r') as f:
            content = json.load(f)
            # print(content)
            data.append(content)
    return data


def distill_features(data):
    namelist=['Permissions']#,'Activities','Services','Receivers','Providers'
    res=pd.DataFrame()
    for name in namelist:
        res[name]=data[name]
    return res


# 现在你有了四个字典列表，可以继续进行后续处理
def feat2data1():
    
    # black_data = load_json_files('black_json')
    sex_data = load_json_files('4_json')
    scam_data = load_json_files('3_json')
    gamble_data = load_json_files('2_json')
    black_data = load_json_files('1_json')
    white_data = load_json_files('0_json')
    # apks_data = load_json_files('apks_json')
    combined_df= pd.DataFrame()
    for s in sex_data:
        s=pd.json_normalize(s)
        s= distill_features(s)
        s['FEAT_LABEL']='red'
        combined_df = pd.concat([combined_df,s], ignore_index=True)
    for g in gamble_data:
        g=pd.json_normalize(g)
        g= distill_features(g)
        g['FEAT_LABEL']='red'
        combined_df = pd.concat([combined_df,g], ignore_index=True)
    for sc in scam_data:
        sc=pd.json_normalize(sc)
        sc= distill_features(sc)
        sc['FEAT_LABEL']='red'
        combined_df = pd.concat([combined_df,sc], ignore_index=True)
        
    for bk in black_data:
        bk=pd.json_normalize(bk)
        bk= distill_features(bk)
        bk['FEAT_LABEL']='orange'
        combined_df = pd.concat([combined_df,bk], ignore_index=True)
    for wh in white_data:
        wh=pd.json_normalize(wh)
        wh= distill_features(wh)
        wh['FEAT_LABEL']='yellow'
        combined_df = pd.concat([combined_df,wh], ignore_index=True)
    # for apk in apks_data:
    #     apk=pd.json_normalize(apk)
    #     apk= distill_features(apk)
    #     apk['FEAT_LABEL']='apk'
    #     combined_df = pd.concat([combined_df,apk], ignore_index=True)
        
    # combined_df = pd.concat([combined_df,glist], ignore_index=True)
    combined_df.to_csv('apk_feat_dataset/dataset_roy.csv', index=False)
    # print(sex_df.head())
    print("feature to data done!")
    
def feat2data2():
    
    # black_data = load_json_files('black_json')
    sex_data = load_json_files('4_json')
    scam_data = load_json_files('3_json')
    gamble_data = load_json_files('2_json')
    # black_data = load_json_files('1_json')
    # white_data = load_json_files('0_json')
    # apks_data = load_json_files('apks_json')
    combined_df= pd.DataFrame()
    
    for s in sex_data:
        s=pd.json_normalize(s)
        s= distill_features(s)
        s['FEAT_LABEL']='sex'
        combined_df = pd.concat([combined_df,s], ignore_index=True)
    for g in gamble_data:
        g=pd.json_normalize(g)
        g= distill_features(g)
        g['FEAT_LABEL']='gamble'
        combined_df = pd.concat([combined_df,g], ignore_index=True)
    for sc in scam_data:
        sc=pd.json_normalize(sc)
        sc= distill_features(sc)
        sc['FEAT_LABEL']='scam'
        combined_df = pd.concat([combined_df,sc], ignore_index=True)
    # for apk in apks_data:
    #     apk=pd.json_normalize(apk)
    #     apk= distill_features(apk)
    #     apk['FEAT_LABEL']='apk'
    #     combined_df = pd.concat([combined_df,apk], ignore_index=True)
    # combined_df = pd.concat([combined_df,glist], ignore_index=True)
    combined_df.to_csv('apk_feat_dataset/dataset_scg.csv', index=False)
    # print(sex_df.head())
    print("feature to data done!")
    
if __name__ == "__main__":
    feat2data1()
    feat2data2()