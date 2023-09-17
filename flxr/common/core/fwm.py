
"""
Base FLUX Framework Dependant Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
from abc import ABC
import time


#   EXTERNAL IMPORTS
from flxr.common.protocols import Flux


#   MODULE CLASS
class Fwm(ABC):
    def __init__(self, hfw: Flux, cls: type) -> None:
        """ FLUX runtime framework module """
        self.__framework: Flux = self.__validate_hfw(hfw)
        self.__class: type = self.__validate_type(cls)
        self.__injectables: list = []

    def hfw(self) -> Flux:
        """ Returns module hosting framework instance """
        return self.__framework

    def fwm_class(self) -> type:
        """ Returns module type """
        return self.__class

    def hfw_service(self, svc: str, **svc_args) -> any:
        """ Execute specified framework service """
        return self.__framework.service(requestor=self.fwm_class())[svc](**svc_args)

    def fwm_clearance(self) -> int:
        """ Returns module framework service clearance """
        return self.hfw_service(svc='clvl', cls=self.fwm_class())

    def process_proxy(self) -> dict:
        """ Returns hosting framework process proxy """
        pass

    @staticmethod
    def threaded() -> bool: return False

    def to_service_injector(self, load: list[tuple]) -> None:
        """ Append module methods to
        framework service injector """
        for injectable in load:
            if type(injectable) is tuple:
                _call, _func, _clearance = injectable
                self.__injectables.append(
                    {'call': _call, 'func': _func, 'clearance': _clearance}
                )

    def inject_services(self) -> None:
        """ Send module services to
        framework service host """
        self.console(msg=f"Injecting {self.__class.__name__} services:")
        for _injectable in self.__injectables:
            self.hfw().inject_service(
                call=_injectable.get('call'),
                cls=self.fwm_class(),
                func=_injectable.get('func'),
                clearance=_injectable.get('clearance')
            )
        self.console(msg=f"Successfully injected {len(self.__injectables)} services")
        self.__injectables.clear()

    def console(self, msg: str, error: bool = False, **kwargs) -> None:
        """ Send text to the framework
        console for logging """
        self.hfw_service(svc='console', msg=msg, error=error, **kwargs)

    def exception(self, excinfo: tuple, **kwargs) -> None:
        """ Record module exception in framework log """
        self.hfw_service(svc='exception', cls=self.fwm_class(), excinfo=excinfo, **kwargs)

    def extend_permissions(self, cls: type, **kwargs) -> None:
        """ Extend module permissions to another class """
        self.console(msg=f"Extending permissions to {cls.__name__}...")
        self.hfw_service(
            svc='wcls',
            requestor=self.fwm_class(),
            cls=cls,
            admin=kwargs.get('admin', False),
            clearance=kwargs.get('clearance', 1)
        )

    @staticmethod
    def wait(secs: float) -> None: time.sleep(secs)

    @staticmethod
    def __invalid_parameter(param: str, value) -> None:
        """ Raises a value error on an invalid parameter """
        raise ValueError(
            f"Invalid value for {param} parameter: {value}"
        )

    def __validate_hfw(self, hfw) -> Flux:
        """ Validate hosting framework parameter """
        try:
            if hfw.is_rfw():
                return hfw
        except AttributeError:
            self.__invalid_parameter('hfw', hfw)

    def __validate_type(self, cls) -> type:
        """ Validate class type parameter """
        if type(cls) is type:
            return cls
        self.__invalid_parameter('cls', cls)
