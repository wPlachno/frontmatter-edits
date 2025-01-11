# wcprinter.py
# Version: 0.0.1.011
# Last Changes: 01/07/2025

from utilities.wcconstants import Verbosity, PRINT

class WoodchipperToolkitPrinter:
    def __init__(self, verbosity=Verbosity.NORMAL):
        self.verbosity = verbosity

    def verb(self, verbosity):
        return self.verbosity >= verbosity

    def pr(self, text, verbosity=Verbosity.NORMAL, new_line=True):
        end = "\n" if new_line else ""
        if self.verb(verbosity):
            print(text, end=end)

    def nl(self, verbosity=Verbosity.NORMAL):
        self.pr(text="", verbosity=verbosity)

    def error(self, text, verbosity=Verbosity.NORMAL, new_line=True):
        self.pr(PRINT.ERROR.format(text), verbosity=verbosity, new_line=new_line)

    def label(self, text, verbosity=Verbosity.NORMAL, new_line=True):
        self.pr(PRINT.LABEL.format(text), verbosity=verbosity, new_line=new_line)

    def kvp(self, key, value, verbosity=Verbosity.NORMAL, new_line=True):
        self.pr(PRINT.KVP.format(key, str(value)), verbosity=verbosity, new_line=new_line)

    def on_bool(self, condition, if_true, if_false, verbosity=Verbosity.NORMAL, new_line=True):
        print_st = if_true if condition else if_false
        self.pr(print_st, verbosity=verbosity, new_line=new_line)

    def v_frame(self, frame_list, *args, new_line=True):
        self.pr(frame_list[self.verbosity].format(*args), new_line=new_line)



