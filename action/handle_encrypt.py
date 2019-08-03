import re
from utils.Log import *
from utils.md5_encrypt import md5_encrypt


def handler_encrypt(request_data):
    """加密数据处理"""
    try:
        if '${encrypt_md5(' in request_data:
            str_val = re.search(r'\$\{encrypt_md5\((.+?)\)\}', request_data)
            # print(str_val)
            if str_val:
                md5_val = md5_encrypt(str_val.group(1))
                request_data = re.sub(r'\$\{encrypt_md5\(.+?\)\}', md5_val, request_data)
                info("加密处理后的数据是：%s" % request_data)
                return request_data
            else:
                info("没有匹配到要 md5 加密的数据：%s" % request_data)
        else:
            info("invalid encrypt type %s" % request_data)
    except Exception as e:
        info("处理 MD5 加密数据异常：%s" % e)

# base64加密
