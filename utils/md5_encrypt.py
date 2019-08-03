"""md5加密"""
import hashlib


def md5_encrypt(str):
    # 创建md5实例
    m5 = hashlib.md5()
    m5.update(str.encode('utf-8'))
    value = m5.hexdigest()
    return value
