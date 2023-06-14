
""" Framework Service Host Module """


#   MODULE IMPORTS
from flxr.fwsvc import *


#   MODULE CLASSES
class ServiceHost:

    __whitelist: dict = {}
    __admin: list = []

    def __init__(self, hfw: any, svc: dict) -> None:
        """
        Framework service host
        
        :param hfw: The hosting framework in which services are deployed
        :param svc: Hosting framework base services
        """

        self.__hfw = fw_obj(hfw)
        self.__hfw_base: dict = svc
        self.__services: dict = {}
        self.whitelist(
            requestor=self,
            cls=hfw,
            admin=True
        )
        self._inject_services()
    
    def services(self) -> list:
        """ Returns the list of all available service calls """
        return [_call for _call in self.__services.keys()]
    
    def new(self, call: str, cls: any, func: any, **kwargs) -> None:
        """
        Add new service to service host
        
        :param call: Call symbol to be used in reference to service
        :param cls: The class in which the services function comes from
        :param func: The function in which the service executes
        :param kwargs: Additional service args such as security clearance
        """
        if not self._existing_call(call):
            self.__services[call] = FWService(
                cls=cls,
                func=func,
                clearance=kwargs.get('clearance', ANY)
            )
            self.__hfw_base['console'](f"Added '{call}' call to framework services")

    def whitelist(self, requestor: any, cls: any, **kwargs) -> None:
        """
        Add a class to the whitelist of the service host
        
        :param requestor: The requesting class initiating the whitelist call
        :param cls: The class to be whitelisted
        :param kwargs: Additional args such as security clearance and administrative rights
        """
        if not self._whitelisted(cls):
            if self._authorized(requestor) or (requestor == self):
                self.__whitelist[class_of(cls)] = int(kwargs.get('clearance', ANY))
                self.__hfw_base['console'](f"Successfully added '{class_of(cls).__name__}' to services whitelist")
                if kwargs.get('admin', False):
                    self.authorize(requestor, cls)
                return
            self.__hfw_base['console'](
                f"Failed to whitelist '{class_of(cls).__name__}' "
                f"because {class_of(requestor).__name__} class is not authorized to do so",
                error=True
            )

    def authorize(self, requestor: any, cls: any) -> None:
        """
        Provide a class with administrative privilege over service host
        
        :param requestor: The requesting class initiating the authorize call
        :param cls: The class to be authorized
        """
        if not self._authorized(cls):
            if self._authorized(requestor) or (requestor == self):
                self.__admin.append(class_of(cls))
                self.__whitelist[class_of(cls)] = HIGH
                self.__hfw_base['console'](f"Provided '{class_of(cls).__name__}' with service administrative priviledges")
                return
        self.__hfw_base['console'](
                f"Failed to authorize '{class_of(cls).__name__}' "
                f"because {class_of(requestor).__name__} class is not authorized to do so",
                error=True
        )

    def override(self, requestor: any, call: str, using: any, func: any, **kwargs) -> None:
        """
        Override an existing service with a new
        
        :param requestor: The requesting class initiating the override call
        :param call: Call symbol used in reference to existing service
        :param using: The class in which the services new function comes from
        :param func: The new function in which the service executes
        :param kwargs: Additional service args such as security clearance (None inherits previous clearance)
        """
        if self._existing_call(call):
            if self._has_permission(requestor, self.__services[call]):
                prev_clearance: int = self.__services[call].clearance()
                self.__services[call] = FWService(
                    cls=using,
                    func=func,
                    clearance=kwargs.get('clearance', prev_clearance)
                )
                self.__hfw_base['console'](f"Successfully updated '{call}' service call")
                return
            self.__hfw_base['console'](
                f"Failed to override '{call}' service call "
                f"because {class_of(requestor).__name__} class is not authorized to do so",
                error=True
            )

    def serve(self, requestor: any) -> dict:
        """
        Returns appropriate services to requestor
        
        :param requestor: The requesting class initiating the service call
        :return: The services available to requestor
        """
        _svcs: dict = {}
        if self._whitelisted(requestor):
            _svcs = {
                _call: __svc.execute for _call, __svc in self.__services.items()
                if self._has_permission(requestor, __svc)
            }
        if _svcs == {}:
            self.__hfw_base['console'](f"No service available for '{class_of(requestor).__name__}'")
        return _svcs

    def _existing_call(self, call: str) -> bool:
        """ Determines if a service call exists in the host """
        if call in self.__services.keys():
            return True
        return False

    def _whitelisted(self, requestor: any) -> bool:
        """ Determines if a requestor is whitelisted """
        if class_of(requestor) in self.__whitelist.keys():
            return True
        return False

    def _authorized(self, requestor: any) -> bool:
        """ Determines if a requestor has administrative privilege """
        if class_of(requestor) in self.__admin:
            return True
        return False

    def _has_permission(self, requestor: any, svc: FWService) -> bool:
        """ Determines if a requestor is authorized to use a service """
        if not self._whitelisted(requestor):
            return False
        
        # Locate services loose function at this point!
        # " AttributeError: 'function' object has no attribute 'clearance' "
        if self.__whitelist[class_of(requestor)] >= svc.clearance():
            return True
        return False

    def _inject_services(self) -> None:
        """ Add service host services to the host """
        _injectables: list = [
            ('svcs', self.services, MED),
            ('nsvc', self.new, ANY),
            ('osvc', self.override, LOW),
            ('wcls', self.whitelist, LOW),
            ('acls', self.authorize, LOW),
            ('ecall', self._existing_call, MED)
        ]
        for _new in _injectables:
            self.new(
                call=_new[0],
                cls=self,
                func=_new[1],
                clearance=_new[2]
            )

        for _call, _old in self.__hfw_base.items():
            self.__services[_call] = FWService(
                cls=type(self.__hfw),
                func=_old,
                clearance=ANY
            )
