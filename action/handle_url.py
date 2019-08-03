from config.url_conf import url
from utils.Log import *
import re


def get_url(apisheet_requestPath):
    """拼接域名和path"""
    try:
        request_url = url.rstrip("/") + '/' + apisheet_requestPath.lstrip("/")
        return request_url
        info("处理apisheet url为：%s" % request_url)
    except Exception as e:
        info("处理url发生异常：%s" % e)


def handle_url_params(apisheet_requestUrl, casesheet_requestData):
    """替换url中的参数"""
    try:
        params = re.findall(r'{(.+?)}', apisheet_requestUrl)
        # print(params)
        if len(params) > 0:
            for p in params:
                value = casesheet_requestData.get(p)
                if value:
                    apisheet_requestUrl = apisheet_requestUrl.replace("{%s}" % p, str(value))
        info("替换url中的参数后，请求url是: %s" % apisheet_requestUrl)
        return apisheet_requestUrl
    except Exception as e:
        info("处理url中的参数发生异常:%s" % e)
