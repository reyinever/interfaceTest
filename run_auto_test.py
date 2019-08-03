from utils.ParseExcel import ParseExcel
from config.path_conf import test_data_file_path
from config.case_conf import *
from action.handle_url import get_url,handle_url_params
from action.handle_headers import get_headers
from action.handle_cookies import get_cookies
from action.handle_depend_data import get_request_data
from action.handle_unique_num import handle_unique_num
from action.handle_encrypt import handler_encrypt
from utils.Log import *
from action.handle_store_data import store_data
from action.assert_result import assert_result
from action.write_result import write_result,clear_result,write_api_result,clear_api_result
from utils.HttpClient import HttpClient
import time
from utils.get_report_name import get_report_name
from utils.html_report import report_html
from utils.send_mail import send_mail


def run_test():
    # 解析测试数据excel表
    pe=ParseExcel()
    pe.loadWorkBook(r'%s'%test_data_file_path)
    # 获取接口表数据
    apisheet_obj=pe.getSheetByName('API')
    # 获取是否执行列
    apisheet_isExecute=pe.getCol(apisheet_obj,API_isExecute)
    # print(apisheet_isExecute)

    # 统计总数
    execute_case_no=0
    faild_case_no=0
    success_case_no=0

    # 生成报告数据
    test_results_for_html_report=[]

    # info("-----------------执行api--------------------")
    for idx,cell in enumerate(apisheet_isExecute[1:],2):  # 从第2行开始，遍历要是否执行列，设置idx从2开始
        # 接口需要执行的接口
        if cell.value and cell.value.strip().lower()=='y':
            # 需要执行的接口所在的行对象
            apisheet_rowObj=pe.getRow(apisheet_obj,idx)
            # api名称
            apisheet_apiName=apisheet_rowObj[API_apiName-1].value
            apisheet_requestPath=apisheet_rowObj[API_requestPath - 1].value
            apisheet_requestMethod=apisheet_rowObj[API_requestMethod-1].value
            apisheet_paramsType=apisheet_rowObj[API_paramsType-1].value
            apisheet_headers=apisheet_rowObj[API_headers-1].value
            apisheet_cookies=apisheet_rowObj[API_cookies-1].value

            info("---------------执行api：%s------------------"%apisheet_apiName)

            # 测试用例表名
            apisheet_caseSheetName=apisheet_rowObj[API_caseSheetName-1].value

            # 处理api请求url
            apisheet_requestUrl = get_url(apisheet_requestPath)

            # 统计每个api的执行结果
            api_case_no=0
            api_case_success_no=0
            api_case_fail_no=0

            info("------------------执行用例：%s-----------------"%apisheet_caseSheetName)
            # 获取测试用例表对象
            casesheet_obj=pe.getSheetByName(apisheet_caseSheetName)
            # 获取是否需要执行的用例列对象
            casesheet_isExecute=pe.getCol(casesheet_obj,CASE_isExecute)
            for c_idx,c_cell in enumerate(casesheet_isExecute[1:],2):
                # 用例是否执行
                if c_cell.value and  c_cell.value.strip().lower()=='y':

                    execute_case_no+=1
                    api_case_no+=1

                    # 获取要执行的用例表的行对象
                    casesheet_rowObj=pe.getRow(casesheet_obj,c_idx)

                    casesheet_caseName=casesheet_rowObj[CASE_caseName-1].value
                    casesheet_requestData=casesheet_rowObj[CASE_requestData-1].value
                    # 依赖字段
                    casesheet_dependApiNoCaseNo=casesheet_rowObj[CASE_dependApiNoCaseNo-1].value
                    casesheet_dependRequestDataFields=casesheet_rowObj[CASE_dependRequestDataFields-1].value
                    casesheet_dependResponseDataFields=casesheet_rowObj[CASE_dependResponseDataFields-1].value
                    casesheet_dependStoreRequestDataFields=casesheet_rowObj[CASE_dependStoreRequestDataFields-1].value
                    casesheet_dependStoreResponseDataFields=casesheet_rowObj[CASE_dependStoreResponseDataFields-1].value

                    casesheet_storeDataFields=casesheet_rowObj[CASE_storeDataFields-1].value
                    casesheet_assertData=casesheet_rowObj[CASE_assertData-1].value

                    # info("----------------------请求前数据处理-----------------------")

                    # 处理url中的参数
                    if '{'in apisheet_requestUrl:
                        apisheet_requestUrl = handle_url_params(apisheet_requestUrl,eval(casesheet_requestData))

                    # 获取headers
                    if apisheet_headers and apisheet_headers.strip().lower()=='y':
                        apisheet_headers=get_headers()

                    # 获取cookies
                    if apisheet_cookies and apisheet_cookies.strip().lower()=='y':
                        apisheet_cookies=get_cookies()

                    # 处理唯一数
                    if "${unique" in casesheet_requestData:
                        casesheet_requestData=handle_unique_num(casesheet_requestData)

                    # 处理加密数据
                    if "${encrypt" in casesheet_requestData:
                        casesheet_requestData=handler_encrypt(casesheet_requestData)

                    # 处理依赖数据
                    if casesheet_dependApiNoCaseNo:
                        casesheet_requestData=get_request_data(pe,apisheet_obj,
                                                               casesheet_dependApiNoCaseNo,
                                                               casesheet_requestData,
                                                               casesheet_dependRequestDataFields,
                                                               casesheet_dependResponseDataFields,
                                                               casesheet_dependStoreRequestDataFields,
                                                               casesheet_dependStoreResponseDataFields)


                    if not isinstance(casesheet_requestData,dict):
                        casesheet_requestData=eval(casesheet_requestData)

                    info("----------------------发送请求-----------------------")
                    info("请求 url：%s" % apisheet_requestUrl)
                    info("请求 方法：%s" % apisheet_requestMethod)
                    info("请求参数类型：%s" % apisheet_paramsType)
                    info("请求数据：%s" % casesheet_requestData)
                    info("请求头数据：%s" % apisheet_headers)
                    info("请求cookies数据：%s" % apisheet_cookies)

                    httpc=HttpClient()

                    # 请求计时开始
                    start_time=time.time()

                    # 发送请求
                    response=httpc.request(requestUrl=apisheet_requestUrl,
                                           requestMethod=apisheet_requestMethod,
                                           paramsType=apisheet_paramsType,
                                           requestData=casesheet_requestData,
                                           headers=apisheet_headers,
                                           cookies=apisheet_cookies
                                           )
                    # 耗时
                    escape_time=time.time()-start_time

                    info("响应结果：%s"%response)

                    # 请求成功
                    if response.status_code==200:
                        info("------------------处理响应数据-------------------")
                        # 响应数据
                        casesheet_responseData=response.json()

                        response_content=response.content.decode('utf-8')

                        info("响应数据：%s"%response.content.decode('utf-8'))

                        # 存储依赖数据
                        if casesheet_storeDataFields:
                            store_result=store_data(pe,casesheet_obj,c_idx,eval(casesheet_storeDataFields),casesheet_requestData,response)
                            info("存储依赖数据执行结果：%s"%store_result)

                        # 比对结果
                        error_key={}
                        if casesheet_assertData:
                            error_key=assert_result(casesheet_responseData,eval(casesheet_assertData))

                        info("断言结果error_key：%s"%error_key)

                        if error_key:
                            faild_case_no+=1
                            api_case_fail_no+=1
                            test_results_for_html_report.append((apisheet_requestUrl,casesheet_requestData,
                                                                 response_content,int(escape_time*1000),
                                                                 casesheet_assertData,"失败"))
                        else:
                            success_case_no+=1
                            api_case_success_no+=1
                            test_results_for_html_report.append((apisheet_requestUrl, casesheet_requestData,
                                                                 response_content, int(escape_time*1000),
                                                                 casesheet_assertData, "成功"))

                        # 写测试结果
                        write_result(pe,casesheet_obj,casesheet_responseData,error_key,c_idx,escape_time)
                    else:
                        info('响应失败，响应状态码：%s'%response.status_code)
                        clear_result(pe, casesheet_obj, row_no=c_idx)
                else:
                    clear_result(pe, casesheet_obj,row_no=c_idx)
                    info('case：%s 被忽略执行'%casesheet_caseName)

            # 写接口的执行结果
            write_api_result(pe, apisheet_obj, idx, api_case_no, api_case_success_no, api_case_fail_no)

        else:
            #清空忽略执行的接口结果
            clear_api_result(pe,apisheet_obj,idx)
            info('api：%s 被忽略执行'%apisheet_apiName)

    # 写报告
    info("-------------------生成报告--------------------")
    report_name=get_report_name()
    report_html(data=test_results_for_html_report,html_name=report_name)

    time.sleep(3)

    # 发送邮件
    info("-------------------发送邮件--------------------")
    send_file=report_name+'.html'
    send_content="本次自动化测试共执行用例数：%s，成功数：%s，失败数：%s,成功率：%.2f%%"\
                 %(execute_case_no,success_case_no,faild_case_no,success_case_no/execute_case_no*100)
    send_mail(send_file,send_content)


if __name__ == '__main__':
    """执行测试"""
    run_test()


