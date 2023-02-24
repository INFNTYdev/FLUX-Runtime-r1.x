
""" FLUX Runtime-Engine Framework Exception Handler """


#   MODULE IMPORTS
from fluxr import *


#   MODULE PACKAGE
__package__ = pkg_n()


#   MODULE CLASSES
class ExceptionLogEntry:
    def __init__(self, **kwargs):
        """ Exception log entry """
        self.__exc_index: int = None
        self.__exc_date: str = None
        self.__exc_time: str = None
        self.__unaccounted: bool = None
        self.__author: str = None
        self.__type: str = None
        self.__exc_cause: str = None
        self.__exc_pointer: str = None
        return

    def get_index(self) -> int:
        """ Returns the exceptions index """
        return

    def get_date(self) -> str:
        """ Returns the exceptions occurrence date """
        return

    def get_time(self) -> str:
        """ Returns the exceptions occurrence time """
        return

    def is_unaccounted(self) -> bool:
        """ Determines if the exception is unaccounted """
        return

    def authoring_class(self) -> str:
        """ Returns a string of the exceptions author """
        return

    def get_type(self) -> str:
        """ Returns the exception type """
        return

    def get_cause(self) -> str:
        """ Returns the exception cause """
        return

    def get_pointer(self) -> str:
        """ Returns the exception pointer """
        return


class ExceptionLog:
    def __init__(self, **kwargs):
        """ Framework exception log """
        return


class FrameworkExceptionManager:
    pass
