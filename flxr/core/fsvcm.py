
"""
Framework Service Manager Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
pass


#   EXTERNAL IMPORTS
from flxr.common.core import DeployableFwm
from flxr.constant import SvcVars, GlobalFuncs
from flxr.utility import FlxrService


#   MODULE CLASS
class FlxrServiceManager(DeployableFwm):

    __whitelist: dict = {}
    __admin: list = []

    def __init__(self, hfw) -> None:
        """ Framework service manager """
        super().__init__(hfw=hfw, cls=FlxrServiceManager)
        self.__services: dict = {}
        self.whitelist(requestor=self, cls=self, admin=True)
        self.whitelist(requestor=self, cls=hfw, admin=True)
        self.__inject_self()

    def calls(self) -> list[str]:
        """ Returns list of all
        framework service calls """
        return [name for name in self.__services.keys()]

    def existing_call(self, call: str) -> bool:
        """ Returns true if provided
        call exist in services """
        return call in self.calls()

    def whitelisted(self, requestor) -> bool:
        """ Returns true if provided
        requestor is whitelisted """
        return GlobalFuncs.class_of(requestor) in self.__whitelist.keys()

    def authorized(self, requestor) -> bool:
        """ Returns true if provided requestor
        has administrative privileges """
        return GlobalFuncs.class_of(requestor) in self.__admin

    def class_clearance(self, cls: type) -> int:
        """ Returns security clearance
        of provided class """
        if self.whitelisted(cls):
            return self.__whitelist[GlobalFuncs.class_of(cls)]
        return None

    def has_permission(self, requestor, svc: FlxrService) -> bool:
        """ Returns true if provided requestor
        has permission to use provided service """
        if not self.whitelisted(requestor):
            return False
        return self.__whitelist[GlobalFuncs.class_of(requestor)] >= svc.clearance()

    def serve(self, requestor) -> dict[FlxrService]:
        """ Returns appropriate framework
        services to requestor """
        _svcs: dict = {}
        if self.whitelisted(requestor):
            _svcs = {
                _call: __svc.execute for _call, __svc in self.__services.items()
                if self.has_permission(requestor=requestor, svc=__svc)
            }
        if _svcs == {}:
            self.console(msg=SvcVars.SLM_F_006.format(requestor=GlobalFuncs.class_of(requestor)))
        return _svcs

    def serve_call(self) -> any:
        """ Returns framework services call """
        return self.serve

    def whitelist(self, requestor: type, cls, **kwargs) -> None:
        """ Add class to services whitelist group """
        if not self.whitelisted(cls):
            if not (self.authorized(requestor) or requestor == self):
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
        if not self.authorized(cls):
            if not (self.authorized(requestor) or requestor == self):
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

    def new(self, call: str, cls, func, **kwargs) -> None:
        """ Add new service to framework services """
        if not self.existing_call(call):
            self.__services[call] = FlxrService(
                cls=cls,
                func=func,
                clearance=kwargs.get('clearance', SvcVars.ANY)
            )
            self.console(msg=SvcVars.SLM_F_001.format(call=call))

    def override(self, requestor, call: str, using: type, func, **kwargs) -> None:
        """ Override an existing framework
        service with a new """
        pass

    def remove(self, call: str) -> None:
        """ Remove specified service
        from framework services """
        pass

    def __inject_self(self) -> None:
        """ Manually inject base
        service manager services """
        _injectables: list = [
            ('svcs', self.calls, SvcVars.ANY),
            ('nsvc', self.new, SvcVars.ANY),
            ('dsvc', self.remove, SvcVars.HIGH),
            ('wcls', self.whitelist, SvcVars.ANY),
            ('acls', self.authorize, SvcVars.ANY),
            ('osvc', self.override, SvcVars.ANY),
            ('clvl', self.class_clearance, SvcVars.ANY),
            ('ecall', self.existing_call, SvcVars.LOW),
        ]
        for new in _injectables:
            self.new(
                call=new[0],
                cls=FlxrServiceManager,
                func=new[1],
                clearance=new[2]
            )
        for call, _func in self.hfw().base_service().items():
            self.new(
                call=call,
                cls=type(self.hfw()),
                func=_func,
                clearance=SvcVars.ANY
            )
