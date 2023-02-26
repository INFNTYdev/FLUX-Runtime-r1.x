
""" FLUX Runtime-Engine Framework Exception Handler """


#   MODULE IMPORTS
from fluxr import *


#   MODULE PACKAGE
__package__ = pkg_n()


#   MODULE CLASSES
class ExceptionLogEntry:
    def __init__(self, **kwargs):
        """ Framework exception log entry """
        self.__exc_index: int = kwargs.get('index')
        self.__exc_date: str = kwargs.get('date')
        self.__exc_time: str = kwargs.get('time')
        self.__unaccounted: bool = kwargs.get('unaccounted')
        self.__author: str = kwargs.get('author')
        self.__type: str = kwargs.get('type')
        self.__exc_cause: str = kwargs.get('cause')
        self.__exc_pointer: str = kwargs.get('pointer')
        return

    def get_index(self) -> int:
        """ Returns the exceptions index """
        return self.__exc_index

    def get_date(self) -> str:
        """ Returns the exceptions occurrence date """
        return self.__exc_date

    def get_time(self) -> str:
        """ Returns the exceptions occurrence time """
        return self.__exc_time

    def is_unaccounted(self) -> bool:
        """ Determines if the exception is unaccounted """
        return self.__unaccounted

    def authoring_class(self) -> str:
        """ Returns a string of the exceptions author """
        return self.__author

    def get_type(self) -> str:
        """ Returns the exception type """
        return self.__type

    def get_cause(self) -> str:
        """ Returns the exception cause """
        return self.__exc_cause

    def get_pointer(self) -> str:
        """ Returns the exception pointer """
        return self.__exc_pointer


class ExceptionLog:
    def __init__(self, **kwargs):
        """ Framework exception log """
        self.__exc_log: list = []
        return

    def log(self):
        """ Log an exception to the log """
        return

    def length(self) -> int:
        """ Returns the number of exception logged """
        return len(self.__exc_log)


class FrameworkExceptionManager:
    def __init__(self, fw: any):
        """ Framework exception manager """
        self.__FW = fw_obj(fw)
        self.__S: dict = None

        ...
        return
