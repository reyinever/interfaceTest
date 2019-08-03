import re
from utils.Log import *


def assert_result(response_data, assert_data):
    # 支持的交验方式 值、正则、类型
    # 如： {"code":"00","userid":{"value":"\w+"},"id":{"type":"int"}}
    try:
        error_key = {}
        for key, value in assert_data.items():
            if isinstance(value, str):
                # 通过值校验
                if response_data[key] != value:
                    error_key[key] = response_data[key]
            elif isinstance(value, dict):
                if value.get('value', None):
                    # 通过正则校验
                    reg_str = value['value']
                    reg_res = re.match(reg_str, '%s' % response_data[key])
                    if not reg_res:
                        error_key[key] = response_data

                elif value.get('type', None):
                    # 校验数据类型
                    type_str = value['type']
                    if not isinstance(response_data[key], eval(type_str.lower())):
                        error_key[key] = response_data

        # info("断言结果：%s"%error_key)
        return error_key
    except Exception as e:
        info("断言结果发生异常：%s" % e)
