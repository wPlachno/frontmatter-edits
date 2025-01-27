# fm_handler.py
# Created: 01/11/2025
# Version: 0.0.1.004
# Last Changed: 01/27/2025

from utilities.wcmodehandler import WoodchipperCoreModeHandler as WCHandler
from utilities.wcutil import WoodchipperNamespace as WCNamespace, WoodchipperHeatMapDictionary as WCHeatDict, \
    WoodchipperListDictionary as WCListDict
from core.fm_file import WoodchipperObsidianFile as WCObsidianFile
from constants import RESPONSE


class FrontMatterHandlerDefault(WCHandler):
    def __init__(self, request, response):
        WCHandler.__init__(self, request, response)
        self.key = self.request.key
        self.value = self.request.value
        self.filter = self.request.filter_property
        self.target_paths = self.request.target_paths
        self.add_if_necessary = self.request.add_if_necessary
        self.change_if_existing = self.request.change_if_existing
        self.file_results = list(())

    def handle(self):
        for target_path in self.target_paths:
            target_file = WCObsidianFile(target_path)
            target_file.read()
            self.file_results.append(self.handle_file(target_file))
            if not self.debug:
                target_file.write()
        self.compile_success()

    def handle_file(self, target_file: WCObsidianFile):
        previous_value = target_file[self.key]
        current_value = previous_value
        filter_match = self.matches_filter(target_file)
        if filter_match:
            current_value = target_file.set_property(self.key, self.value, self.add_if_necessary, self.change_if_existing)
        file_ns = self.compile_file(target_file, previous_value, current_value, filter_match)
        return file_ns

    def compile_file(self, target_file: WCObsidianFile, previous_value, current_value, filter_match: bool):
        file_ns = WCNamespace(target_file.file.name)
        file_ns.add(RESPONSE.FILE.PATH, target_file.file.path)
        file_ns.add(RESPONSE.FILE.PREVIOUS_VALUE, previous_value)
        file_ns.add(RESPONSE.FILE.CURRENT_VALUE, current_value)
        file_ns.add(RESPONSE.FILE.PASSED_FILTER, filter_match)
        if not self.debug:
            target_file.write()
        return file_ns

    def compile_success(self, success=True):
        self.log_kvp(RESPONSE.FILES, self.file_results)
        if success:
            self.log_success()

    def matches_filter(self, file):
        if self.filter:
            target_value = file[self.filter[0]]
            return target_value == self.filter[1]
        return True

class FrontMatterHandlerRemove(FrontMatterHandlerDefault):
    def handle_file(self, target_file):
        removed_value = target_file[self.key]
        filter_match = self.matches_filter(target_file)
        if removed_value and filter_match:
            del target_file[self.key]
        file_ns = self.compile_file(target_file, removed_value, target_file[self.key], filter_match)
        return file_ns

class FrontMatterHandlerSummarize(WCHandler):
    def __init__(self, request, response):
        WCHandler.__init__(self, request, response)
        self.target_paths = self.request.target_paths
        self.heat = WCHeatDict()

    def handle(self):
        for target_path in self.target_paths:
            target_file = WCObsidianFile(target_path)
            target_file.read()
            for prop_item in target_file.properties:
                self.heat.mark(prop_item.key, prop_item.value)
        self.compile_success()

    def compile_success(self, success=True):
        raw_heat_list, heat_total = self.heat.compile()
        ns_heat_list = list(())
        for key_item in raw_heat_list:
            ns_heat_list.append(self._compile_heat_item(key_item))
        self.log_kvp(RESPONSE.SUMMARIZE.PATHS, self.target_paths)
        self.log_kvp(RESPONSE.SUMMARIZE.KEYS, ns_heat_list)
        self.log_kvp(RESPONSE.SUMMARIZE.TOTAL, heat_total)
        if success:
            self.log_success()

    def _compile_heat_item(self, key_item):
        key = key_item[0]
        key_freq = key_item[1]
        values = key_item[2]
        heat_list = list(())
        for value_item in values:
            value = value_item[0]
            value_freq = value_item[1]
            value_ns = self.compile_heat_dict_value(key, value, value_freq)
            heat_list.append(value_ns)
        return self.compile_heat_dict_key(key, key_freq, heat_list)

    @staticmethod
    def compile_heat_dict_value(key, value, frequency):
        value_ns = WCNamespace(f"{key}:{value}")
        value_ns.add(RESPONSE.SUMMARIZE.KEY.VALUE.VALUE, value)
        value_ns.add(RESPONSE.SUMMARIZE.KEY.VALUE.FREQUENCY, frequency)
        return value_ns

    @staticmethod
    def compile_heat_dict_key(key, frequency, values):
        key_ns = WCNamespace(key)
        key_ns.add(RESPONSE.SUMMARIZE.KEY.KEY, key)
        key_ns.add(RESPONSE.SUMMARIZE.KEY.FREQUENCY, frequency)
        key_ns.add(RESPONSE.SUMMARIZE.KEY.VALUES, values)
        return key_ns

class FrontMatterHandlerShow(WCHandler):
    def __init__(self, request, response):
        WCHandler.__init__(self, request, response)
        self.target_paths = self.request.target_paths
        self.key = self.request.key
        self.value_locations = WCListDict()
        self.count = 0

    def handle(self):
        for target_path in self.target_paths:
            target_file = WCObsidianFile(target_path)
            target_file.read()
            file_value = target_file[self.key]
            if file_value:
                self.value_locations.mark(file_value, target_file.file.name)
                self.count += 1
        self.compile_success()

    def compile_success(self, success=True):
        values = list(map(lambda value_item: self._compile_value_item(value_item), self.value_locations.compile()))
        self.log_kvp(RESPONSE.SHOW.PATHS, self.target_paths)
        self.log_kvp(RESPONSE.SHOW.KEY, self.key)
        self.log_kvp(RESPONSE.SHOW.VALUES, values)
        self.log_kvp(RESPONSE.SHOW.OCCURRENCES, self.count)
        self.log_kvp(RESPONSE.SHOW.UNIQUE_VALUES, len(values))
        if success:
            self.log_success()

    def _compile_value_item(self, value_item):
        value = value_item[0]
        file_list = value_item[1]
        value_frequency = len(file_list) if file_list else 0
        value_ns = self.compile_value_description(self.key, value, value_frequency, file_list)
        return value_ns

    @staticmethod
    def compile_value_description(key, value, frequency, file_list):
        value_ns = WCNamespace(f"{key}:{value}")
        value_ns.add(RESPONSE.SHOW.VALUE.VALUE, value)
        value_ns.add(RESPONSE.SHOW.VALUE.FREQUENCY, frequency)
        value_ns.add(RESPONSE.SHOW.VALUE.FILES, file_list)
        return value_ns