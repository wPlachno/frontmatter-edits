import sys
import pathlib
import wcutil
from fmActor import create_actor
import constants as S
import wcTerminalIO as T

flag_list = list((S.MODE_ADD, S.MODE_SET, S.MODE_CHANGE, S.MODE_REMOVE, S.MODE_TOTAL, S.MODE_HELP))
flags = wcutil.FlagFarm(flag_list)
debug = wcutil.Debug(active=True)
dbg = debug.scribe
class CommandLineInformation:
    def __init__(self):
        self.success = False
        self.type = S.EMPTY
        self.property_text = S.EMPTY
        self.property_key = S.EMPTY
        self.property_value = S.EMPTY
        self.directory = None
        self.directory_text = S.EMPTY
        self.error = S.EMPTY

def show_error(error):
    error_title = error.split(S.COLON)[0]
    T.ScreenDisplay(error, header=error_title, pause=True)

def show_help():
    T.ScreenDisplay(S.SCREEN_HELP_TEXT, header=S.SCREEN_HELP_HEADER, pause=True)

def show_directory_picker():
    directory_screen = T.ScreenDirectory()
    directory_screen.display()
    if directory_screen.success:
        return directory_screen.directory_path
    return None

def show_interactive():
    class MenuItem:
        def __init__(self, choice, type):
            self.choice = choice
            self.type = type
    menu_items = [
        MenuItem(S.MENU_CHOICE_ADD,S.MODE_ADD),
        MenuItem(S.MENU_CHOICE_SET,S.MODE_SET),
        MenuItem(S.MENU_CHOICE_CHANGE,S.MODE_CHANGE),
        MenuItem(S.MENU_CHOICE_REMOVE,S.MODE_REMOVE),
        MenuItem(S.MENU_CHOICE_TOTAL,S.MODE_TOTAL)
    ]
    T.ScreenDisplay(S.SCREEN_WELCOME_TEXT, header=S.SCREEN_WELCOME_HEADER, pause=True).display()
    directory_path = show_directory_picker()
    menu_header = directory_path
    menu_choice = S.MENU_CHOICE_INVALID
    while menu_choice != S.MENU_CHOICE_QUIT:
        menu_screen = T.ScreenMenu(S.SCREEN_MENU_TEXT, header=menu_header)
        if not menu_screen.display():
            break
        menu_choice = menu_screen.choice
        if menu_choice != S.MENU_CHOICE_QUIT:
            if menu_choice == S.MENU_CHOICE_DIR_SET:
                directory_path = show_directory_picker()
                menu_header = S.DIRECTORY_CHANGED.format(directory_path)
            elif menu_choice == S.MENU_CHOICE_DIR_CLEAR:
                directory_path = None
                menu_header = S.DIRECTORY_NONE
            else:
                directory = directory_path
                if not directory_path:
                    header = S.SCREEN_DIRECTORY_HEADER.format(menu_items[menu_choice].type)
                    directory_screen = T.ScreenPrompt(S.SCREEN_DIRECTORY_TEXT, header=header)
                    if directory_screen.add_validator(validate_folder).display():
                        directory = directory_screen.reply
                header = S.SCREEN_PROPERTY_HEADER.format(menu_items[menu_choice].type, str(directory))
                if menu_choice != S.MENU_CHOICE_TOTAL:
                    property_screen = T.ScreenPrompt(S.SCREEN_PROPERTY_TEXT, header=header)
                    if property_screen.add_validator(T.Create_String_Validator(lambda s: len(s.split(S.COLON)) == 2)).display():
                        reply_property = property_screen.reply.strip()
                        actor = create_actor(directory, reply_property, menu_items[menu_choice].type)
                        actor.run()
                        menu_header = actor.summarize_short()
                        T.ScreenDisplay(actor.summarize(),header=menu_header).display()
                else:
                    actor = create_actor(directory, S.FAKE_PROPERTY, menu_items[menu_choice].type)
                    actor.run()
                    T.ScreenDisplay(actor.summary, pause=True).display()
    T.ScreenDisplay(S.SCREEN_FAREWELL_TEXT, header=S.SCREEN_FAREWELL_HEADER).display()


def format_path(path_raw):
    path = path_raw.strip()
    if path[0] == S.FORWARDSLASH or path[0] == S.BACKSLASH:
        return pathlib.Path().resolve() / path[1:]
    return path

def validate_folder(screen, path_raw):
    screen.reply = format_path(path_raw)
    screen.warning = S.SCREEN_DIRECTORY_ERROR.format(screen.reply)
    if wcutil.valid_directory_at(pathlib.Path(screen.reply)):
        screen.reply = pathlib.Path(screen.reply)
        return True
    else:
        return False
def decipher_command_line(arguments, flags):
    """
    Gets the target directory paths, either as a command line argument
    or the working directory. Also deciphers the rest of the command
    line arguments for flags like VERBOSE and HISTORY
    :return: A list of directory paths
    """
    # Decipher the command line arguments
    cl = CommandLineInformation()

    if len(arguments) == 2 and arguments[1].strip().upper() == S.MODE_HELP:
        cl.success = True
        cl.type = S.MODE_HELP
        return cl

    if len(arguments) == 1:
        cl.success = True
        cl.type = S.MODE_MENU
        return cl

    if len(arguments) < 3:
        cl.error = S.ERROR_NOT_ENOUGH_ARGUMENTS
        return cl
    cl.type = arguments[1].strip().upper()
    if cl.type not in flag_list:
        cl.error = S.ERROR_INVALID_COMMAND
        return cl

    cl.property_text = arguments[2]
    property_split = cl.property_text.split(S.COLON)
    if len(property_split) < 2:
        cl.error = S.ERROR_INVALID_PROPERTY
        return cl
    cl.property_key = property_split[0].strip()
    cl.property_value = property_split[1].strip()

    cl.directory = pathlib.Path().resolve()

    if len(arguments) > 3:
        cl.directory_text = format_path(arguments[3])
        if wcutil.valid_directory_at(pathlib.Path(cl.directory_text)):
            cl.directory = pathlib.Path(cl.directory_text)
        else:
            cl.error = S.ERROR_INVALID_DIRECTORY
            return cl
    cl.success = True
    return cl

cl = decipher_command_line(sys.argv, flags)
if not cl.success:
    show_error(cl.error)
    exit(1)
if cl.type == S.MODE_HELP:
    show_help()
    exit(0)
if cl.type == S.MODE_MENU:
    show_interactive()
    exit(0)
else:
    actor = create_actor(cl.directory, cl.property_text, cl.type)
    actor.run()
    if cl.type == S.MODE_TOTAL:
        print(actor.summary)
