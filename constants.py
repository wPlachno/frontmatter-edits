class TOKEN:
    FRONTMATTER = "---"
    class LINK:
        class QUOTED:
            START = '"[['
            END = ']]"'
        class RAW:
            START = "[["
            END = "]]"

EMPTY = ""
NL = "\n"
COLON = ":"
FORWARDSLASH = "/"
BACKSLASH = "\\"
MD = ".md"
FM_TOKEN = "---"
FM_LINE = "---\n"

FRAME_PLAIN_ACTION = "{2}: {0} {1}"
FRAME_PROPERTIES_IN = "Properties seen in {0}: "
FRAME_PROPERTY = "{0}: {1}"
FRAME_SUMMARY_HEADER = "{0} files affected"
FRAME_SUMMARY_ITEM = "- {0}\n"

MODE_ADD = "ADD"
MODE_SET = "SET"
MODE_CHANGE = "CHANGE"
MODE_REMOVE = "REMOVE"
MODE_TOTAL = "TOTAL"
MODE_HELP = "HELP"
MODE_MENU = "MENU"

MENU_CHOICE_INVALID = -1
MENU_CHOICE_ADD = 0
MENU_CHOICE_SET = 1
MENU_CHOICE_CHANGE = 2
MENU_CHOICE_REMOVE = 3
MENU_CHOICE_TOTAL = 4
MENU_CHOICE_DIR_SET = 5
MENU_CHOICE_DIR_CLEAR = 6
MENU_CHOICE_QUIT = 7

USE_WORKING = "."
FAKE_PROPERTY = "A: B"
DIRECTORY_NONE = "No Working Directory"
DIRECTORY_CHANGED = "Working Directory: {0}"


ERROR_NOT_ENOUGH_ARGUMENTS = "Incorrect Arguments: You have not given us enough arguments. Correct syntax: [ADD/SET/CHANGE/REMOVE/TOTAL] [Key]:[Value] [Root Folder Path (Optional)]"
ERROR_INVALID_COMMAND = "Invalid Command: Our command choices are ADD, SET, CHANGE, REMOVE, or TOTAL."
ERROR_INVALID_PROPERTY = "Incorrect Property: Please provide the property, in form \"[KEY]:[VALUE\", as the first argument,and a directory path as the optional second argument."
ERROR_INVALID_DIRECTORY = "Invalid Directory: The path you passed did not resolve to a valid directory."

SCREEN_HELP_HEADER = "Welcome!"
SCREEN_HELP_TEXT = """You can use this python script to edit a frontmatter property across an entire directory.
Modes: 
- ADD: Adds a property if it does not already exist. Does not change any existing values.
- SET: Adds a property if it does not already exist. Also sets any existing values.
- CHANGE: Sets the value of a property, but only if it already exists.
- REMOVE: Removes a property from all files.
- TOTAL: Collects all properties mentioned in these files.
Syntax: [MODE] [Property_key]:[Property_value] [OPTIONAL directory_path]
Or you can pass no arguments and enter interactive mode!"""

SCREEN_WELCOME_HEADER = SCREEN_HELP_HEADER
SCREEN_WELCOME_TEXT = """Welcome to the Frontmatter-Edit project.
This python script was designed to add properties to the frontmatter of an entire directory's markdown files.
When using the script, you'll be asked which mode to operate in.
Add will add the property with the given value to all files that dont already have it.
Set will make sure every file has the property with the given value.
Change will set every file that has the property to the given value.
Remove will delete the given property from all files.
Total will describe every property in any file.
"""

SCREEN_MENU_HEADER = "Main Menu"
SCREEN_MENU_TEXT = ["Add a property","Set a property","Change a property", "Remove a property","Total the properties","Set the Directory", "Clear any set directory", "Quit"]

SCREEN_PROPERTY_HEADER = "{0}: {1}"
SCREEN_PROPERTY_TEXT = """Please enter a property.
The property should be in the format \"[Key]: [Value]\", all in quotation marks."""

SCREEN_DIRECTORY_HEADER = "Chosen Mode: {0}"
SCREEN_DIRECTORY_TEXT = """Please enter a directory.
You may use the working directory by entering a period.
You can also choose a child directory by starting with a slash."""
SCREEN_DIRECTORY_ERROR = "The directory you entered is invalid.\nYour previous choice: {0}"

SCREEN_TOTAL_HEADER = "Property Totals"
SCREEN_TOTAL_TEXT = "{0}: {1} files"

SCREEN_FAREWELL_HEADER = "Thank you!"
SCREEN_FAREWELL_TEXT = "Thank you for using Frontmatter-Edit. If you have any comments, questions, or concerns, feel free to send them to wjplachno@gmail.com."