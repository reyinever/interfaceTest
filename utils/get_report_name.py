from config.path_conf import report_dir
import os
from utils.get_time import get_current_time


def get_report_name():
    return os.path.join(report_dir, get_current_time() + "_report")


if __name__ == '__main__':
    print(get_report_name())
