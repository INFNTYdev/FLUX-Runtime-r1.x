
""" FLUX Runtime-Engine Framework Service Provider """


#   MODULE IMPORTS
from fluxr import *
...


#   MODULE PACKAGE
__package__ = pkg_n()


#   MODULE CLASSES
class ServiceUnit:
    def __init__(self, cls: any, func: any, clearance: int):
        """ Framework service unit """
        self.__class: type = cls
        self.__func = func
        self.__clearance: int = clearance
        return

    def get_class(self) -> type:
        """ Returns the service units class """
        return self.__class

    def func(self) -> any:
        """ Returns the units function """
        return self.__func

    def lvl(self) -> int:
        """ Returns the units clearance value """
        return self.__clearance


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
        self.authorize_class(requestor=self, cls=self.__FW)
        if ('whitelist' in kwargs) and (type(kwargs.get('whitelist')) is list):
            for li in kwargs.get('whitelist'):
                self.whitelist_class(self.__FW, li[0], li[1])
        return

    def services(self) -> list:
        """ Returns list of all current service calls """
        return [call for call in self.__serve.keys()]

    def new_service(self, call: str, cls: any, func: any, **kwargs):
        """ Add a function reference to the service provider """
        if callable(func):
            if not self.__existing_call(call):
                self.__serve[call] = ServiceUnit(
                    cls=self.p_obj(cls),
                    func=func,
                    clearance=self.__value_to_const(kwargs.get('clearance', 0))
                )
        return

    def serve(self, requestor: any) -> dict:
        """ Returns appropriate services to requestor """
        svcs: dict = {}
        if self.__whitelisted(requestor):
            s: list = [x for x in self.__serve.keys() if self.__has_authority(requestor, x)]
            for approved in s:
                svcs[approved] = self.__serve[approved].func()
        return svcs

    def whitelist_class(self, requestor: any, cls: any, clearance: str = 'any', **kwargs):
        """ Add a class to the providers whitelist """
        if self.__authorized(requestor):
            self.__whitelist[self.p_obj(cls)] = self.__value_to_const(clearance)
            if kwargs.get('admin', False):
                self.authorize_class(requestor, cls)
        return

    def authorize_class(self, requestor: any, cls: any):
        """ Add a class to the providers administration """
        if self.__authorized(requestor):
            self.__admin.append(self.p_obj(cls))
            self.__whitelist[self.p_obj(cls)] = self.__HIGH
            self.__out(F"Provided {str(self.p_obj(cls).__name__)} with service administrative rights")
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

    def __whitelisted(self, requestor: any) -> bool:
        """ Determines if requestor is whitelisted """
        return bool(self.p_obj(requestor) in list(self.__whitelist.keys()))

    def __has_authority(self, requestor: any, call: str):
        """ Determines if a class has authority to use a service """
        if self.__whitelisted(requestor):
            if self.__whitelist[self.p_obj(requestor)] >= self.__serve[call].lvl():
                return True
        return False

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
            if 0 <= value <= 3:
                return value
        return

    def __existing_call(self, call: str) -> bool:
        """ Determines whether a given call value already exist """
        return bool(call in self.services())

    def __out(self, text: str, **kwargs):
        """ Send text to the console """
        self.__S['console'](text, **kwargs)
        return
