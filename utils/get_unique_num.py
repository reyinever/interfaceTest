from config.path_conf import unique_num_path
import os
import json
from utils.Log import *


def get_unique_num(get_num_path=unique_num_path):
    """获取唯一数"""
    try:
        if os.path.exists(get_num_path) and os.path.getsize(get_num_path) > 0:
            with open(get_num_path, "r") as fp:
                data = json.load(fp)
                # print(data)
                value = data.get("unique_number")
                info("获取的唯一数据是：%s" % value)
                data["unique_number"] += 1
        else:
            value = 111
            data = {"unique_number": value + 1}
        with open(get_num_path, "w") as fp:
            json.dump(data, fp)
            info("保存的下一个获取的唯一数据是：%s" % data)
        return value
    except Exception as e:
        print(e)
        info(" 获取测试数据中的唯一数发生异常：%s" % e)


if __name__ == '__main__':
    print(get_unique_num())
