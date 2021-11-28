import time


# Module for test use
def test(i):
    '''
    >>> test(2)
    [DEBUG] Output is 1
    '''
    print("[DEBUG] Output is", i)


# Debug
# Log
'''
Usage: log(str)
It will create log.txt in the directroy.
'''
def log(logt=""):
    time_now = timestamp.calc()
    logt = f"[{time_now}] {logt}\n"
    logf = open("log.txt", mode='a')
    logf.write(logt)

# Timestamp
def timestamp():
    def init():
        global time_start
        time_start = time.time()
        log()
        logt = "[MAIN] Program started"
        log(logt)

    def calc():
        time_now = time.time()
        start_t = time_now - time_start
        start_time = round(start_t, 2)
        return start_time
