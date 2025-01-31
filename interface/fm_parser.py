# fm_parser.py
# Written by: Will Plachno
# Created: 01/11/2025
# Version: 0.0.1.006
# Last Changed: 01/30/2025

from os import getcwd
from pathlib import Path

from utilities.wcparser import CLParser as WCParser
from utilities.wcutil import tail_matches_token as check_file_type
from constants import MODE

def build_parser():
    parser = WCParser("frontmat",
                      version="0.0.2.001",
                      description="Allows for mass edits of YAML Frontmatter in Obsidian Markdown directories.",
                      footer="Created by Will Plachno. Copyright 2025.")
    parser.add_argument("mode", choices=[MODE.SHOW, MODE.ADD, MODE.REMOVE, MODE.SET, MODE.CHANGE, MODE.SUMMARIZE], default=MODE.SUMMARIZE,
                        description="The mode we are operating in.\n  summarize - Shows all keys in the frontmatter of target files.\n  show - Shows all values associated with the given Key and what files they exist in.\n  add - Adds a new property to target files without editing it if it already exists.\n  set - Adds the property to each target file and sets all instances of the key to the given value.\n  change - Modifies any existing occurrences of the given key to the given value.\n  remove - Removes a property from the target files.\n")
    parser.add_argument("key", description="The target key to be analyzed.")
    parser.add_argument("value", description="The value for the given key.")
    parser.add_argument("targets", nargs="+",
                        description="A set of filenames that exist in the given directory that should be the only files considered 'targets'.")
    parser.add_argument("--directory", "-directory", "-d", "-dir", default=getcwd(), shaper=path_shaper, nargs=1,
                        description="A path to a directory that should be used for this script call.")
    parser.add_argument("--filter", "-filter", "-f", nargs=1,
                        description="Filters the Add, Set, Update, and Remove modes for files with a matching property. Should be formatted as \"key:value\".")
    return parser

def post_parser(request):
    target_paths = determine_target_paths(request)
    add_if_necessary, change_if_existing = determine_set_type(request)
    setattr(request, "filter_property", translate_filter(request.filter))
    setattr(request, "target_paths", target_paths)
    setattr(request, "add_if_necessary", add_if_necessary)
    setattr(request, "change_if_existing", change_if_existing)
    return request

def determine_target_paths(request):

    # check Directory validity and get file paths
    root = Path(request.directory)
    if not root.is_dir():
        print(f"The path {root.resolve()} did not resolve to a directory.")
        exit(1)
    md_files = filter(lambda x: markdown_check(x.name), root.iterdir())
    target_paths = list(map(path_shaper, md_files))

    # compile and institute targets
    targets = list(())
    if request.key and request.mode == MODE.SUMMARIZE:
        targets.append(request.key)
    if request.value and (request.mode == MODE.SUMMARIZE or request.mode == MODE.SHOW):
        targets.append(request.value)
    targets.extend(request.targets)
    if len(targets) > 0:
        target_paths = list(filter((lambda dir_path: dir_path.name in targets), target_paths))

    return target_paths

def determine_set_type(request):
    add_if_necessary = False
    change_if_existing = False
    if request.mode == MODE.ADD:
        add_if_necessary = True
    elif request.mode == MODE.CHANGE:
        change_if_existing = True
    elif request.mode == MODE.SET:
        add_if_necessary = True
        change_if_existing = True
    return add_if_necessary, change_if_existing

def translate_filter(filter_string):
    if filter_string:
        pieces = filter_string.split(':')
        key = pieces[0]
        value = pieces[1]
        return key, value
    return None


def path_shaper(text):
    return Path(text).resolve()

def markdown_check(text):
    if check_file_type(text, ".md"):
        return True
    return False

def markdown_path_shaper(text):
    if markdown_check(text):
        return Path(text).resolve()
    print(f"File {text} is not a markdown file.")
    exit(1)