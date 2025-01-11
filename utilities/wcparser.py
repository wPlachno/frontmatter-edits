# wcparser.py
# Created: 11/07/2024
# Version: 0.0.1.011
# Last Changed: 01/01/2025

import sys
from types import SimpleNamespace
from utilities import wcconstants as S

class CLP_Argument:
    def __init__(self, *name_or_tags, default=None, description="", optional=True, nargs=0, choices=None, hide=False, shaper=None):
        self.name = ""
        self.tags = []
        self.flag = False
        self.choices = choices
        self.default = default
        self.description = description
        self.hide = hide
        self.optional = optional
        self.nargs = nargs
        self.bucket = False
        self.shaper = shaper
        self.value = self.default
        if self.nargs == '+':
            self.nargs = 0
            self.bucket = True
            if not self.default:
                self.value = []
        if self.choices and not self.default:
            self.default = self.choices[0]
        self._decipher_name_or_tags(name_or_tags)

    def _decipher_name_or_tags(self, name_or_tags):

        self.tags = name_or_tags
        for tag in self.tags:
            if tag.startswith("-"):
                self.flag = True
            else:
                self.name = tag
            if tag.startswith("--"):
                self.flag = True
                self.name = tag[2:]
                break
        if self.name == "":
            self.name = "UNKNOWN"

    def set_value(self, value):
        if self.shaper:
            self.value = self.shaper(value)
        else:
            self.value = value

    def get_usage(self):
        usage_clr = S.COLOR.SUPER
        usage_str = ( "["+self.name+"]" if self.optional else self.name )
        if self.choices:
            usage_str = "{" + ", ".join(self.choices) + "}"
        elif self.flag:
            usage_str = ", ".join(self.tags)
            if self.optional:
                usage_str = "[" + usage_str + "]"
            usage_clr = S.COLOR.SIBLING
        return S.clr(usage_str, usage_clr)

    def print_help(self):
        return self.get_usage() + S.KEY.NL + S.KEY.DH + self.description + S.KEY.NL

    def check_arg(self, index, args):
        current_arg = args[index]
        if self.choices:
            if current_arg in self.choices:
                self.set_value(current_arg)
                return index+1
        elif current_arg in self.tags:
            if self.nargs == 0:
                self.set_value(True)
                return index + 1
            elif self.nargs == 1:
                if index+1 < len(args):
                    self.set_value(args[index+1])
                    return index+2
                else:
                    raise Exception(f"Arg {self.name} expects 1 arg to follow.")
            else:
                value = []
                offset = 1
                while offset <= self.nargs and offset + index < len(args):
                    value.append(args[index + offset])
                    offset += 1
                self.set_value(value)
                return index + offset
        return index

    def check_pos(self, index, pos):
        if self.flag or self.choices or index >= len(pos):
            return index
        if self.bucket:
            self.set_value(pos[index:])
            return len(pos)
        if self.nargs > 1:
            new_index = index + self.nargs
            self.set_value(pos[index:new_index])
            return new_index
        self.set_value(pos[index])
        return index+1

    def found(self):
        return self.value is None

class CLParser:
    def __init__(self, name=None, version=None, description=None, footer=None, include_usage=True):
        self.name = name
        self.version = version
        self.description = description
        self.footer = footer
        self.include_usage = include_usage
        self.args = []
        self.namespace = SimpleNamespace()

    def add_argument(self, *name_or_tags, default=None, description="", optional=True, nargs=0, choices=None, hide=False, shaper=None):
        self.args.append(CLP_Argument(*name_or_tags,
                     default=default,
                     description=description,
                     optional=optional,
                     nargs=nargs,
                     choices=choices,
                     hide=hide,
                     shaper=shaper))

    def parse_args(self, args):
        pos_args = []
        index = 1
        # First check args for flags and choices
        while index < len(args):
            found = False
            for arg in self.args:
                new_index = arg.check_arg(index, args)
                if not index == new_index:
                    found = True
                    index = new_index
                    break
            if not found:
                pos_args.append(args[index])
                index += 1
        # Now, deal with positional arguments
        if len(pos_args) > 0:
            target_arg = 0
            for arg in self.args:
                target_arg = arg.check_pos(target_arg, pos_args)
        return self._create_namespace()

    def _create_namespace(self):
        for arg in self.args:
            if not arg.found() and not arg.optional:
                sys.exit("Incorrect command line argument")
            setattr(self.namespace, arg.name, arg.value)
        if self.namespace.help:
            self.print_help()
            sys.exit(0)
        return self.namespace

    def print_help(self):
        print()
        # Usage line:
        # usage: [name] arg.usage
        if self.include_usage:
            print(self.get_usage())
        # Description
        if self.description:
            print(self.description)
        # Arguments:
        # positional arguments:
        # args.print_help(), self.flag == false
        print("Arguments: ")
        for arg in self.args:
            if not arg.flag and not arg.hide:
                print(arg.print_help())
        # Options:
        # options:
        # args.print_help(), self.flag == true
        print("Options: ")
        for arg in self.args:
            if arg.flag and not arg.hide:
                print(arg.print_help())
        # Footer
        if self.footer:
            print(self.footer)

    def print_version(self):
        if self.version:
            print(self.version)

    def get_usage(self):
        usage_str = "usage: "
        for arg in self.args:
            usage_str += arg.get_usage() + " "
        return usage_str

