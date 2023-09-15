import time

def get_time():
    try:
        curr_time = time.strftime("%H:%M", time.localtime())
        return curr_time
    except:
        print("Ошибка получения ВРЕМЕНИ")


