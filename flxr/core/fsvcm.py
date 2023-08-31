
"""
Framework Service Manager Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
pass


#   EXTERNAL IMPORTS
from flxr.constant import SvcVars, GlobalFuncs
from flxr.utility import FlxrService
from .fwmod import FrameworkModule


#   MODULE CLASS
class FlxrServiceManager(FrameworkModule):

    __whitelist: dict = {}
    __admin: list = []

    def __init__(self, hfw) -> None:
        """ Framework service manager """
        super().__init__(hfw=hfw, cls=FlxrServiceManager)
        self.__services: dict = {}
        self.whitelist(requestor=self, cls=self, admin=True)
        self.whitelist(requestor=self, cls=hfw, admin=True)
        self._inject_self()

    def calls(self) -> list[str]:
        """ Returns the list of all framework service calls """
        return [name for name in self.__services.keys()]

    def new(self, call: str, cls, func, **kwargs) -> None:
        """ Add new service to framework services """
        if not self._existing_call(call):
            self.__services[call] = FlxrService(
                cls=cls,
                func=func,
                clearance=kwargs.get('clearance', SvcVars.ANY)
            )
            self.console(msg=SvcVars.SLM_F_001.format(call=call))

    def remove(self, call: str) -> None:
        """ Remove specified service from framework services """
        pass

    def whitelist(self, requestor: type, cls, **kwargs) -> None:
        """ Add class to services whitelist group """
        if not self._whitelisted(cls):
            if not (self._authorized(requestor) or requestor == self):
                self.console(
                    msg=SvcVars.SLM_F_003.format(
                        cls=GlobalFuncs.class_of(cls),
                        requestor=GlobalFuncs.class_of(requestor)
                    ),
                    notice=True
                )
                return
            self.__whitelist[GlobalFuncs.class_of(cls)] = int(kwargs.get('clearance', SvcVars.LOW))
            self.console(msg=SvcVars.SLM_F_002.format(cls=GlobalFuncs.class_of(cls).__name__))
            if kwargs.get('admin', False):
                self.authorize(requestor=requestor, cls=cls)

    def authorize(self, requestor: type, cls) -> None:
        """ Add class to services administration group """
        if not self._authorized(cls):
            if not (self._authorized(requestor) or requestor == self):
                self.console(
                    msg=SvcVars.SLM_F_004.format(
                        cls=GlobalFuncs.class_of(cls),
                        requestor=GlobalFuncs.class_of(requestor)
                    ),
                    notice=True
                )
                return
            self.__admin.append(GlobalFuncs.class_of(cls))
            self.__whitelist[GlobalFuncs.class_of(cls)] = SvcVars.HIGH
            self.console(msg=SvcVars.SLM_F_005.format(cls=GlobalFuncs.class_of(cls).__name__))

    def override(self, requestor: type, call: str, using: type, func, **kwargs) -> None:
        """ Override an existing framework service with new """
        pass

    def serve(self, requestor: type) -> dict[FlxrService]:
        """ Returns appropriate framework services
        to requestor """
        _svcs: dict = {}
        if self._whitelisted(requestor):
            _svcs = {
                _call: __svc.execute for _call, __svc in self.__services.items()
                if self._has_permission(requestor=requestor, svc=__svc)
            }
        if _svcs == {}:
            self.console(msg=SvcVars.SLM_F_006.format(requestor=GlobalFuncs.class_of(requestor)))
        return _svcs

    def serve_call(self) -> any:
        """ Returns the framework services call """
        return self.serve

    def class_clearance(self, cls: type) -> int:
        """ Returns the security clearance of
        the provided class """
        if self._whitelisted(cls):
            return self.__whitelist[GlobalFuncs.class_of(cls)]
        return None

    def _existing_call(self, call: str) -> bool:
        """ Returns true if the provided call exist
        in the services """
        return call in self.__services.keys()

    def _whitelisted(self, requestor: type) -> bool:
        """ Returns true if the provided requestor
        is whitelisted """
        return GlobalFuncs.class_of(requestor) in self.__whitelist.keys()

    def _authorized(self, requestor: type) -> bool:
        """ Returns true if the provided requestor
         has administrative privilege """
        return GlobalFuncs.class_of(requestor) in self.__admin

    def _has_permission(self, requestor, svc: FlxrService) -> bool:
        """ Returns true if the provided requestor has
        permission to use the service """
        if not self._whitelisted(requestor):
            return False
        return self.__whitelist[GlobalFuncs.class_of(requestor)] >= svc.clearance()

    def _inject_self(self) -> None:
        """ Manually inject base service manager services """
        _injectables: list = [
            ('svcs', self.calls, SvcVars.ANY),
            ('nsvc', self.new, SvcVars.ANY),
            ('dsvc', self.remove, SvcVars.HIGH),
            ('wcls', self.whitelist, SvcVars.ANY),
            ('acls', self.authorize, SvcVars.ANY),
            ('osvc', self.override, SvcVars.ANY),
            ('clvl', self.class_clearance, SvcVars.ANY),
            ('ecall', self._existing_call, SvcVars.LOW),
        ]
        for new in _injectables:
            self.new(
                call=new[0],
                cls=FlxrServiceManager,
                func=new[1],
                clearance=new[2]
            )
        for call, _func in self.framework().base_service().items():
            self.new(
                call=call,
                cls=type(self.framework()),
                func=_func,
                clearance=SvcVars.ANY
            )
