# fm_printer.py
# Written By: Will Plachno
# Created: 01/11/2025
# Version: 0.0.1.006
# Last Changed: 01/26/2025

from utilities.wcmodeprinter import WoodchipperCoreModePrinter as WCPrinter
from utilities.wcconstants import Verbosity, clr, COLOR
from utilities.wcutil import WoodchipperHeatMap as WCHeatMap, colorize_path as PATH
from constants import OUT, CHANGE

class FrontMatterPrinterDefault(WCPrinter):
    def __init__(self, request, response):
        WCPrinter.__init__(self, request, response)
        self.file_list = self.data.files
        self.heat = WCHeatMap()

    def print(self):
        if WCPrinter.print(self):
            for file in self.file_list:
                self.describe_file_change(file)
            self.printer.nl(verbosity=Verbosity.DEBUG)
            heat_map, total = self.heat.compile()
            self.printer.pr(OUT.TOTAL.TOTAL + str(total))
            for heat_item in heat_map:
                change_type = heat_item[0]
                freq = heat_item[1]
                change_summary = self.translate_change(change_type, OUT.TOTAL) + str(freq)
                self.printer.pr(change_summary)

    def describe_file_change(self, file):
        change_type = CHANGE.SET
        if not file.previous_value:
            change_type = CHANGE.ADDED
        elif not file.current_value:
            change_type = CHANGE.REMOVED
        if file.previous_value == file.current_value:
            change_type = CHANGE.SKIPPED
        self.heat.mark(change_type)
        change_desc = self.translate_change(change_type, OUT)
        self.printer.pr(OUT.FULL.format(PATH(file.path), change_desc, str(file.previous_value), str(file.current_value)), Verbosity.DEBUG)

    @staticmethod
    def translate_change(change, other):
        match change:
            case CHANGE.ADDED:
                return other.ADDED
            case CHANGE.REMOVED:
                return other.REMOVED
            case CHANGE.SET:
                return other.SET
        return other.SKIPPED

class FrontMatterPrinterTargeted(WCPrinter):
    def __init__(self, request, response):
        WCPrinter.__init__(self, request, response)
        self.target_files = list(self.data.paths)

    def print(self):
        if self.printer.verb(Verbosity.DEBUG):
            self.printer.pr("Target files: ")
            for path in self.target_files:
                self.printer.pr(f" - {PATH(path)}")
            self.printer.nl()
        return WCPrinter.print(self)

class FrontMatterPrinterSummarize(FrontMatterPrinterTargeted):
    def __init__(self, request, response):
        FrontMatterPrinterTargeted.__init__(self, request, response)
        self.key_map = self.data.keys
        self.total_properties = self.data.total
        self.unique_values = 0

    def print(self):
        if FrontMatterPrinterTargeted.print(self):
            for key_item in self.key_map:
                self.print_key(key_item)
            self.printer.nl()
            self.printer.pr(OUT.SUMMARIZE.UNIQUE_KEYS.format(len(self.key_map)))
            self.printer.pr(OUT.SUMMARIZE.UNIQUE_VALUES.format(self.unique_values))
            self.printer.pr(OUT.SUMMARIZE.TOTAL_PROPERTIES.format(self.total_properties))

    def print_key(self, key_item):
        key = key_item.key
        freq = key_item.frequency
        values = key_item.values
        unique_values = len(values)
        self.unique_values += unique_values
        self.printer.pr(OUT.SUMMARIZE.SHORT.format(key, freq, unique_values))
        if self.printer.verbosity == Verbosity.DEBUG:
            for value_item in values:
                value = value_item.value
                val_freq = value_item.frequency
                self.printer.pr(OUT.SUMMARIZE.VALUE.format(value, val_freq))

class FrontMatterPrinterShow(FrontMatterPrinterTargeted):
    def __init__(self, request, response):
        FrontMatterPrinterTargeted.__init__(self, request, response)
        self.key = self.data.key
        self.values = self.data.values
        self.amt_unique_values = self.data.unique
        self.occurrences = self.data.occurrences

    def print(self):
        # Property: [NAME]
        # Occurrences: [FREQ]
        # Values: [FREQ]
        # [VALUE]: [FREQ]
        # - [FILE]
        if FrontMatterPrinterTargeted.print(self):
            # values: [{value, frequency, files: list}]
            for value_item in self.values:
                value = value_item.value
                frequency = value_item.frequency
                files = value_item.files
                self.printer.pr(OUT.SHOW.VALUE.format(value, frequency))
                for file in files:
                    self.printer.pr(OUT.SHOW.PATH.format(PATH(file)))
            self.printer.nl()
            self.printer.pr(OUT.SHOW.HEADER.format(self.key, self.occurrences, self.amt_unique_values))

