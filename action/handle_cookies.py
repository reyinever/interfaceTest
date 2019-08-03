from config.path_conf import cookies_path
import json
from utils.Log import *


def get_cookies():
    """读取cookies"""
    try:
        with open(cookies_path,'r') as fp:
            cookies=json.load(fp)
            # print(cookies)
            return cookies
    except Exception as e:
        info("读取cookies发生异常：%s"%e)


def set_cookies(cookies_data):
    """写headers"""
    try:
        with open(cookies_path,'w') as fp:
            json.dump(cookies_data,fp)
        info("保存cookies成功，cookies：%s"%cookies_data)
        return True
    except Exception as e:
        info("保存cookies发生异常：%s"%e)
        return False


if __name__ == '__main__':
    d={"login":"true"}
    print(set_cookies(d))
    print(get_cookies())