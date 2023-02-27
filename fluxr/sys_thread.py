
""" FLUX Runtime-Engine Framework Thread Manager """


#   MODULE IMPORTS
from fluxr import *


#   MODULE PACKAGE
__package__ = pkg_n()


#   MODULE CLASSES
class SystemThread:
    def __init__(self, handle: str, thread: Thread, **kwargs):
        """ Framework thread """
        return


class SystemThreadManager:
    def __init__(self, fw: any, svc_c: any):
        """ Framework thread manager """
        self.__FW = fw_obj(fw)
        self.__S = svc_c

        self.__thread_host: dict = {}
        self.__inject_services()
        return

    def threads(self) -> list:
        """ Returns a list of stored thread handles """
        return [x for x in self.__thread_host.keys()]

    def thread_exist(self, handle: str):
        """ Determines if a thread exist in the host """
        return bool(handle in list(self.__thread_host.keys()))

    def thread_active(self, handle: str) -> bool:
        """ Determines if a thread is currently running """
        return

    def new(self, handle: str, thread: Thread, **kwargs):
        """ Establish new thread in thread host """
        return

    def start(self, handle: str):
        """ Start requested thread """
        return

    def join(self, handle: str):
        """ Join requested thread with main thread """
        return

    def delete(self, handle: str):
        """ Delete requested thread """
        return

    def __inject_services(self):
        """ Add thread manager functions to service provider """
        self.__S(self)['nsvc']('threads', self, self.threads)
        return

    def __out(self, text: str, **kwargs):
        """ Send text to the console """
        self.__S(self)['console'](text, **kwargs)
        return
