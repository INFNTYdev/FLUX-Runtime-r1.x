
""" FLUX Runtime-Engine Framework Console Manager """


#   MODULE IMPORTS
from fluxr import *


#   MODULE PACKAGE
__package__ = pkg_n()


#   MODULE CLASSES
class ConsoleQueueEntry:
    def __init__(self):
        """ Console queue entry """
        return


class ConsoleLogEntry:
    def __init__(self):
        """ Console log entry """
        return


class ConsoleLog:
    def __init__(self):
        """ Framework console log """
        self.__console_log: dict = {}
        self.__console_queue: list = []
        self.__index: int = 0
        return

    def log(self):
        """ Log console output to console log and queue """
        return

    def queue_length(self) -> int:
        """ Returns the queues current length """
        return len(self.__console_queue)

    def log_length(self) -> int:
        """ Returns the current length of the log """
        return len(self.__console_log.keys())

    def log_index(self) -> int:
        """ Returns the logs current index """
        return self.__index


class SystemConsoleManager:
    def __init__(self, fw: any, svc_c: any):
        """ Framework console manager """
        self.__FW = fw_obj(fw)
        self.__S = svc_c

        self.__console_host: ConsoleLog = ConsoleLog()
        self.__inject_services()
        return

    def start(self):
        """ Start framework console manager """
        return

    def console_out(self, text: str, **kwargs):
        """ Send text to the console manager log for output """
        p_config: dict = {
            'is_error': kwargs.get('error', False),
            'skip_line': kwargs.get('skip', bool(self.__console_host.log_index() == 0)),
            'prefix': kwargs.get('prefix', ''),
            'seperator': kwargs.get('sepr', '|'),
            'show_date': kwargs.get('c_date', True),
            'show_time': kwargs.get('c_time', True)
        }
        return

    # FRAMEWORK SERVICE BOILER PLATE - lvl3
    def __inject_services(self):
        """ Add class functions to service provider """
        pass

    def __out(self, text: str, **kwargs):
        """ Send text to the console """
        self.__S(self)['console'](text, **kwargs)
        return

    def __status(self, status: bool):
        """ Update the modules status """
        self.__S(self)['setstat'](self, status)
        return

    def __date(self) -> str:
        """ Returns the current date """
        return self.__S(self)['date']()

    def __time(self) -> str:
        """ Returns the current time """
        return self.__S(self)['time']()

    def __runtime(self) -> str:
        """ Returns the current runtime """
        return self.__S(self)['rt']()

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
