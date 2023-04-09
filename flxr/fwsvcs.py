
""" Framework services host """


# MODULE IMPORTS
from flxr import *

# MODULE PACKAGE
__package__ = pkg_n()


# MODULE CLASSES
class Service:
    def __init__(self, cls: type, func: any, clearance: int = ANY):
        """
        Framework service unit

        :param cls: The services encompassing class
        :param func: The services function
        :param clearance: The services security clearance
        """

        self.__type: type = cls
        self.__function = func
        self.__clearance: int = clearance

    def service_class(self) -> type:
        """ Returns the class type of the service """
        return self.__type

    def execute(self, **kwargs) -> any:
        """ Execute the service function """
        return self.__function(**kwargs)

    def clearance(self) -> int:
        """ Returns the service clearance level """
        return self.__clearance


class ServiceHost:

    __whitelist: dict = {}
    __admin: list = []

    def __init__(self, fw: any, svc: any, **kwargs):
        """
        Framework services host

        :param svc: Initial base framework services
        :param whitelist: List of types to whitelist on initialization
        :param kwargs: Additional initialization parameters
        """

        self.__host = fw_obj(fw)
        self._base: dict = svc
        self.__services: dict = {}
        self.whitelist(
            requestor=self,
            cls=self.__host,
            admin=True
        )
        self._apply_base_services(svc)
        if ('whitelist' in kwargs) and (type(kwargs.get('whitelist')) is list):
            for cls in kwargs.get('whitelist'):
                self.whitelist(
                    requestor=self.__host,
                    cls=self._class_of(cls[0]),
                    clearance=int(cls[1])
                )
        self._inject_services()

    def services(self) -> list:
        """ Returns the list of all available system services """
        return [call for call in self.__services.keys()]

    def whitelist(self, requestor: any, cls: any, **kwargs):
        """ Add a class to the services distrubutor whitelist """
        if self._authorized(requestor) or (requestor is self):
            self.__whitelist[self._class_of(cls)] = int(kwargs.get('clearance', ANY))
            self._base['console'](f"Successfully added '{self._class_of(cls).__name__}' to services whitelist")
            if kwargs.get('admin', False):
                self.authorize(requestor, cls)

    def authorize(self, requestor: any, cls: any):
        """ Add a class to the services distributor administration """
        if self._authorized(requestor) or (requestor is self):
            self.__admin.append(self._class_of(cls))
            self.__whitelist[self._class_of(cls)] = HIGH
            self._base['console'](f"Provided '{self._class_of(cls).__name__}' with services admin priviledges")

    def new(self, call: str, cls: any, func: any, **kwargs):
        """ Add a new system service to distributor """
        if callable(func):
            if not self._existing_call(call):
                self.__services[call] = Service(
                    cls=self._class_of(cls),
                    func=func,
                    clearance=kwargs.get('clearance', ANY)
                )
                self._base['console'](f"Added '{call}' call to framework services")

    def override(self, requestor: any, call: str, using: any, func: any, **kwargs):
        """ Override an existing system service with a new """
        if self._existing_call(call):
            if self._has_authority(requestor, self.__services[call]):
                prev_clearance: int = self.__services[call].clearance()
                self.__services[call] = Service(
                    cls=self._class_of(using),
                    func=func,
                    clearance=kwargs.get('clearance', prev_clearance)
                )

    def serve(self, requestor: any) -> dict:
        """ Returns appropriate system services to requestor """
        svcs: dict = {}
        if self._whitelisted(self._class_of(requestor)):
            s: list = [
                call for call, __svc in self.__services.items() if self._has_authority(self._class_of(requestor), __svc)
            ]
            for approved in s:
                svcs[approved] = self.__services[approved].execute
        return svcs

    def _whitelisted(self, requestor: any) -> bool:
        """ Determines if a requestor is whitelisted """
        for _cls, __hierarchy in self.__whitelist.items():
            if self._class_of(requestor) is _cls:
                return True
        return False

    def _authorized(self, requestor: any) -> bool:
        """ Determines if a requestor has administrative rights """
        return self._class_of(requestor) in self.__admin

    def _has_authority(self, requestor: any, svc: Service) -> bool:
        """ Determines if a class is authorized to use a service """
        if self._whitelisted(self._class_of(requestor)):
            if self.__whitelist[self._class_of(requestor)] >= svc.clearance():
                return True
        return False

    def _inject_services(self):
        """ Inject service host services into distributor """
        injectables: list = [
            ('svcs', self.services, MED),
            ('osvc', self.override, MED),
            ('wcls', self.whitelist, LOW),
            ('acls', self.authorize, LOW),
            ('nsvc', self.new, ANY),
            ('clsof', self._class_of, ANY)
        ]
        for new in injectables:
            self.new(
                call=new[0],
                cls=self,
                func=new[1],
                clearance=new[2]
            )

    def _apply_base_services(self, svc: dict):
        """ Apply the frameworks base services to the distributor """
        for _call, __service in svc.items():
            if callable(__service):
                self.__services[_call] = Service(
                    cls=self.__host,
                    func=__service
                )

    def _existing_call(self, call: str) -> bool:
        """ Determines if a service call exist in the distributor """
        for _call in self.__services.keys():
            if _call == call:
                return True
        return False

    @staticmethod
    def _class_of(obj: any) -> type:
        """ Returns the class of a given object """
        if 'object' in str(obj):
            return obj.__class__
        elif inspect.isclass(obj):
            return obj
