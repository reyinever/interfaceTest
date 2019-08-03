import os

# 项目路径
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 测试数据所在的目录
test_data_dir = project_path + '\\testdata'
# 测试用例路径
test_data_file_path = project_path + '\\testdata\\test_case.xlsx'
# 日志配置文件路径
log_config_path = os.path.join(project_path, "config", "Logger.conf")
# 测试唯一数文件路径
unique_num_path = os.path.join(test_data_dir, 'unique_num.json')
# 存储headers路径
headers_path = os.path.join(test_data_dir, "headers.json")
# 存储cookies路径
cookies_path = os.path.join(test_data_dir, "cookies.json")
# 报告的存储目录
report_dir = os.path.join(project_path, "report")
