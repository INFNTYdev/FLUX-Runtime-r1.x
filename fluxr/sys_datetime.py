
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

        ...
        return
