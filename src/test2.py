import os
import re
from xml.etree.ElementTree import parse
from androguard.misc import AnalyzeAPK

def get_permissions(manifest_path):
    permissions = []
    tree = parse(manifest_path)
    root = tree.getroot()
    for permission in root.findall('.//uses-permission'):
        permissions.append(permission.get('{http://schemas.android.com/apk/res/android}name'))
        # print(permission.get('android:name'))
    return permissions

def get_activities(manifest_path):
    activities = []
    tree = parse(manifest_path)
    root = tree.getroot()
    for activity in root.findall('.//activity'):
        activities.append(activity.get('{http://schemas.android.com/apk/res/android}name'))
    return activities

def get_services(manifest_path):
    services = []
    tree = parse(manifest_path)
    root = tree.getroot()
    for service in root.findall('.//service'):
        services.append(service.get('{http://schemas.android.com/apk/res/android}name'))
    return services

def get_receivers(manifest_path):
    receivers = []
    tree = parse(manifest_path)
    root = tree.getroot()
    for receiver in root.findall('.//receiver'):
        receivers.append(receiver.get('{http://schemas.android.com/apk/res/android}name'))
    return receivers

def get_providers(manifest_path):
    providers = []
    tree = parse(manifest_path)
    root = tree.getroot()
    for provider in root.findall('.//provider'):
        providers.append(provider.get('{http://schemas.android.com/apk/res/android}name'))
    return providers

def get_valid(manifest_path):
    valid = []
    tree = parse(manifest_path)
    root = tree.getroot()
    for meta_data in root.findall('.//meta-data'):
        if meta_data.get('{http://schemas.android.com/apk/res/android}name') == 'com.google.android.gms.version':
            valid.append(meta_data.get('{http://schemas.android.com/apk/res/android}value'))
    return valid

def get_filename(manifest_path):
    filename = os.path.basename(manifest_path)
    return filename

def get_appname(manifest_path, apk_path):
    app_name = ''
    # try:
    #     a, d, dx = AnalyzeAPK(apk_path)
    #     try:
    #         app_name = a.get_app_name()
    #         return app_name
    #     except:
    #         print("get_app_name error")
    # except:
    #     print("get_app_name error")
    tree = parse(manifest_path)
    root = tree.getroot()
    for application in root.findall('.//application'):
        app_name = application.get('{http://schemas.android.com/apk/res/android}label')
    return app_name

def get_package(manifest_path):
    package = ''
    tree = parse(manifest_path)
    root = tree.getroot()
    for package_name in root.findall('.//package'):
        package = package_name.text
    return package

def get_icon(manifest_path):
    icon = ''
    tree = parse(manifest_path)
    root = tree.getroot()
    for application in root.findall('.//application'):
        for icon_node in application.findall('.//icon'):
            icon = icon_node.get('{http://schemas.android.com/apk/res/android}src')
    return icon

def analy(result_path,apk_path):
    manifest_path = result_path+"\\dissectApktool\\AndroidManifest.xml"

    permissions = get_permissions(manifest_path)
    activities = get_activities(manifest_path)
    services = get_services(manifest_path)
    receivers = get_receivers(manifest_path)
    providers = get_providers(manifest_path)
    valid = get_valid(manifest_path)
    filename = get_filename(manifest_path)
    appname = get_appname(manifest_path, apk_path)
    package = get_package(manifest_path)
    #  = get_icon(manifest_path)

    
    print("Permissions: ", permissions)
    print("Activities: ", activities)
    print("Services: ", services)
    print("Receivers: ", receivers)
    print("Providers: ", providers)
    print("Valid: ", valid)
    print("Filename: ", filename)
    print("Appname: ", appname)
    print("Package: ", package)
    # print("Icon: ", icon)
    feat={
        'Permissions':permissions,
        'Activities':activities,
        'Services':services,
        'Receivers':receivers,
        'Providers':providers,
        'Valid':valid,
        'Filename':filename,
        'Appname':appname,
        'Package':package,
        # 'Icon':icon
    }
    return feat

if __name__ == '__main__':
    analy