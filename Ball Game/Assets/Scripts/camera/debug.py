#globally used debug file.
debug_on = False#by default, debug is turned off
def log(message):
    """Same as print, but will print only when debugging flag is turned on."""
    global debug_on
    if debug_on:
        print(message)
def set_debug(val):
    """Turns on debug flag, which allows log to start printing."""
    global debug_on
    debug_on = val