
""" FLUX Runtime-Engine Framework Datetime Manager """


#   MODULE IMPORTS
from fluxr import *


#   MODULE PACKAGE
__package__ = pkg_n()


#   MODULE CLASSES
class SystemDatetimeManager:
    def __init__(self, fw: any, svc_c: any):
        """ Framework datetime manager """
        self.__FW = fw_obj(fw)
        self.__S = svc_c

        self.__local_datetime: dict = {
            'sec': 0,
            'min': 0,
            'hr': 0,
            'day': 0,
            'month': 0,
            'year': 0
        }
        self.__date: str = None
        self.__time: str = None
        self.__phase: str = None
        self.RUN: bool = False
        return

    def start(self):
        """ Start datetime manager """
        return

    def current_date(self) -> str:
        """ Returns the current date """
        return

    def current_time(self) -> str:
        """ Returns the current time """
        return

    def __runnable(self) -> bool:
        """ Determines if the module
        has permission to execute """
        return

    def __datetime(self):
        """ Datetime manager main loop """
        return

    def __update(self):
        """ Update datetime manager object """
        return

    @staticmethod
    def __convert_24_hr(hr: str):
        """ Convert 24-hr to 12-hr """
        return

    def __inject_services(self):
        """ Add datetime manager functions to service provider """
        return

    def __out(self, text: str, **kwargs):
        """ Send text to the console """
        self.__S(self)['console'](text, **kwargs)
        return

    def __status(self, status: bool):
        """ Update the modules status """
        return

    def __new_thread(self, handle: str, thread: Thread, **kwargs):
        """ Establish new thread in thread host """
        return

    def __exc(self, cls: any, exc_o: any, exc_info: tuple, **kwargs):
        """ Handle system raised exceptions """
        self.__S(self)['exc'](cls, exc_o, exc_info, **kwargs)
        return
