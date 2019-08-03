import requests
from utils.Log import *


class HttpClient(object):
    """模拟客户端发送请求"""

    def __init__(self):
        pass

    def request(self, requestUrl, requestMethod, paramsType=None, requestData=None, headers=None, cookies=None):
        try:
            # 替换url中的参数
            if "{" in requestUrl:
                for k in requestData:
                    requestUrl = requestUrl.replace("{%s}" % k, str(requestData[k]))
            # print(requestUrl)
        except Exception as e:
            info("requestUrl参数处理异常：%s" % e)

        try:
            if requestMethod.lower() == "post":
                if paramsType is None or paramsType.lower() == "url":
                    response = requests.post(url=requestUrl, headers=headers, cookies=cookies)
                    return response
                elif paramsType.lower() == "form":
                    response = requests.post(url=requestUrl, data=requestData, headers=headers, cookies=cookies)
                    return response
                elif paramsType.lower() == "json":
                    response = requests.post(url=requestUrl, json=requestData, headers=headers, cookies=cookies)
                    return response
                elif paramsType.lower() == "files":
                    response = requests.post(url=requestUrl, files=requestData, headers=headers, cookies=cookies)
                    return response

            elif requestMethod.lower() == "get":
                if paramsType is None or paramsType.lower() == "url":
                    response = requests.get(url=requestUrl, headers=headers, cookies=cookies)
                    return response
                elif paramsType.lower() == "params":
                    response = requests.get(url=requestUrl, params=requestData, headers=headers, cookies=cookies)
                    return response
                elif paramsType.lower() == "json":
                    response = requests.get(url=requestUrl, json=requestData, headers=headers, cookies=cookies)
                    return response

            elif requestMethod.lower() == "patch":
                if paramsType is None or paramsType.lower() == "url":
                    response = requests.patch(url=requestUrl, headers=headers, cookies=cookies)
                    return response
                elif paramsType.lower() == "params":
                    response = requests.patch(url=requestUrl, data=requestData, headers=headers, cookies=cookies)
                    return response
            elif requestMethod.lower() == "delete":
                if paramsType is None or paramsType.lower() == "url":
                    response = requests.delete(url=requestUrl, headers=headers, cookies=cookies)
                    return response
                elif paramsType.lower() == "params":
                    response = requests.delete(url=requestUrl, data=requestData, headers=headers, cookies=cookies)
                    return response
            else:
                print("")
                info("不支持的请求方式：%s" % paramsType)
        except Exception as e:
            print(e)
            info("HttpClient发请求异常：%s" % e)
