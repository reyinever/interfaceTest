from utils.get_unique_num import get_unique_num
from utils.Log import *


def handle_unique_num(request_data):
    try:
        if "${unique_num}" in request_data:
            request_data = request_data.replace("${unique_num}", str(get_unique_num()))
            return request_data
        else:
            info("请求中没有包含使用唯一数的变量")
    except Exception as e:
        info("替换请求参数中的唯一数发生异常：%s" % e)
