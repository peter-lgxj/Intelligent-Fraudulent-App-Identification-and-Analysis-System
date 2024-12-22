from .APK_Analyze import Analyze
from .APK_Downloader import Downloader
from .RES_Analyze import RES_Analyze
from .List_Manager import Manager
from .HTML_Producer import *
import json
import requests
import time
import os
import shutil


class Domain:
    server_url = 'http://10.100.195.138:8912'
    def __init__(self):
        self.apk_analyzer= Analyze()
        self.apk_downloader = Downloader()
        self.res_analyzer = RES_Analyze()
        self.list_manager = Manager()
        self.apkdir='./apks'
        self.apkname= ''
        self.result_path='./out'
        self.jsonname=''
        self.jsonpath=''
        self.state=''
        self.basic_info={}
        self.uid={}
        self.backstage=[]
        self.type=''
        self.level='white'
        self.permission_infos=[]
        self.html_obj=None
    
    def set_server_url(self, url):
        self.server_url = url+':8912'

    def clear_folder(self,folder_path):
        # 检查文件夹是否存在
        if not os.path.exists(folder_path):
            print(f"Folder {folder_path} does not exist.")
            return

        # 检查文件夹是否为空
        if os.listdir(folder_path):
            print(f"Folder {folder_path} is not empty. Clearing contents...")
            
            # 删除文件夹中的所有文件和子文件夹
            shutil.rmtree(folder_path)
            print(f"Deleted folder {folder_path} and its contents.")
            os.mkdir(folder_path)
        else:
            print(f"Folder {folder_path} is empty.")
        
        return

    def get_from_direct(self, apk_path):
        apkname,bool,apkdir=self.apk_downloader.get_apk(apk_path)
        self.apkname=apkname
        self.apkdir=apkdir
        return bool

    def get_from_url(self, url):
        apkname,bool=self.apk_downloader.download_apk(url)
        self.apkname=apkname
        return bool

    def get_from_qrcode(self, img_path):
        apkname,bool=self.apk_downloader.decode_qrcode(img_path)
        self.apkname=apkname
        return bool
    
    def get_basic_info(self):
        feature=self.apk_analyzer.get_basic_info(self.apkname,self.apkdir,self.result_path)
        jsonname = 'target.json'
        print(jsonname)
        self.jsonname=jsonname
        jsonpath = './extract_data/'+'apks_json'
        self.jsonpath=jsonpath
        self.clear_folder(jsonpath)
        filepath = './extract_data/'+'apks_json'+'/'+jsonname
        print(filepath)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(feature, f, indent=4)
        self.basic_info= feature
        return feature
    
    def set_result_path(self,result_path):
        self.result_path=result_path
    
    def get_src(self):
        self.clear_folder(self.result_path)
        self.apk_analyzer.decompile(self.apkname,self.result_path,self.apkdir)

    def get_uid(self,result_path):
        uid=self.apk_analyzer.extract_endpoints(result_path)
        self.uid=uid
        return uid
    
    def search_list(self,name,type):
        return self.list_manager.search_list(name,type)
    
    def permission_analysis(self):
        jsonname=self.jsonname
        jsonpath=self.jsonpath
        list,state=self.res_analyzer.get_permission_des(jsonname,jsonpath)
        self.permission_infos=list
        self.state=state
        if state=='危险':
            self.level='black'
        return list
    
    def get_judge_res(self,type):
        t=self.res_analyzer.get_judge_result(type,self.basic_info["Permissions"])
        if t in ['sex','scam','gamble']:
            self.type=t
        if t in ['black','grey','white']:
            self.level=t
        return t
    
    def config_list(self, name, type,fuc):
        if fuc=='add':
            self.list_manager.add_list(name,type)
        elif fuc=='del':
            self.list_manager.del_list(name,type)
            
    def set_jsonpath(self,jsonpath):
        self.jsonpath=jsonpath
    
    def set_jsonname(self,jsonname):
        self.jsonname=jsonname
    
    def set_resultpath(self,result_path):
        self.result_path=result_path
    
    def ping_url(self,url, timeout=3):
        # start_time = time.time()
        # try:
        #     response = requests.get(url, timeout=timeout)
        #     response_time = time.time() - start_time
        #     if response.status_code == 200:
        #         print(f"{url} responded in {response_time} seconds")
        #         return True
        #     else:
        #         print(f"{url} returned an error status code: {response.status_code}")
        #         return False
        # except requests.Timeout:
        #     print(f"{url} timed out")
        #     return False
        # except Exception as e:
        #     print(f"An error occurred: {e}")
        #     return False
        import subprocess
        try:
            # subprocess.Popen(['start', 'cmd', '/c', f'ping -n 1 {url}'], shell=True)
            # 使用subprocess.run执行ping命令，并获取结果
            result = subprocess.run(['ping', '-n', '1', '-w' ,'200',url], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # 检查结果是否包含"1 packets transmitted, 1 received"
            if "已接收 = 1" in result.stdout:
                print(f"{url} is reachable")
                return True
            else:
                print(f"{url} is not reachable")
                return False
        except Exception as e:
            print(f"Error pinging {url}: {e}")
            return False
        
    # def upload_file(self):
    #     apk_path=self.apkdir+'/'+self.apkname
    #     url = self.server_url+'/upload_apk'

    #     # 读取APK文件内容
    #     with open(apk_path, 'rb') as file:
    #         files = {'file': ('file.apk', file)}

    #         # 发送POST请求
    #         response = requests.post(url, files=files)

    #         # 打印响应内容
    #         print(response.text)
    #     return [response.json()['message']]
    
    # def server_analyze(self):
    #     url = self.server_url+'/analyze/'
    #     response = requests.get(url)
    #     print(response.text)
    #     return [response.json()['message']]
    
    # def get_domain(self):
    #     url = self.server_url+'/get_domains/'
    #     response = requests.get(url)
    #     print(response.text)
    #     for u in response.json()['domains']:
    #         self.backstage.append(u)
    #     self.backstage = list(set(self.backstage))
    #     return [response.json()['domains']]
        
    def extract_domain(self,url):
        from urllib.parse import urlparse
        domain_name = urlparse(url).netloc
        return domain_name
    
    def fetch_pack_fake(self):
        
        for url in self.uid["urls"]:
            url = self.extract_domain(url)
            print(url)
            if self.ping_url(url,1):
                print("Ping successful")
                self.backstage.append(url)
            else:
                print("Ping failed")
                
        for url in self.uid["ips"]:
            print(url)
            url = url
            if self.ping_url(url,2):
                print("Ping successful")
                self.backstage.append(url)
            else:
                print("Ping failed")
        
        for url in self.uid["domains"]:
            url = url
            if self.ping_url(url,2):
                print("Ping successful")
                self.backstage.append(url)
            else:
                print("Ping failed")
        for url in self.backstage:
            print(url+'\n')
        self.backstage = list(set(self.backstage))
        return self.backstage
    
    def produce_out_file(self):
        self.html_obj=produce_html(self.basic_info,self.backstage,self.type,self.level,self.permission_infos,self.result_path,self.server_url)

    def set_basic_info(self,json_path):
        with open(json_path, 'r') as f:
            self.basic_info = json.load(f)

    def set_level(self,level):
        self.level=level
    
    def set_type(self,type):
        self.type=type
        
    def set_json_info(self,jsonname,jsonpath):
        self.jsonname=jsonname
        self.jsonpath=jsonpath

    def set_basic_info(self,json_path):
        with open(json_path, 'r') as f:
            self.basic_info = json.load(f)

# if __name__ == '__main__':
#     d=Domain()
#     d.get_from_direct("D:\Program\softbei\zongshe\DriverApp.apk.1")
#     print("successfully get from direct")
#     d.get_src()
#     print("successfully get src")
#     f=d.get_basic_info()
#     print("successfully get basic info")
#     # d.set_basic_info('extract_data\\apks_json\\target.json')
#     t=d.get_judge_res('scg')
#     print("successfully get judge res scg")
#     t=d.get_judge_res('roy')
#     print("successfully get judge res roy")
#     d.get_uid("out")
#     print("successfully get uid")
#     d.fetch_pack_fake()
#     print("successfully fetch pack fake")
#     d.produce_out_file()
#     print("successfully produce out file")