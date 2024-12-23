from zhipuai import ZhipuAI

def chat_model(input_text):
    client = ZhipuAI(api_key="fb0f562368872376dd7d338811ab92ee.2kTbUmK0gsfVKUuU") # 填写您自己的APIKey
    response = client.chat.completions.create(
        model="glm-4v",  # 填写需要调用的模型名称
        messages=[
        {
            "role": "user",
            "content": [
            {
                "type": "text",
                "text": input_text
            },
            ]
        }
        ]
    )
    print(response.choices[0].message)
    print(response.choices[0].message.content)
    return response.choices[0].message.content

if __name__ == "__main__":
    chat_model("这是一个app的检测结果，请依据以下内容帮我写一篇分析报告：APP名称是test,APP权限分析是['android.permission.QUERY_ALL_PACKAGES', 'android.permission.MANAGE_EXTERNAL_STORAGE', 'com.metanet.house.permission.KW_SDK_BROADCAST', 'android.permission.ACCESS_WIFI_STATE', 'android.permission.ACCESS_NETWORK_STATE', 'android.permission.CHANGE_CONFIGURATION', 'freemme.permission.msa', 'android.permission.GET_TASKS', 'android.permission.INTERNET'],APP危险等级是black,APP类型是危险,APP后台通联地址是http://test.com,")