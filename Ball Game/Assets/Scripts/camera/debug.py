#globally used debug file.
debug_on = False#by default, debug is turned off
#log procedure will print only when debugging is turned on.
def log(message):
    global debug_on
    if debug_on:
        print(message)
def set_debug(val):
    global debug_on
    debug_on = val