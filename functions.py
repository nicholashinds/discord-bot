import datetime


def get_time():
    time = datetime.datetime.now().strftime("%b %d, %Y at %H:%M:%S")
    return time
