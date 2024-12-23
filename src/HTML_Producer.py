def create_html(title, data ,ai_report,icon_path):
    stylesheet="stylesheet"
    styles="styles.css"
    html = f"<html><head><title>{title}</title><link rel={stylesheet} href={styles}><style> body {{text-align: center;}}</style></head><body>"
    # for key, value in data.items():
    #     html += f"<h2>{key}</h2><p>"
    #     if isinstance(value, list):
    #         for item in value:
    #             html += f"{item}<br>"
    #     else:
    #         html += f"{value}"
    #     html += "</p>"
    
    html += f"<img src={icon_path}>"
    
    for key, value in data.items():
        html += f"<div class='data-section'>"
        html += f"<h2 class='section-title'>{key}</h2>"
        html += f"<p class='section-content'>"
        if isinstance(value, list):
            for item in value:
                html += f"{item}<br>"
        else:
            html += f"{value}"
        html += "</p></div>"
        
    for key, value in ai_report.items():
    
        # html += f"<h2>{key}</h2><p>"
        report_with_breaks = value.replace('\n', '<br>')
        # html += f'{report_with_breaks}</p>'
        
        html += f"<div class='ai-report'>"
        html += f"<h2 class='section-title'>{key}</h2>"
        html += f"<p class='section-content'>"
        html += f'{report_with_breaks}</p></div>'

    html += "</body></html>"
    return html



def produce_html(basic_info,backstage,type,level,permission_infos,result_path,server_url):

    # 示例
    title = "APP:"+basic_info["Appname"]+"的分析结果报告"
    if level == "white":
        type== "安全"
    
    ai_input = "这是一个app的检测结果，请依据以下内容帮我写一篇分析报告："
    ai_input += f"APP名称是{basic_info['Appname']},"   
    ai_input += f"APP权限分析是{permission_infos},"
    ai_input += f"APP危险等级是{level},"
    ai_input += f"APP类型是{type},"
    ai_input += f"APP后台通联地址是{backstage}"
    
    # import requests
    # response = requests.get(server_url+'/get_ai_inputs?'+"input="+ai_input)
    # print(response)
    # report = response.json()["output"]
    print(ai_input)
    # from chat_model import chat_model
    # report = chat_model(ai_input)
    report="这里应该是ai生成的报告，但是现在ai试用到期了，所以暂时用这个占位"
    
    data = {
        "APP名称": basic_info["Appname"],
        "APP危险等级": level,
        "APP类型": type,
        "APP后台通联地址": backstage,
        "APP权限分析": permission_infos
    }
    ai_report={"综合分析报告": report}
    
    
    print(data)
    print(report)
    icon_path=result_path+"\\dissectApktool\\"+basic_info["icon"]
    html_obj = create_html(title, data ,ai_report,icon_path)

    # 将HTML对象保存为文件
    with open(result_path+"/output.html", "w", encoding="utf-8") as f:
        f.write(html_obj)
    return html_obj

# if __name__ == "__main__":
#     basic_info = {"Appname":"test"}
#     backstage = "http://test.com"
#     type = "危险"
#     level= "black"
#     permission_infos = [
#         "android.permission.QUERY_ALL_PACKAGES",
#         "android.permission.MANAGE_EXTERNAL_STORAGE",
#         "com.metanet.house.permission.KW_SDK_BROADCAST",
#         "android.permission.ACCESS_WIFI_STATE"
#         ]
#     produce_html(basic_info,backstage,type,level,permission_infos,"./","http://127.0.0.1:8912")
    
    # data = {
    #     "APP名称": basic_info["Appname"],
    #     "APP危险等级": level,
    #     "APP类型": type,
    #     "APP后台通联地址": backstage,
    #     "APP权限分析": permission_infos
    # }
    # report='**APP检测分析报告**\n\n**一、APP基本信息**\n- APP名称：test\n- APP权限请求：\n  - android.permission.QUERY_ALL_PACKAGES\n  - android.permission.MANAGE_EXTERNAL_STORAGE\n  - com.metanet.house.permission.KW_SDK_BROADCAST\n  - android.permission.ACCESS_WIFI_STATE\n- APP危险等级：black（黑色）\n- APP类型：危险\n- APP后台通联地址：http://test.com\n\n**二、权限分析**\n该APP申请了多个敏感权限，包括查询所有应用程序、管理外部存储、广播发送和访问WiFi状态等。这些权限可能 被用于非法目的，例如窃取用户数据、恶意软件安装或远程控制设备。\n\n**三、危险等级评估**\n根据所申请的权限和背景调查，我们评估该APP为危险等级。此类权限通常不会被正常 应用程序所需要，因此它们的申请可能存在可疑意图。\n\n**四、建议措施**\n为了保护您的设备和安全，我们建议您采取以下措施：\n1. 立即卸载该APP。\n2. 运行系统更新以修补任 何已知的安全漏洞。\n3. 定期扫描您的设备以检测任何潜在的恶意软件或活动。\n4. 谨慎下载和安装来自不可信来源的应用程序。\n5. 更改所有相关服务的密码，以防个人信息泄露。\n\n如果您有其他问题或需要进一步的帮助，请随时联系我们。'

    # ai_report={"综合分析报告": report}
    
    # html_obj=create_html("test",data,ai_report)
    
    # with open('.'+"/output.html", "w", encoding="utf-8") as f:
    #     f.write(html_obj)
        