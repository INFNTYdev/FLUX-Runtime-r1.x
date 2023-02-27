
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
        self.__S = fw.service_call(self)

        self.__out("TEST")
        return

    def __out(self, text: str, **kwargs):
        """ Send text to the console """
        self.__S(self)['console'](text, **kwargs)
        return
