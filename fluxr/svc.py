
""" FLUX Runtime-Engine Framework Service Provider """


#   MODULE IMPORTS
from fluxr import *
...


#   MODULE PACKAGE
__package__ = pkg_n()


#   MODULE CLASSES
class ServiceProvider:

    __whitelist: dict = {}
    __admin: list = []

    def __init__(self, fw: any, **kwargs):
        """ Framework service provider """
        self.__FW = fw_obj(fw)
        fw.console_out("Initializing service provider...")
        self.__serve: dict = {}
        return

    def __init_attr(self, **kwargs):
        """ Initialize provider parameters """
        return

    def services(self) -> list:
        """ Returns list of all current services """
        return

    def serve(self, requestor: any) -> dict:
        """ Returns appropriate services to requestor """
        return
