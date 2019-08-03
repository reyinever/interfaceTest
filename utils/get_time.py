import time


def get_current_date():
    current_date = time.strftime("%Y-%m-%d")
    return current_date


def get_current_time():
    current_time = time.strftime("%Y-%m-%d_%H-%M-%S")
    return current_time
