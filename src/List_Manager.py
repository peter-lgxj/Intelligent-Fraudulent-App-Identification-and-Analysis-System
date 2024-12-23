import os
import pandas as pd

class Manager:
    def __init__(self):
        pass
    
    def save_list(self,list, type):
        if type == "white":
            filepath = "./list/white.csv"
        elif type == "black":
            filepath = "./list/black.csv"
            
        orign=pd.read_csv(filepath)
        o_list=orign['name'].to_list()
        for name in list:
            o_list.append(name)
        o_list = [x for x in o_list if x!=""]
        # o_list = list(set(o_list))
        # print(o_list)
        df = pd.DataFrame(o_list, columns=['name'])
        df.to_csv(filepath, index=False)

    def extract_list(self,path):
        csv=pd.read_excel(path)
        # print(csv)
        list=csv['apkName'].to_list()
        return list

    def set_list(self,):
        l=self.extract_list('./sex.xlsx')
        self.save_list(l, "black")
        l=self.extract_list('./scam.xlsx')
        self.save_list(l, "black")
        l=self.extract_list('./gamble.xlsx')
        self.save_list(l, "black")
        l=self.extract_list('./black.xlsx')
        self.save_list(l, "black")
        l=self.extract_list('./white.xlsx')
        self.save_list(l, "white")
        l=self.extract_list('./zj_white.xlsx')
        self.save_list(l, "white")

    def search_list(self,name, type):
        if type == "white":
            filepath = "./list/white.csv"
        elif type == "black":
            filepath = "./list/black.csv"
        orign=pd.read_csv(filepath)
        o_list=orign['name'].to_list()
        if name in o_list:
            return True
        else:
            return False

    def add_list(self,name, type):
        self.save_list([name], type)

    def del_list(self,name, type):
        if type == "white":
            filepath = "./list/white.csv"
        elif type == "black":
            filepath = "./list/black.csv"
        orign=pd.read_csv(filepath)
        o_list=orign['name'].to_list()
        o_list.remove(name)
        # print(name in o_list)
        df = pd.DataFrame(o_list, columns=['name'])
        df.to_csv(filepath, index=False)
        
    def show_list(self,type):
        if type == "white":
            filepath = "./list/white.csv"
        elif type == "black":
            filepath = "./list/black.csv"
        orign=pd.read_csv(filepath)
        o_list=orign['name'].to_list()
        return o_list

