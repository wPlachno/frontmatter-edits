# propertyfiller.py
# Created: 8/22/24 by Will Plachno
# Version: 0.0.2.001
# Last Changed: 01/15/2025

import sys

from utilities.wccore import WoodchipperCore as WCCore
import interface.fm_parser as my_parser
import core.fm_handler as handlers
import interface.fm_printer as printers
from constants import MODE

def _main(args):
    core = WCCore()
    core.set_parser_builder(my_parser.build_parser)
    core.set_post_parser(my_parser.post_parser)
    core.set_debug_mode_description("Debug mode prohibits file changes.")
    core.add_mode(MODE.SUMMARIZE, handlers.FrontMatterHandlerSummarize, printers.FrontMatterPrinterSummarize)
    core.add_mode(MODE.SHOW, handlers.FrontMatterHandlerShow, printers.FrontMatterPrinterShow)
    core.add_mode(MODE.ADD, handlers.FrontMatterHandlerDefault, printers.FrontMatterPrinterDefault)
    core.add_mode(MODE.CHANGE, handlers.FrontMatterHandlerDefault, printers.FrontMatterPrinterDefault)
    core.add_mode(MODE.SET, handlers.FrontMatterHandlerDefault, printers.FrontMatterPrinterDefault)
    core.add_mode(MODE.REMOVE, handlers.FrontMatterHandlerRemove, printers.FrontMatterPrinterDefault)
    core.run()

if __name__ == "__main__":
    _main(sys.argv)