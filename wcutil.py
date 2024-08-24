"""
wcutil.py
Created by Will Plachno on 11/30/23

Woodchipper Utilities
An assortment of helpful functions and classes.

Includes:

- Classes:_________________________________________________________
- -- FlagFarm class: A simple dictionary wrapper for boolean flags
- -- Debug class: A set of debugging tools

- Globals:_________________________________________________________

- Functions:_______________________________________________________
- -- valid_directory_at: Returns whether the path is a directory,
        safely defaulting to False.
- -- text_has_paths: Checks whether the given string has any of the
        common path delimiters.
- -- tail_matches_token: Checks whether the end of the given string
        matches the given token. Useful for checking file types.
- -- time_stamp:
"""
import pathlib
from datetime import datetime

class FlagFarm:
    def __init__(self, list_of_flag_keys):
        self.keys = list_of_flag_keys
        self.values = dict((key, False) for key in self.keys)

    def __setitem__(self, key, value):
        if self.has_flag(key):
            self.values[key] = value

    def __getitem__(self, item):
        if self.has_flag(item):
            return self.values[item]
        return None

    def __len__(self):
        return len(self.keys)

    def has_flag(self, key):
        return key in self.keys

    def active_flags(self):
        return [key for key in self.keys if self.values[key]]

    def active_count(self):
        count = 0
        for key in self.keys:
            if self.values[key]:
                count += count

    def activate(self, key):
        if self.has_flag(key):
            self.values[key] = True

class Debug:
    def __init__(self, message_handler=print, active=False):
        self.is_active = active
        self.handlers = [message_handler]

    def scribe(self, message):
        if self.is_active:
            for handler in self.handlers:
                handler(message)

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False

    def set(self, active_as_boolean=True):
        self.is_active = active_as_boolean

    def add_message_handler(self, new_handler):
        self.handlers.append(new_handler)


def valid_directory_at(directory_path):
    """
    Determines whether the path points to an actual directory
    :param directory_path: A path, hopefully a directory
    :return: Whether path actually leads to a directory.
    """
    try:
        if directory_path and pathlib.Path(directory_path).is_dir():
            return True
    except Exception:
        return False
    return False

def text_has_paths(text):
    """
    Checks a string for any path delimiters
    :param text: The string to check for path delimiters
    :return: Whether text contains path delimiters
    """
    has_paths = False
    try:
        text.index('/')
        has_paths = True
    finally:
        try:
            text.index('\\')
            has_paths = True
        finally:
            return has_paths

def tail_matches_token(text, token):
    token_size = len(token)
    if token_size > 0:
        return text[-token_size:] == token


preferred_time_format = "%m%d%y:%H:%M:%S"
def time_stamp(time=None):
    """
    Returns the current time in the format I like.
    :return: 12/24/23:7:42:22 = 12/24 of 2023 at 7:42 and 22 seconds,
    but the current time.
    """
    if time:
        return datetime(time).strftime(preferred_time_format)
    return datetime.now().strftime(preferred_time_format)

onSynonyms = list(("on","true","1","yes","t","y","+","active","positive", "a", "p"))
def str2Bool(rawText:str):
    text = rawText.lower()
    if text in onSynonyms:
        return True
    return False

def bool2Str(value:bool, include_color:bool=False):
    pretext = '\033[0;32m' if value else '\033[0;31m'
    text = "on" if value else "off"
    return pretext+text+'\033[0m' if include_color else text

def run_on_sorted_list(target_list, function_given_item):
    """
    Sorts the list, then runs the function on each item.
    :param target_list: The list to be sorted
    :param function_given_item: The function to run on each item.
    :return: None
    """
    sorted_list = sorted(target_list)
    for list_item in sorted_list:
        function_given_item(list_item)

def decipher_command_line(arguments, flags):
    """
    Gets the target directory paths, either as a command line argument
    or the working directory. Also deciphers the rest of the command
    line arguments for flags like VERBOSE and HISTORY
    :return: A list of directory paths
    """
    # Decipher the command line arguments
    target_directories = []
    for cl_argument in arguments[1:]:
        arg_as_flag = cl_argument.upper()
        if flags.has_flag(arg_as_flag):
            flags.activate(arg_as_flag)
        else:
            target_directories.append(cl_argument)
    if len(target_directories) < 1:
        target_directories.append(pathlib.Path().resolve())
    return target_directories

class WoodChipperFile:

    def __init__(self, filePath):
        self.path = pathlib.Path(filePath)
        self.name = self.path.name
        self.text = list(())
        if not self.path.exists():
            file = open(self.path, 'x')
            file.close()

    def read(self):
        with (open(self.path, "r")
              as text_file):
            self.text = list(text_file)

    def write(self):
        with (open(self.path, "w")
              as text_file):
            for text_line in self.text:
                text_file.write(text_line)

    def clear(self):
        self.text = list (())

    def append_line(self, text):
        fixedText = text
        if fixedText[-1] != '\n':
            fixedText = fixedText + '\n'
        self.text.append(fixedText)

    def insert_line(self, index, text):
        fixedText = text
        if fixedText[-1] != '\n':
            fixedText = fixedText + '\n'
        self.text.insert(index, fixedText)

    def run_per_line(self, _func):
        retVal = True
        for rawLine in self.text:
            line = rawLine
            if line[-1] == '\n':
                line = line[:-1]
            retVal = retVal and _func(line)
        return retVal

    def __str__(self):
        return self.name + " (" + self.path + "): " + len(self.text) + " items"

class WoodchipperSettingsFile:
    def __init__(self):
        self.path = pathlib.Path.home() / ".wcp_Settings.txt"
        self.file = WoodChipperFile(self.path)
        self.keys = set(())
        self.values = {}

    def load(self):
        self.file.read()
        self.file.run_per_line(self._add_from_file)
        if "debug" not in self.keys:
            self.set_key("debug","off")

    def save(self):
        self.file.clear()
        for key in self.keys:
            self.file.append_line(key+":"+self.values[key])
        self.file.write()


    def __getitem__(self, item):
        return self.values[item]

    def __setitem__(self, key, value):
        self.set_key(key,value)

    def set_key(self, key, value):
        self.keys.add(key)
        self.values[key] = value

    def get_key(self, key):
        return self.values[key]

    def _add_from_file(self, text):
        linePieces = text.split(':')
        self.set_key(linePieces[0], linePieces[1])
        return True

    def get_debug(self):
        return self["debug"] == "on"

    def flip_debug(self):
        debug = self["debug"]
        if debug == "off":
            self["debug"] = "on"
        else:
            self["debug"] = "off"

    def is_defined(self, key):
        return key in self.keys

    def get_or_default(self, key, default="undefined"):
        if self.is_defined(key):
            return self[key]
        else:
            self.set_key(key, default)
            self.save()
