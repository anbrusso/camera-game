class Debug:
    debug_on = False
    @staticmethod
    def print_debug(self,message):
        if debug:
            print(message)
    @staticmethod
    def set_debug(self,val):
        debug_on = val