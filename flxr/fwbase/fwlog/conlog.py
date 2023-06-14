
""" Framework Console Log Database """


#   MODULE IMPORTS
from flxr.fwbase.fwlog import *


#   MODULE CLASSES
class FWConsoleDatabase(list):
    def __init__(self) -> None:
        """ Framework console log database """
        super().__init__()

    def get_next(self) -> FWConsoleLogEntry:
        """ Returns the next console entry """
        if len(self) > 0:
            _next: FWConsoleLogEntry = self[0]
            del self[0]
            return _next
