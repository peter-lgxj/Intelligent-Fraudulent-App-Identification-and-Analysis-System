import os
import zipfile

def extract_assets(apk_dir,apkname, output_dir):
    apk_path=os.path.join(apk_dir,apkname)
    with zipfile.ZipFile(apk_path, 'r') as apk_zip:
        # 找到assets文件夹并解压
        for file_info in apk_zip.infolist():
            if file_info.is_dir() and file_info.filename.startswith('assets/'):
                file_path = file_info.filename[len('assets/'):]
                dir_path = os.path.join(output_dir, file_path)
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
            elif file_info.filename.startswith('assets/'):
                file_path = file_info.filename[len('assets/'):]
                file_path= file_path.replace("/", "_")
                # if file_path.lower() in ['.jpg', '.png','.mp4', '.gif', '.jpeg']:
                file_extension = os.path.splitext(file_path)[1]
                if file_extension.lower() in ['.jpg', '.png','.mp4', '.gif', '.jpeg']:
                    output_path = os.path.join(output_dir, file_path)
                    with open(output_path, 'wb') as f:
                        f.write(apk_zip.read(file_info))
def remove_extra_images(folder):

    # 定义目标文件夹
    # folder = '/path/to/folder'

    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder):
        # 获取文件路径
        filepath = os.path.join(folder, filename)
        
        # 检查文件大小是否小于10kb（10240字节）
        if os.path.getsize(filepath) < 10240:
            os.remove(filepath)


# apk_dir = 'apks'
# output_dir = 'img'
# apkname='5f9028a4aff659a277ad1d002b3f7f6c.apk'
# extract_assets(apk_dir,apkname, output_dir)
