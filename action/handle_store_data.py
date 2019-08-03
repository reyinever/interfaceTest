from utils.Log import *
from config.case_conf import *
from action.handle_headers import set_headers
from utils.md5_encrypt import md5_encrypt
from action.handle_cookies import set_cookies


def store_data(pe, casesheet_obj, row_no, store_data_fields, request_data, response_obj):
    """存储数据"""
    try:
        # 存储的数据
        store_request_data = {}
        store_response_data = {}
        response_data = response_obj.json()
        if isinstance(store_data_fields, dict) and isinstance(request_data, dict) and isinstance(response_data, dict):
            # print(store_data_fields)
            for k, v in store_data_fields.items():
                if k == "request":
                    for i in v:
                        store_request_data[i] = request_data[i]
                        if i == "password":
                            store_request_data[i] = md5_encrypt(store_request_data[i])
                    print(store_request_data)
                    info("存储请求数据：%s" % store_request_data)
                    # 存储的数据写入用例表中
                    pe.writeCell(casesheet_obj, content='%s' % store_request_data, rowNo=row_no,
                                 colNo=CASE_storeRequestData)

                if k == "response":
                    for i in v:
                        store_response_data[i] = response_data[i]
                    # info("响应数据：%s"%response_data)
                    info("存储响应数据：%s" % store_response_data)

                    # 存储的数据写入用例表中
                    pe.writeCell(casesheet_obj, content="%s" % store_response_data, rowNo=row_no,
                                 colNo=CASE_storeResponseData)

                if k == "headers":
                    # 存储响应中的token
                    token = response_data.get("token")
                    headers_data = {"Authorization": "Bearer %s" % token}
                    set_headers(headers_data)
                    info("存储请求头数据：%s" % headers_data)

                if k == "cookies":
                    cookieJar = response_obj.cookies
                    cookies = {}
                    for k, v in cookieJar.items():
                        cookies[k] = v
                    info("cookies：%s" % cookies)
                    set_cookies(cookies)

            return "success"

        return "faild"

    except Exception as e:
        info("数据存储发生异常：%s" % e)
