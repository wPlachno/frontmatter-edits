# wcmodehandler.py
# Version: 0.0.1.010
# Last Changes: 01/01/2025 - Made default handler debug aware

from utilities.wcutil import WoodchipperNamespace as WCNamespace
from utilities.wcconstants import RESULTS

class WoodchipperCoreModeHandler:
    def __init__(self, request: any, response: any):
        self.request = request
        self.response = response
        self.debug = request.debug
        self.results = WCNamespace("HandlerResults")
        self.results.add(RESULTS.ERROR, None)
        self.results.add(RESULTS.SUCCESS, False)

    def log_success(self):
        self.results.success = True

    def log_error(self, error):
        self.results.success = False
        self.results.error = error

    def log_kvp(self, key, value):
        self.results.add(key, value)

    def handle(self):
        return True

    def run(self):
        self.handle()
        return self.results