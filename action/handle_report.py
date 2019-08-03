from utils.html_report import report_html
from utils.get_report_name import get_report_name


def new_report(data):
    report_html(data, html_name=get_report_name())
