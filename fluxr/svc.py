
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

    __HIGH: int = 3
    __MED: int = 2
    __LOW: int = 1
    __ANY: int = 0

    def __init__(self, fw: any, **kwargs):
        """ Framework service provider """
        self.__FW = fw_obj(fw)
        self.__S: dict = fw.base_services()

        self.__out("Initializing service provider...")
        self.__serve: dict = {}
        self.__eval_param(**kwargs)
        return

    def __eval_param(self, **kwargs):
        """ Evaluate provider parameters """
        self.whitelist_class(requestor=self, cls=self.__FW, clearance=self.__HIGH)
        self.authorize_class(requestor=self, cls=self.__FW)
        if ('whitelist' in kwargs) and (kwargs.get('whitelist') is list):
            for li in kwargs.get('whitelist'):
                self.whitelist_class(self.__FW, li[0], li[1])
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
            self.__whitelist[self.p_obj(cls)] = self.__value_to_const(clearance)
        return

    def authorize_class(self, requestor: any, cls: any):
        """ Add a class to the providers administration """
        if self.__authorized(requestor):
            self.__admin.append(self.p_obj(cls))
            self.__whitelist[self.p_obj(cls)] = self.__HIGH
        return

    @staticmethod
    def p_obj(obj: any) -> type:
        """ Returns the class of a request object """
        if 'object' in str(obj):
            return obj.__class__
        elif inspect.isclass(obj):
            return obj
        return

    def __authorized(self, requestor: any) -> bool:
        """ Determines if requestor has administrative rights """
        return bool((self.p_obj(requestor) in self.__admin)
                    or (requestor == self))

    def __value_to_const(self, value: any) -> int:
        """ Returns class constant value from string or integer """
        if type(value) is str:
            if value.lower() == 'h' or value.lower() == 'high':
                return self.__HIGH
            elif value.lower() == 'm' or value.lower() == 'medium':
                return self.__MED
            elif value.lower() == 'l' or value.lower() == 'low':
                return self.__LOW
            elif value.lower() == 'a' or value.lower() == 'any':
                return self.__ANY
        elif type(value) is int:
            if value <= 3:
                return value
        return

    def __out(self, text: str, **kwargs):
        """ Send text to the console """
        self.__S['console'](text, **kwargs)
        return
