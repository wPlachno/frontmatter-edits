# wccli.py
# Written By: Will Plachno
# Created: 12/14/24
# Version: 0.0.1.015
# Last Changed: 01/07/2025

from utilities.wcutil import WoodchipperSettingsFile as WCProfile
from utilities.wcprinter import WoodchipperToolkitPrinter as WCPrinter
from utilities.wcconstants import Verbosity, MODE

class WoodchipperCommandLineInterface:
    def __init__(self, printers, parser_build_function, post_parse_function=None):
        self.profile = WCProfile()
        self.parser = parser_build_function()
        self.post_parser = post_parse_function
        self._check_parser_for_mode()
        self.printer = WCPrinter(self.profile.verbosity)
        self.printers = printers
        self.request = None

    def process_request(self, args):
        self.request = self.parser.parse_args(args)
        if self.post_parser:
            self.request = self.post_parser(self.request)
        if self._check_config():
            self._print_profile(Verbosity.DEBUG)
            self.printer.nl(Verbosity.DEBUG)
            self._print_request(Verbosity.DEBUG)
            self.printer.nl(Verbosity.DEBUG)
        return self.request

    def display_results(self, results):
        self._print_response(results, Verbosity.DEBUG)
        self.printer.nl(Verbosity.DEBUG)
        printer_type = self.printers[results.mode]
        printer_obj = printer_type(results, self.printer)
        printer_obj.print()

    def _check_config(self):
        proceed, out_string, test = self.profile.check_parser(self.request)
        self.printer.verbosity = self.profile.verbosity
        if test:
            self.request.mode = MODE.TEST
            self.request.target = test
        elif not proceed:
            self.request.mode = MODE.NONE
            self.printer.pr(out_string, Verbosity.RESULTS_ONLY, new_line=False)
            return False
        return True

    def _print_profile(self, verbosity=Verbosity.DEBUG):
        self.printer.label("Profile", verbosity)
        for key in self.profile.keys:
            self.printer.kvp(key, self.profile[key], verbosity)

    def _print_request(self, verbosity=Verbosity.DEBUG):
        self.printer.label("Request", verbosity)
        req = vars(self.request)
        for key in req:
            self.printer.kvp(key, req[key], verbosity)

    def _print_response(self, response, verbosity=Verbosity.DEBUG):
        self.printer.label("Response", verbosity)
        req = vars(response)
        for key in req:
            self.printer.kvp(key, req[key], verbosity)

    def _check_parser_for_mode(self):
        found = False
        for arg in self.parser.args:
            if arg.name == "mode":
                found = True
        if not found:
            raise Exception(f"The parser must contain a 'mode' argument, but none was found.")
