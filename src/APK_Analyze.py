import os
import re
from androguard.misc import AnalyzeAPK
# from androguard.core.bytecode import apk
import json
import shutil
import xml.etree.ElementTree as ET
import os

class Analyze:
    def __init__(self,tools='tools'):
        self.tools=tools #apktools和jadx的文件夹

    def analyze(self, apkname,apkdir,result_path):
        basic_info=self.get_basic_info(apkname,apkdir)
        result={}
        result.update(basic_info)
        return result
    
    def get_basic_info(self, apkname,apkdir,result_path):
        
        # '''
        # apkname:apk文件名
        # apkdir:apk文件所在的文件夹
        # 获取apk的基本信息
        # 返回dict
        # '''
        try:
            apk_path=os.path.join(apkdir,apkname)
            a, d, dx = AnalyzeAPK(apk_path)
            try:
                # 提取权限
                permissions = a.get_permissions()
                # 提取活动
                activities = a.get_activities()
                # 提取服务
                services = a.get_services()
                # 提取接收器
                receivers = a.get_receivers()
                # 提取提供者
                providers = a.get_providers()
                # 判断 APK 是否有效
                valid = a.is_valid_APK()
                # 获取 APK 文件名，只保留文件名称部分
                filename = os.path.basename(a.get_filename())
                # 获取 APP 名
                appname = a.get_app_name()
                # 获取 package 名
                package = a.get_package()
                # 获取 android 版本名
                version = a.get_androidversion_code()
                # 获取 APK 文件列表
                # filelist = a.get_files()
                
                icon=a.get_app_icon()
            except:
                from test2 import analy
                apk_path=os.path.join(apkdir,apkname)
                return analy(result_path,apk_path)
        except:
            from test2 import analy
            apk_path=os.path.join(apkdir,apkname)
            return analy(result_path,apk_path)

 
        features = {
            "File": filename,
            "Permissions": permissions,
            "Activities": activities,
            "Services": services,
            "Receivers": receivers,
            "Providers": providers,
            "Valid": valid,
            "Filename": filename,
            "Appname": appname,
            "Package": package,
            "Version": version,
            "icon":icon,
        }
 
        return features
    
    def decompile(self,apkmame,result_path,apkdir):
        '''
        result_path:反编译后文件存放的文件夹
        反编译apk
        '''
        
        current_path = os.getcwd()
        # try:
        #     delete_files_in_folder(result_path+'/dissectJadx')
        #     os.mkdir(result_path)
        os.mkdir(result_path+'/dissectJadx')
        os.mkdir(result_path+'/dissectApktool')
        # except Exception as e:
        #     print(e)
        
        os.system(current_path+'\\'+self.tools+'\\jadx-1.3.1\\bin\\'+'jadx.bat -d '+result_path+'\\dissectJadx '+apkdir+'\\'+apkmame+' --deobf-rewrite-cfg')
        os.system('cd '+current_path)
        os.system('java -jar '+current_path+'/'+self.tools+'/apktool.jar d '+apkdir+'/'+apkmame+' -o '+result_path+'/dissectApktool/ -f')

    def extract_endpoints(self,decompiled_folder):
        '''
        获取apk中所有的url、ip和域名
        '''
        current_path = os.getcwd()
        print("[+] Beginning Endpoint Extraction...")
        print("[~] Extracting URLs...")
        print("[~] Extracting IPs...")
        url_matches = []
        ip_matches = []
        domain_matches = []

        for root, dirs, files in os.walk(decompiled_folder):
            for file in files:
                if  file.endswith(".java") or file.endswith(".smali") or file.endswith(".xml"): # 
                    file_path = os.path.join(root, file)
                    # print(file_path)
                    with open(file_path, 'r', encoding='utf-8',errors='ignore') as f:
                        # print('analyzeing'+file_path)
                        content = f.read()
                        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', content)
                        domains = re.findall(r'www\.[a-zA-Z0-9]{1,}\.[a-zA-Z0-9]{1,}', content)
                        ips = re.findall(r'\b(?:(?:2[0-4]\d|25[0-5]|1\d\d|[1-9]?\d)\.){3}(?:2[0-4]\d|25[0-5]|1\d\d|[1-9]?\d)\b', content)
                        for url in urls:
                            url_matches.append(url)
                        for ip in ips:
                            ip_matches.append(ip)
                        for domain in domains:
                            domain_matches.append(domain)

        url_matches = list(set(url_matches))  # 将urls转换为列表并去重
        ip_matches = list(set(ip_matches)) # 将ips转换为列表并去重
        domain_matches = list(set(domain_matches))

        
        result = {"urls": url_matches, "ips": ip_matches, "domains": domain_matches}
        return result

# if __name__ == '__main__':
    # a = Analyze()
    # a.get_basic_info('86-yl.cll.im.nenif.apk','apks')