from time import time
timings = {}
starts = {}

def timer_start(flag):
    global start
    global starts

    starts[flag] = time()

def timer_stop(flag):
    global timings
    global starts

    if not flag in timings:
        timings[flag] = 0
    timings[flag] = timings[flag] + (time() - starts[flag])

def timer_print_timings():
    for flag in timings:
        print '[Timer] %s: %f' % (flag, timings[flag])
