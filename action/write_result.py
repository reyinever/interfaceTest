from config.case_conf import *
from utils.Log import *
from utils.get_time import get_current_time


def write_result(pe, casesheet_obj, response_data, error_key, row_no, escape_time):
    try:
        # 写响应数据
        pe.writeCell(sheet=casesheet_obj, content='%s' % response_data, rowNo=row_no, colNo=CASE_responseData)
        if error_key:
            # 断言失败
            pe.writeCell(sheet=casesheet_obj, content='fail', rowNo=row_no, colNo=CASE_result, font_color='RED')
            pe.writeCell(sheet=casesheet_obj, content='%s' % error_key, rowNo=row_no, colNo=CASE_errorInfo)
        else:
            # 断言成功
            pe.writeCell(sheet=casesheet_obj, content='pass', rowNo=row_no, colNo=CASE_result, font_color='GREEN')
            pe.writeCell(sheet=casesheet_obj, content='', rowNo=row_no, colNo=CASE_errorInfo)
        pe.writeCell(sheet=casesheet_obj, content="%s" %int(escape_time * 1000), rowNo=row_no, colNo=CASE_escapeTime)
        pe.writeCell(sheet=casesheet_obj, content="%s" % get_current_time(), rowNo=row_no, colNo=CASE_executeTime)
        info("断言结果 error_key：%s" % error_key)
    except Exception as e:
        info("断言结果发生异常：%s" % e)


def clear_result(pe, casesheet_obj, row_no):
    """清空忽略的用例结果数据"""
    pe.writeCell(sheet=casesheet_obj, content='', rowNo=row_no, colNo=CASE_result)


def write_api_result(pe, apisheet_obj, row_no, total_no, pass_no, fail_no):
    pe.writeCell(sheet=apisheet_obj, content='%s' % get_current_time(), rowNo=row_no, colNo=API_executeTime)
    if pass_no == total_no:
        pe.writeCell(sheet=apisheet_obj, content='pass', rowNo=row_no, colNo=API_result, font_color="green")
    else:
        pe.writeCell(sheet=apisheet_obj, content='fail', rowNo=row_no, colNo=API_result, font_color="red")
    pe.writeCell(sheet=apisheet_obj, content='%s' % total_no, rowNo=row_no, colNo=API_executeNo)
    pe.writeCell(sheet=apisheet_obj, content='%s' % pass_no, rowNo=row_no, colNo=API_passNo)
    if fail_no==0:
        pe.writeCell(sheet=apisheet_obj, content='%s' % fail_no, rowNo=row_no, colNo=API_failNo)
    else:
        pe.writeCell(sheet=apisheet_obj, content='%s' % fail_no, rowNo=row_no, colNo=API_failNo,font_color='red')


def clear_api_result(pe, apisheet_obj, row_no):
    pe.writeCell(sheet=apisheet_obj, content='', rowNo=row_no, colNo=API_result)
