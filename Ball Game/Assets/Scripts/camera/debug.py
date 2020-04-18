debug_on = False
def log(message):
    global debug_on
    if debug_on:
        print(message)
def set_debug(val):
    global debug_on
    debug_on = val