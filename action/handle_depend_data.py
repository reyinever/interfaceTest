from config.case_conf import *
from utils.Log import *


def get_row_obj(pe, sheet_obj, col_no, val):
    """获取excel表指定列指定值所在的行对象"""
    try:
        sheetObj_colNo = pe.getCol(sheet_obj, col_no)
        for idx, cell in enumerate(sheetObj_colNo[1:], 2):  # 从第2行开始，遍历要是否执行列，设置idx从2开始
            # print(cell.value)
            if cell and str(cell.value).strip().lower() == str(val):
                # print(cell.value)
                # 需要执行的api所在的行对象
                sheetObj_rowObj = pe.getRow(sheet_obj, idx)
                # print('so_ro', sheetObj_rowObj)
                return sheetObj_rowObj
    except Exception as e:
        info("获取excel表指定列指定值所在的行对象，发生了异常：%s" % e)


def get_request_data(pe, apisheet_obj, apiNoCaseNo,
                     casesheet_requestData,
                     casesheet_dependRequestDataFields,
                     casesheet_dependResponseDataFields,
                     casesheet_dependStoreRequestDataFields,
                     casesheet_dependStoreResponseDataFields):
    """处理请求依赖数据"""
    try:
        if apiNoCaseNo:
            apiNoCaseNo = eval(apiNoCaseNo)
        if casesheet_requestData:
            casesheet_requestData = eval(casesheet_requestData)
        if casesheet_dependRequestDataFields:
            casesheet_dependRequestDataFields = eval(casesheet_dependRequestDataFields)
        if casesheet_dependResponseDataFields:
            casesheet_dependResponseDataFields = eval(casesheet_dependResponseDataFields)
        if casesheet_dependStoreRequestDataFields:
            casesheet_dependStoreRequestDataFields = eval(casesheet_dependStoreRequestDataFields)
        if casesheet_dependStoreResponseDataFields:
            casesheet_dependStoreResponseDataFields = eval(casesheet_dependStoreResponseDataFields)

        apiNo, caseNo = apiNoCaseNo
        apisheet_rowObj = get_row_obj(pe, apisheet_obj, API_apiNo, apiNo)

        # 依赖数据所在的表名
        caseSheetName_depend = apisheet_rowObj[API_caseSheetName - 1].value

        # 依赖数据所在的表
        casesheet_obj_depend = pe.getSheetByName(caseSheetName_depend)
        # 依赖数据所在的行对象
        casesheet_rowObj_depend = get_row_obj(pe, casesheet_obj_depend, CASE_caseNo, caseNo)
        # print("2:", casesheet_rowObj_depend)

        # 获取依赖数据所在行的 requestData
        casesheet_requestData_depend = casesheet_rowObj_depend[CASE_requestData - 1].value
        if casesheet_dependRequestDataFields and casesheet_requestData_depend:
            for k in casesheet_dependRequestDataFields:
                # 请求数据中的依赖数据进行替换
                casesheet_requestData[k] = eval(casesheet_requestData_depend).get(k)
        # print("a:", casesheet_requestData)
        # 获取依赖数据所在行的 responseData
        casesheet_responseData_depend = casesheet_rowObj_depend[CASE_responseData - 1].value
        # print(casesheet_dependResponseDataFields)
        # print(casesheet_responseData_depend)
        if casesheet_dependResponseDataFields and casesheet_responseData_depend:
            for k in casesheet_dependResponseDataFields:
                # print(k)
                # 请求数据中的依赖数据进行替换
                casesheet_requestData[k] = eval(casesheet_responseData_depend).get(k)
        # print('b:', casesheet_requestData)

        # 获取依赖数据所在行的 storeRequestData
        casesheet_storeRequestData_depend = casesheet_rowObj_depend[CASE_storeRequestData - 1].value
        if casesheet_dependStoreRequestDataFields and casesheet_storeRequestData_depend:
            for k in casesheet_dependStoreRequestDataFields:
                # 请求数据中的依赖数据进行替换
                casesheet_requestData[k] = eval(casesheet_storeRequestData_depend).get(k)
        # print("c", casesheet_requestData)

        # 获取依赖数据所在行的 storeResponseData
        casesheet_storeResponseData_depend = casesheet_rowObj_depend[CASE_storeResponseData - 1].value
        if casesheet_dependStoreResponseDataFields and casesheet_storeResponseData_depend:
            for k in casesheet_dependStoreResponseDataFields:
                # 请求数据中的依赖数据进行替换
                casesheet_requestData[k] = eval(casesheet_storeResponseData_depend).get(k)
        info("处理依赖数据完成：%s" % casesheet_requestData)
        return casesheet_requestData
    except Exception as e:
        info("处理请求依赖数据，发生了异常：%s" % e)
