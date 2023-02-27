
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
        self.__inject_services()
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
        if self.RUN:
            return True
        else:
            return False

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

    # FRAMEWORK CONTROL BOILER PLATE - lvl1
    def __inject_services(self):
        """ Add class functions to service provider """
        self.__new_service('date', self, self.current_date)
        self.__new_service('time', self, self.current_time)
        return

    def __out(self, text: str, **kwargs):
        """ Send text to the console """
        self.__S(self)['console'](text, **kwargs)
        return

    def __status(self, status: bool):
        """ Update the modules status """
        self.__S(self)['setstat'](self, status)
        return

    def __fw_stable(self) -> bool:
        """ Determines if required system modules are active """
        return self.__S(self)['corestat']()

    def __fw_active(self) -> bool:
        """ Returns frameworks run status """
        return self.__S(self)['runstat']()

    def __new_service(self, call: str, cls: any, func: any, **kwargs):
        """ Add a function reference to the service provider """
        self.__S(self)['nsvc'](call, cls, func, **kwargs)
        return

    def __threads(self) -> list:
        """ Returns a list of stored thread handles """
        return self.__S(self)['threads']()

    def __new_thread(self, handle: str, thread: Thread, **kwargs):
        """ Establish new thread in thread host """
        self.__S(self)['nthread'](handle, thread, **kwargs)
        return

    def __delete_thread(self, handle: str):
        """ Delete requested thread """
        self.__S(self)['dthread'](handle)
        return

    def __exc(self, cls: any, exc_o: any, exc_info: tuple, **kwargs):
        """ Handle system raised exceptions """
        self.__S(self)['exc'](cls, exc_o, exc_info, **kwargs)
        return
