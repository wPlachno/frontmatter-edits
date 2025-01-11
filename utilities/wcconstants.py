"""
wcconstants.py
Created by Will Plachno on 09/07/24
Version: 0.0.1.011
Last Changes: 01/03/2025

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
    RED='\033[0;31m'
    GREY='\033[90m'
    YELLOW='\033[93m'
    BLUE='\033[94m'
    DARK_YELLOW='\033[0;33m'
    GREEN='\033[0;32m'
    DARK_GREEN='\033[2;32m'
    PURPLE='\033[0;35m'
    BLACK='\033[0;30m'
    WHITE='\033[37m'
    DEFAULT='\033[0m'

class COLOR:
    SUPER=  COLOUR.PURPLE
    SUB=    COLOUR.GREY
    SUBSIB= COLOUR.DARK_GREEN
    SIBLING=COLOUR.DARK_YELLOW
    OPTION= COLOUR.BLUE
    QUOTE=  COLOUR.GREEN
    ACTIVE= COLOUR.GREEN
    CANCEL= COLOUR.RED
    DEFAULT=COLOUR.DEFAULT

def clr(text, color):
    return color + text + COLOUR.DEFAULT

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
                   "positive", "a", "p"))

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
