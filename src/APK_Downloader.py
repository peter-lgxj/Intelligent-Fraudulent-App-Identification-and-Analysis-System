import requests
from PIL import Image
import pyzbar.pyzbar as pyzbar
import os
import shutil
# import urllib.request

class Downloader:
    def __init__(self):
        pass
    
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

    def get_apk(self,filepath):
        filename = os.path.basename(filepath)
        
        target_folder = os.path.dirname(filepath)
        # # self.clear_folder(target_folder)
        # os.link(filepath, os.path.join(target_folder, filename))
        # os.system("clear")
        # print(f"APK已成功下载到{target_folder}")
        return filename,True, target_folder
    

    def download_apk(self,url, filename="./apks/target.apk"):
        '''
        url: APK下载链接
        filename: 保存的文件名
        '''
        # response = requests.get(url)
        headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0"}
        response = requests.get(url, headers=headers)    
        if response.status_code == 200:
            with open(filename, 'wb') as file:
                file.write(response.content)
            print(f"APK已成功下载到{filename}")
            return 'target.apk',True
        else:
            print("下载失败")
            return 'target.apk',False

    def decode_qrcode(self,image_path, filename="./apks/target.apk"):
        '''
        image_path: 二维码图片路径
        filename: 保存的文件名
        '''
        img = Image.open(image_path)
        # 因为一张图片可能是一张二维码，也可能里面有许多二维码
        barcodes = pyzbar.decode(img)
        for barcode in barcodes:
            barcodeData = barcode.data.decode("utf-8")
            print(barcodeData)
        return self.download_apk(barcodeData, filename)


