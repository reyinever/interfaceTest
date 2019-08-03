from config.path_conf import headers_path
import json
from utils.Log import *


def get_headers():
    """读取headers"""
    try:
        with open(headers_path, 'r') as fp:
            headers = json.load(fp)
            return headers
    except Exception as e:
        info("读取headers发生异常：%s" % e)


def set_headers(headers_data):
    """写headers"""
    try:
        with open(headers_path, 'w') as fp:
            json.dump(headers_data, fp)
        info("保存headers成功，headers：%s" % headers_data)
        return True
    except Exception as e:
        info("保存headers发生异常：%s" % e)
        return False
