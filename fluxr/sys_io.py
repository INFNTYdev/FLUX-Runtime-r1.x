
""" FLUX Runtime-Engine Framework File I/O Manager """


#   MODULE IMPORTS
from fluxr import *


#   MODULE PACKAGE
__package__ = pkg_n()


#   MODULE CLASSES
class SystemFileIOManager:
    def __init__(self, fw: any, svc_c: any):
        """ Framework file I/O manager """
        self.__FW = fw_obj(fw)
        self.__S = svc_c

        self.RUN: bool = False
        return

    def stop(self):
        """ Stop framework file manager """
        self.RUN = False
        return
