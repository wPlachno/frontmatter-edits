"""
wcconstants.py
Created by Will Plachno on 09/07/24
Version: 0.0.1.014
Last Changes: 01/20/2025

Woodchipper Constants
An assortment of helpful strings and other constants.
"""

class KEY:
    EMPTY=""
    NL="\n"     # New Line
    FS="/"      # Forward Slash
    BS="\\"     # Back Slash
    QU="\""     # Quotes
    CD=", "     # Comma Delimiter
    SDL=":"     # IS THIS USED?
    ES="."      # End Statement
    EL=".\n"    # End line

    CS=": "     # Colon Separator
    DH=" - "    # Description Hyphen

OOB=-1

OP = {
    0:"{0}",
    1:"{1}",
    2:"{2}",
    3:"{3}",
    4:"{4}",
    5:"{5}"
}

class COLOUR:

    DEFAULT='\033[0m'

    BLACK       ='\033[38;5;0m'
    DARK_RED    ='\033[38;5;1m'
    DARK_GREEN  ='\033[38;5;2m'
    DARK_YELLOW ='\033[38;5;3m'
    DARK_BLUE   ='\033[38;5;4m'
    DARK_PURPLE ='\033[38;5;5m'
    DARK_TEAL   ='\033[38;5;6m'
    DARK_WHITE  ='\033[38;5;7m'

    GREY        ='\033[38;5;8m'
    RED         ='\033[38;5;9m'
    GREEN       ='\033[38;5;10m'
    YELLOW      ='\033[38;5;11m'
    BLUE        ='\033[38;5;12m'
    PURPLE      ='\033[38;5;13m'
    TEAL        ='\033[38;5;14m'
    WHITE       ='\033[38;5;15m'

class BG:

    DEFAULT='\033[0m'

    BLACK       ='\033[48;5;0m'
    DARK_RED    ='\033[48;5;1m'
    DARK_GREEN  ='\033[48;5;2m'
    DARK_YELLOW ='\033[48;5;3m'
    DARK_BLUE   ='\033[48;5;4m'
    DARK_PURPLE ='\033[48;5;5m'
    DARK_TEAL   ='\033[48;5;6m'
    DARK_WHITE  ='\033[48;5;7m'

    GREY        ='\033[48;5;8m'
    RED         ='\033[48;5;9m'
    GREEN       ='\033[48;5;10m'
    YELLOW      ='\033[48;5;11m'
    BLUE        ='\033[48;5;12m'
    PURPLE      ='\033[48;5;13m'
    TEAL        ='\033[48;5;14m'
    WHITE       ='\033[48;5;15m'

class COLOR:
    SUPER       =COLOUR.PURPLE
    SUB         =COLOUR.GREY
    SUBSIB      =COLOUR.DARK_GREEN
    SIBLING     =COLOUR.DARK_YELLOW
    OPTION      =COLOUR.DARK_BLUE
    QUOTE       =COLOUR.DARK_TEAL
    ACTIVE      =COLOUR.GREEN
    CANCEL      =COLOUR.DARK_RED
    DEFAULT     =COLOUR.DEFAULT
    PATH_PARENT =COLOUR.DARK_WHITE
    PATH_NAME   =COLOUR.DARK_TEAL

def clr(text, *color):
    codes=color[0]
    for code in color[1:]:
        codes += code
    return codes + text + COLOUR.DEFAULT

class CL_GENERAL:
    ACTIVE = clr("Active", COLOR.ACTIVE)
    INACTIVE = clr("Inactive", COLOR.CANCEL)
    SUCCESS = clr("Success", COLOR.ACTIVE)
    FAILURE = clr("Failure", COLOR.CANCEL)
    ATTRIBUTE = clr(OP[0], COLOR.SIBLING)+KEY.CS+OP[1]+KEY.NL
    TASK = clr("Task", COLOR.SUPER)+KEY.CS
    UNIMPLEMENTED = " ["+clr("UNIMPLEMENTED", COLOR.CANCEL)+"]"

class CL_TASK:
    MODE_CONFIG =   CL_GENERAL.TASK+clr("Config", COLOR.SUB)        +KEY.DH+clr(OP[0], COLOR.SIBLING)+KEY.CS+OP[1]+KEY.NL
    CONFIG_ERROR =  CL_GENERAL.TASK+clr("Config", COLOR.SUB)        +KEY.DH+clr(OP[0], COLOR.CANCEL) +KEY.NL
    TEST_PASS =     CL_GENERAL.TASK+clr("Test Passed", COLOR.SUB)   +KEY.DH+clr(OP[0], COLOR.ACTIVE) +KEY.NL
    TEST_FAIL =     CL_GENERAL.TASK+clr("Test Failed", COLOR.SUB)   +KEY.DH+clr(OP[0], COLOR.CANCEL) +KEY.NL

class FILE_IO:
    READ = "r"
    WRITE = "w"
    EXCLUSIVE_CREATION = "x"

def format_success(success):
    return CL_GENERAL.SUCCESS if success else CL_GENERAL.FAILURE

DEBUG = "debug"
VERBOSE = "verbose"
TEST = "test"
UNDEFINED = "undefined"
ON = "on"
OFF = "off"

FILE_NAME_SETTINGS = ".wcp_Settings.txt"
PREFERRED_TIME_FORMAT = "%m%d%y:%H:%M:%S"
TEST_TAG = "test: "

ON_SYNONYMS = list(("on", "true", "1", "yes",
                   "t", "y", "+", "active",
                   "positive", "a", "p", "enable"))

class Verbosity:
    SILENT = 0 # As little output as possible.
    RESULTS_ONLY = 1 # Only show requested
    NORMAL = 2 # Includes warnings and big errors
    DEBUG = 3 # Print all messages possible

class MODE:
    NONE = "none"
    TEST = "test"
class PRINT:
    ERROR = clr("ERROR: ", COLOR.CANCEL)+OP[0]+KEY.NL
    KVP = clr(OP[0], COLOR.SIBLING)+KEY.CS+OP[1]
    LABEL = clr(OP[0], COLOR.SUPER)+KEY.CS
class RESULTS:
    SUCCESS = "success"
    ERROR = "error"
