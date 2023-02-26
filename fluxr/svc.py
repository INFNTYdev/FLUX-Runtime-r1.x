
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

    HIGH: int = 3
    MED: int = 2
    LOW: int = 1
    ANY: int = 0

    def __init__(self, fw: any, **kwargs):
        """ Framework service provider """
        self.__FW = fw_obj(fw)
        self.__S: dict = fw.base_services()

        self.__out("Initializing service provider...")
        self.__serve: dict = {}
        self.__eval_param(**kwargs)
        return

    def __eval_param(self, **kwargs):
        """ Initialize provider parameters """
        return

    def services(self) -> list:
        """ Returns list of all current services """
        return

    def new_service(self, call: str, cls: any, func: any, clearance: str):
        """ Add a function to the service provider """
        return

    def serve(self, requestor: any) -> dict:
        """ Returns appropriate services to requestor """
        return

    def whitelist_class(self, requestor: any, cls: any, clearance: str):
        """ Add a class to the providers whitelist """
        if self.__authorized(requestor):
            pass
        return

    def authorize_class(self, requestor: any, cls: any):
        """ Add a class to the providers administration """
        return

    def __authorized(self, requestor: any) -> bool:
        """ Determines if requestor has administrative rights """
        return

    def __out(self, text: str, **kwargs):
        """ Send text to the console """
        self.__S['console'](text, **kwargs)
        return
