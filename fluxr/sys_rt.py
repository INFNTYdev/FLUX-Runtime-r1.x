
""" FLUX Runtime-Engine Framework Runtime Clock """


#   MODULE IMPORTS
from fluxr import *


#   MODULE PACKAGE
__package__ = pkg_n()


#   MODULE CLASSES
class SystemRuntimeClock(RuntimeClock):
    def __init__(self, fw: any, svc_c: any, **kwargs):
        """ Framework runtime clock """
        self.__FW = fw_obj(fw)
        self.__S = svc_c

        RuntimeClock.__init__(self)
        if ('with' in kwargs) and (type(kwargs.get('with')) is list):
            self.__out(f"System runtime clock starting from previous point")
            self.resume_from(kwargs.get('with'))
        self.__inject_services()
        return

    def start(self, **kwargs):
        """ Start framework runtime clock """
        self.__new_thread(
            handle='sys-runtime',
            thread=Thread(target=self.__override_start),
            start=True
        )
        initial: str = self.runtime()[-2:]
        while self.runtime()[-2:] == initial:
            time.sleep(0.2)
        self.__out("Master clock active")
        self.__status(True)
        return

    def __override_start(self):
        """ Override runtime clock start sequence """
        try:
            self.override_start(self.__FW)
        except BaseException as Unknown:
            self.__status(False)
            self.__exc(self, Unknown, sys.exc_info(), unaccounted=True,
                       pointer='__override_start()')
            self.__out("An error occurred in the system runtime clock main loop", error=True)
        finally:
            self.__status(False)
            self.__out("System runtime clock module stopped")
            return

    # FRAMEWORK SERVICE BOILER PLATE - lvl2
    def __inject_services(self):
        """ Add class functions to service provider """
        self.__new_service('rt', self, self.runtime)
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
