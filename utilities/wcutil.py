"""
wcutil.py
Created by Will Plachno on 11/30/23
Version: 0.0.1.013
Last Changes: 01/15/2025

Woodchipper Utilities
An assortment of helpful functions and classes.

Includes:

- Classes:_________________________________________________________
- -- Debug class: A set of debugging tools
- -- FlagFarm class: A simple dictionary wrapper for boolean flags
- -- WoodchipperFile: A simple class for reading in the lines of a
        file into an array.
- -- WoodchipperSettingsFile: A class for handling a settings file.

- Functions:_______________________________________________________
- -- bool2Str: Converts a bool into either "on" or "off". Passing
        true will wrap the string in a terminal color code, on as
        green, off as red.
- -- convert_to_array: Takes whatever is passed in and wraps it in
        a list if it wasn't already a list.
- -- decipher_command_line_arguments: Given a list of strings, this
        function checks the list for the flags of a flag farm.
- -- process_str_array_new_lines: Given a list of strings, breaks
        up any strings with new lines into two strings.
- -- run_on_sorted_list: Sorts a list and then runs on each item
        a given function.
- -- str2Bool: Converts a string to a boolean, defaulting to false,
        but marking true if lower() exists in onSynonyms.
- -- text_has_paths: Checks whether the given string has any of the
        common path delimiters.
- -- tail_matches_token: Checks whether the end of the given string
        matches the given token. Useful for checking file types.
- -- time_stamp: Gets the current time in our preferred format, or
        converts a datetime object into a string with our preferred
        format.
- -- valid_directory_at: Returns whether the path is a directory,
        safely defaulting to False.

Wishlist:
- -- WoodchipperFile: Allow for usage of the wcf as an array of
        lines, add two functions which strip or add new lines,
        and add map-filter-reduce functions. As a reminder:
        Map - transforms a collection item by item, returning
            the transformations as a separate collection
        Filter - Runs a function on each item of a collection,
            creating a new collection of items for which the
            function returns true.
        Reduce - Returns a sum of the return values of a function
            run over each item in a collection.
- -- WoodchipperProfileFile: A WoodchipperSettingsFile specifically
        for user account settings across different programs. Also,
        separate it out and leave WoodchipperSettingsFile for a
        simple, non-biased settings file.
- -- Woodchipper_General.py: A catch-all file for random funcs and
        such. Go ahead and move everything from wcutil.py to this,
        then import into wcutil.py as Utility
- -- Woodchipper_TerminalIO.py: A separate file to which we can
        push the terminal printing stuff and the color consts.
        Should still be imported by wcutil as Display. Use the
        file frontmat/WCTerminalIO.py as a starter.
- -- Woodchipper_FlagFarm.py: A separate file to which we can move
        the FlagFarm class and any required functions.
- -- Woodchipper_Strings.py: A separate file to which we can move
        all string functionality, including str2Bool, bool2Str,
        process_str_array_new_lines, text_has_paths, and
        tail_matches_token.
- -- Woodchipper_FileIO.py: A separate file to which we can move
        the generic file i/o functionality - WoodchipperFile,
        WoodchipperSettingsFile
- -- Woodchipper_Debug.py: A separate file to which we can move
        the Debug class and any functions it relies on.
- -- Woodchipper_Profile.py: A separate file to which we can move
        an all-in-one solution: a WoodchipperProfileFile, easy
        Debug, and can easily be plugged into whatever cli parser
        your solution uses.
- -- Woodchipper_Constants.py: A separate file to which we can move
        A way to compile a bunch of widely used constants with a
        constants file, constants.txt in the same folder. We can use
        WoodchipperSettingsFile, then use setattr to load it into a
        Constants object.

"""
import pathlib
from datetime import datetime
from functools import reduce
from pathlib import PosixPath
from types import SimpleNamespace

import utilities.wcconstants as s

""" CLASSES ------------------------------------------------------ """

""" Debug
#
#       A class for handling debug statements. Keeps an internal flag
#   for whether debug statements are currently active. When tasked to 
#   print a debug statement, the class can support multiple handlers,
#   though it defaults to a standard cl print.
#
### Usage
#
#       Generally, I start my projects by setting up my debugging. To
#   do so, you first need to instantiate the class, passing whether
#   the debug statements should be handled or ignored. If you need to
#   setup alternate debug message handlers, you can do so after init
#   using the add_message_handler. 
#       I like to setup an alias for the debug message, making the 
#   call as short as `dbg()` instead of `debug.scribe()`.
#       If using a WoodchipperSettingsFile, you can pass the current
#   debug flag into the instantiation of the debug object. You can see
#   all of this on display in the following code snippet:
#
#   0   settings = wcutil.WoodchipperSettingsFile()
#   1   settings.load()
#   2   debug = wcutil.Debug(active=(settings.get_debug()))
#   3   dbg = debug.scribe
#
### Methods
#
#   # Attribute Controls
#   activate() - turns on debugging.
#   deactivate() - turns off debugging.
#   set(value) - turns debugging to the value, either True or False 
#
#   # Core
#   scribe(message) - passes the message to the message handlers.
#
#   # Auxiliary
#   add_message_handler(handler) - Sets up a new handler for 
#       scribing messages.
"""
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

""" FlagFarm
#
#       Many command-line accessible scripts support command-line
#   flags of some sort. The FlagFarm class is designed to aid in
#   these operations by providing a singleton per script instance
#   for tracking them.
#
### Usage
#
#       The FlagFarm must first be given a list of flags to check for. 
#   Note that the actual checking happens outside of the class. I suggest
#   making the flag list all upper or lowercase for easier comparisons.
#       You can check if an argument is a flag be passing it to has_flag,
#   then activate the flag using activate. The flags can be individually
#   accessed using flagFarm[flag_key]. You can also check how many flags
#   are currently active using active_count and get a list of the active
#   flags using the list provided by active_flags.
#
### Methods
#
#   # Attribute Controls
#   activate(key) - turns on the flag.
#   active_count() - returns the number of active flags
#   active_flags() - returns a list of active flags
#
#   # Auxiliary
#   __get_item__ - returns the value of a given flag, or None if
#       the flag is not tracked by this flagFarm.
#   __set_item__ - If the flag is tracked by this flagFarm, sets
#       its active status to the given value.
#   __len__ - Counts how many flags are tracked by this flagFarm.
"""
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

    def activate(self, key):
        if self.has_flag(key):
            self.values[key] = True

    def active_count(self):
        count = 0
        for key in self.keys:
            if self.values[key]:
                count += 1

    def active_flags(self):
        return [key for key in self.keys if self.values[key]]

    def has_flag(self, key):
        return key in self.keys

class WoodchipperNamespace(SimpleNamespace):
    def __init__(self, name=None):
        SimpleNamespace.__init__(self)
        self._name = name if name else "WoodchipperNamespace"

    def add(self, key, value):
        setattr(self, key, value)

    def __str__(self):
        out_str = s.clr(self._name, s.COLOR.SUPER) + ": { "
        if len(self.__dict__) > 0:
            for key in self.__dict__:
                if key != "_name":
                    value_str = str(self.__dict__[key]).replace("\n", "\n\t")
                    out_str += f"\n\t{s.clr(key, s.COLOR.SIBLING)}: {value_str}"
            out_str += "\n"
        out_str += "}"
        return out_str

class WoodchipperDictionary:
    def __init__(self, default_value=None):
        self.values = dict()
        self.default = default_value
        self.values["default"] = self.default

    def keys(self):
        return filter( (lambda key: key != "default"), self.values.keys())

    def __getitem__(self, key="default"):
        try:
            return self.values[key]
        except KeyError:
            return self.default

    def __setitem__(self, key, value):
        if key.lower() == "default":
            self.default = value
        self.values[key] = value

    def __iter__(self):
        class WoodchipperDictionaryIterator:
            def __init__(self, woodchipper_dictionary):
                self.dict = woodchipper_dictionary
                self.keys = list(woodchipper_dictionary.values.keys())
                self.length = len(self.keys)
                self.index = -1
                self.key = None
                self.value = None
                if not self.find_next():
                    raise StopIteration

            def __next__(self):
                if not self.find_next():
                    raise StopIteration
                return self.value

            def find_next(self):
                self.index += 1
                if self.index > self.length:
                    return False
                elif self.index == self.length:
                    self.set("default")
                    return True
                else:
                    key = self.keys[self.index]
                    if key == "default":
                        return self.find_next()
                    else:
                        self.set(key)
                        return True

            def set(self, key):
                self.key = key
                self.value = self.dict[self.key]
        return WoodchipperDictionaryIterator(self)

class WoodchipperListDictionary(WoodchipperDictionary):
    def __init__(self, allow_duplicates=False):
        WoodchipperDictionary.__init__(self)
        self.allow_duplicates = allow_duplicates

    def mark(self, key, value):
        if not key in self.values:
            self.values[key] = list(()).append(value)
        elif self.allow_duplicates:
            self.values[key].append(value)

    def compile(self):
        return list(map(lambda key: ( key, self.values[key] ), sorted(self.values.keys())))

class WoodchipperHeatMap:
    def __init__(self):
        self._heat = WoodchipperDictionary(0)

    def mark(self, key):
        self._heat[key] = self._heat[key] + 1

    def compile(self):
        heat_map = list( map( lambda property_key: ( property_key, self._heat[property_key] ), sorted(self._heat.keys())) )
        total = reduce( lambda first_item, second_item: ("", first_item[1] + second_item[1]), heat_map )[1]
        return heat_map, total

class WoodchipperHeatMapDictionary:
    def __init__(self):
        self._keys = WoodchipperDictionary()

    def mark(self, key, value):
        if self._keys[key]:
            self._keys[key].mark(value)
        else:
            new_heat = WoodchipperHeatMap()
            new_heat.mark(value)
            self._keys[key] = new_heat

    def compile(self):
        heat = list(())
        total = 0
        for key in sorted(self._keys.keys()):
            key_heat, key_total = self._keys[key].compile()
            total += key_total
            heat.append((key, key_total, key_heat))
        return heat, total





""" WoodchipperFile
#
#       This class is a lightweight wrapper for common file functions,
#   particularly making the read/write more atomic; using this class
#   guarantees that logic is not being done while the file is actually
#   open. We read the file into memory, free it up, do any logic, then
#   call the write function to save it back to the file. 
#
### Usage
#
#       When using WoodchipperFile objects, you pass the path into the
#   initialization of the object, then call read() to pull the file
#   contents as a list into wcf.text, do whatever you need with the 
#   lists, then save the changes by calling write().
#       Note that all lines of text end in a new line character. 
#
### Methods
#
#   # Attribute Controls
#   exists() - checks whether the file exists
#
#   # Core
#   read() - Pulls the contents from the file into the text member
#   write() - Saves the current list into the file.
#
#   # File Editing
#   append_line(text) - Adds a line of text at the end of the file.
#   clear() - Clears the in memory text list.
#   insert_line(index, text) - Inserts a line of text at the index,
#       pushing any later lines 1 index higher, including the text
#       previously at the index this new line gets added at. 
#   run_per_line(_func) - Runs the _func callable on each line of 
#       the file after removing the new line from each. The _func
#       callable is expected to return a boolean. The run_per_line
#       function which also returns a boolean, will only return 
#       true if every call to _func returned true.
#
#   # Auxiliary
#   __str__ - returns a string with the file name, file path, 
#       and the number of lines in the file.
"""
class WoodChipperFile:

    def __init__(self, file_path, auto_create=True):
        self.path = pathlib.Path(file_path)
        self.name = self.path.name
        self.text = list(())

        if auto_create and not self.path.exists():
            file = open(self.path, s.FILE_IO.EXCLUSIVE_CREATION)
            file.close()

    def read(self):
        with (open(self.path, s.FILE_IO.READ)
              as text_file):
            self.text = list(text_file)

    def write(self):
        with (open(self.path, s.FILE_IO.WRITE)
              as text_file):
            for text_line in self.text:
                text_file.write(text_line)

    def clear(self):
        self.text.clear()

    def exists(self):
        return self.path.exists()

    def last_modified(self):
        return pathlib.Path(self.path).stat().st_mtime if self.exists() else 0

    def file_extension(self):
        return str(self.path).split('.')[-1]

    def copy_from(self, other_file):
        if other_file.text:
            self.text = list(other_file.text)

    def append_line(self, text):
        fixed_text = text
        if fixed_text[-1] != s.KEY.NL:
            fixed_text = fixed_text + s.KEY.NL
        self.text.append(fixed_text)

    def insert_line(self, index, text):
        fixed_text = text
        if fixed_text[-1] != s.KEY.NL:
            fixed_text = fixed_text + s.KEY.NL
        self.text.insert(index, fixed_text)

    def run_per_line(self, _func):
        return_value = True
        for rawLine in self.text:
            line = rawLine
            if line[-1] == s.KEY.NL:
                line = line[:-1]
            return_value = return_value and _func(line)
        return return_value

    def find_tag(self, tag):
        for line in self.text:
            if tag in line.lower():
                start_idx = line.lower().find(tag) + len(tag)
                tag_value = line[start_idx:].split()[0]
                return tag_value
        return "None"

    def replace_tag(self, tag, value, add_if_not_found_at_line=-1):
        found = False
        for index in range(0, len(self.text)):
            line = self.text[index]
            if tag in line.lower():
                start_idx = line.lower().find(tag) + len(tag)
                self.text[index] = line[:start_idx] + value + '\n'
                return index
        if found == False and add_if_not_found_at_line != -1:
            line_prefix = '#'
            line_suffix = ''
            line_str = f"{line_prefix} {tag}{value} {line_suffix}\n"
            self.text.insert(add_if_not_found_at_line, line_str)
            return add_if_not_found_at_line
        return -1

    def __str__(self):
        return f"{self.name} ({self.path}): {len(self.text)} lines"


""" WoodchipperListFile
#
#       A version of WoodchipperFile for serializing a set of items,
#   where the order does not matter.
#
### Usage
#
#       Use this like the WoodchipperFile, but keep in mind that each
#   line is intended to be unique if wcf.unique is true. 
#
### Methods
"""
class WoodchipperListFile(WoodChipperFile):
    def __init__(self, file_path, auto_create=True, unique=True):
        WoodChipperFile.__init__(self, file_path, auto_create)
        self.unique = unique

    def __getitem__(self, item):
        return self.text[item][:-1]

    def __setitem__(self, key, value):
        self.text[key] = str(value) + s.KEY.NL

    def  __contains__(self, item):
        text = str(item) + s.KEY.NL
        return text in self.text

    def __len__(self):
        return len(self.text)

    def __str__(self):
        text = s.KEY.EMPTY
        for line in self.text:
            text = text + (line[:-1] + s.KEY.CD)
        return text[:-2]

    def add(self, value):
        text = str(value) + s.KEY.NL
        if (not self.unique) or (text not in self.text):
            self.text.append(text)
            return True
        return False

    def remove(self, value):
        text = str(value) + s.KEY.NL
        found = text in self.text
        self.text.remove(text)
        return found


""" WoodchipperSettingsFile
#
#       A version of WoodchipperFile for serializing a set of items,
#   where the order does not matter.
#
### Usage
#
#       Use this like the WoodchipperFile, but keep in mind that each
#   line is intended to be unique if wcf.unique is true. 
#
### Methods
"""
class WoodchipperDictionaryFile:
    def __init__(self, path="None"):
        self.path = path
        if self.path == "None":
            self.path = pathlib.Path.home() / s.FILE_NAME_SETTINGS
        self.file = WoodChipperFile(self.path)
        self.keys = set(())
        self.values = {}

    def load(self):
        self.file.read()
        self.file.run_per_line(self._add_from_file)
        if s.DEBUG not in self.keys:
            self.set_key(s.DEBUG, s.OFF)

    def save(self):
        self.file.clear()
        for key in self.keys:
            self.file.append_line(key + s.KEY.SDL + self.values[key])
        self.file.write()


    def __getitem__(self, item):
        try:
            return self.values[item]
        except KeyError:
            return None

    def __setitem__(self, key, value):
        self.set_key(key,value)

    def __str__(self):
        out_string = "{ "
        for key in self.keys:
            out_string += f"{key}: {self.values[key]}, "
        out_string = out_string[:-2] + " }"
        return out_string

    def set_key(self, key, value, auto_save=False):
        self.keys.add(key)
        self.values[key] = value
        if auto_save:
            self.save()

    def get_key(self, key):
        return self.values[key]

    def _add_from_file(self, text):
        broken_line = text.split(s.KEY.SDL)
        _key = broken_line[0]
        _val = broken_line[1]
        self.set_key(_key, _val)
        return True

    def is_defined(self, key):
        return key in self.keys

    def get_or_default(self, key, default=s.UNDEFINED):
        if self.is_defined(key):
            return self[key]
        else:
            self.set_key(key, default)
            self.save()


""" WoodchipperSettingsFile
#
#       A global settings file across all Woodchipper scripts
#
### Usage
#
#       Use this like the WoodchipperFile, but keep in mind that each
#   line is intended to be unique if wcf.unique is true. 
#
### Methods
"""
class WoodchipperSettingsFile(WoodchipperDictionaryFile):
    def __init__(self):
        WoodchipperDictionaryFile.__init__(self)
        self.load()
        self._check_variables()
        self.verbosity = int(self[s.VERBOSE])

    def _check_variables(self):
        any_missing = False
        profile_vars = [(s.VERBOSE, str(s.Verbosity.NORMAL))]
        for var_key, var_val in profile_vars:
            if not var_key in self.keys:
                any_missing = True
                self.set_key(var_key, var_val)
        if any_missing:
            self.save()
        return any_missing

    def get_debug(self):
        return self[s.DEBUG] == s.ON

    def flip_debug(self, wanted_value=None):
        new_value = wanted_value
        value_string = self[s.DEBUG]
        if wanted_value:
            value_string = (s.OFF if wanted_value == False else s.ON)
        else:
            if value_string == s.OFF:
                value_string = s.ON
            else:
                value_string = s.OFF
        self.set_key(s.DEBUG, value_string, True)
        return new_value

    def get_verbosity(self):
        return self.verbosity

    def set_verbosity(self, wanted_value):
        self.verbosity = wanted_value
        self[s.VERBOSE] = str(self.verbosity)

    def check_parser(self, argparse_args):
        proceed = not argparse_args.config
        test = None
        out_string = None
        if not argparse_args.verbosity is None:
            verbosity = int_from_string(argparse_args.verbosity)
            if verbosity is not None:
                self.set_verbosity(verbosity)
            else:
                out_string = s.CL_TASK.CONFIG_ERROR.format("Verbosity could not be interpreted as an integer value.")
        if not argparse_args.debug is None:
            debug = argparse_args.debug
            self.flip_debug(wanted_value=debug)
        if not argparse_args.test is None:
            test = argparse_args.test
            # Note: We can test wcutil here by checking test, doing the test, and returning the result
            # Otherwise, we can assume they are testing something outside wcutil
            proceed = False
        self.save()
        argparse_args.verbosity = self.verbosity
        argparse_args.debug = self.get_debug()
        if not out_string:
            out_string = s.CL_TASK.MODE_CONFIG.format(s.VERBOSE, argparse_args.verbosity)
            out_string += s.CL_TASK.MODE_CONFIG.format(s.DEBUG, argparse_args.debug)
        return proceed, out_string, test

    @staticmethod
    def setup_argparse_parser_with_config(parser):
        parser.add_argument("-c", "--config", default=False, hide=True)
        parser.add_argument("--verbosity", shaper=int_from_string, nargs=1)
        parser.add_argument("-d", "--debug", shaper=bool_from_user, nargs=1)
        parser.add_argument("--test", nargs=1)

    @staticmethod
    def get_test_string(text):
        if text.startswith(s.TEST_TAG):
            return text[len(s.TEST_TAG):]
        return None

    def print(self, text, verbosity=s.Verbosity.NORMAL):
        if self.get_debug() or self.verbosity >= verbosity:
            print(text)


""" FUNCTIONS ---------------------------------------------------- """
def bool_from_user(raw_text:str):
    text = raw_text.lower()
    if text in s.ON_SYNONYMS:
        return True
    return False

def colorize_path(path):
    parent = ""
    name = ""
    if type(path) == str:
        pieces = path.split('/')
        name = pieces[-1]
        parent = path[:-len(name)]
    elif type(path) == PosixPath:
        parent = str(path.parent)
        name = path.name
    return f'{s.clr(parent, s.COLOR.PATH_PARENT)}/{s.clr(name, s.COLOR.PATH_NAME)}'



def convert_to_array(target):
    """
    Takes whatever is passed in and returns it inside
    a list, unless it was already a list.
    :param target: anything
    :return: target inside a list or target if target is already a list.
    """
    if target.__class__ is list:
        return target
    return [target]

def decipher_command_line(arguments, flags: FlagFarm):
    """
    Deciphers the command line by parsing through arguments,
    affecting FlagFarm flags with each one, and adding it to
    a return value array if it does not match a flag.
    :return: A list of command line targets
    """
    # Decipher the command line arguments
    targets = []
    for cl_argument in arguments[1:]:
        arg_as_flag = cl_argument.lower()
        if flags.has_flag(arg_as_flag):
            flags.activate(arg_as_flag)
        else:
            targets.append(cl_argument)
    return targets

def int_from_string(text):
    try:
        return int(text)
    except (TypeError, ValueError):
        return None

def process_str_array_new_lines(target):
    """
    Given a list of strings, breaks up each new line
    into two separate strings
    :param target: A list of strings
    :return: a list of more strings with no new lines
    """
    new_lines = list(())
    for _string in target:
        for line in _string.split(s.KEY.NL):
            if len(line) > 0:
                new_lines.append(line)
    return new_lines


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


def string_from_bool(value:bool, include_color:bool=False):
    pretext = s.COLOR.ACTIVE if value else s.COLOR.CANCEL
    text = s.ON if value else s.OFF
    return pretext + text + s.COLOR.DEFAULT if include_color else text


def tail_matches_token(text, token):
    token_size = len(token)
    if token_size > 0:
        return text[-token_size:] == token


def text_has_paths(text):
    """
    Checks a string for any path delimiters
    :param text: The string to check for path delimiters
    :return: Whether text contains path delimiters
    """
    has_paths = False
    try:
        text.index(s.KEY.FS)
        has_paths = True
    finally:
        try:
            text.index(s.KEY.BS)
            has_paths = True
        finally:
            return has_paths


def time_stamp(time=None):
    """
    Returns the current time in the format I like.
    :return: 12/24/23:7:42:22 = 12/24 of 2023 at 7:42 and 22 seconds,
    but the current time.
    """
    if time and type(time) == datetime:
        return time.strftime(s.PREFERRED_TIME_FORMAT)
    return datetime.now().strftime(s.PREFERRED_TIME_FORMAT)


def valid_directory_at(directory_path):
    """
    Determines whether the path points to an actual directory
    :param directory_path: A path, hopefully a directory
    :return: Whether path actually leads to a directory.
    """
    try:
        if directory_path and pathlib.Path(directory_path).is_dir():
            return True
    except PermissionError:
        return False
    return False