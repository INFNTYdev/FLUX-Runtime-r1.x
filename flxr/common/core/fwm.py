
"""
Base FLUX Framework Dependant Module
"""


#   BUILT-IN IMPORTS
from abc import ABC
from typing import Callable


#   EXTERNAL IMPORTS
import flxr
from flxr.common.protocols import Flux


#   MODULE CLASS
class Fwm(ABC):
    def __init__(self, hfw: Flux, cls: type) -> None:
        """ FLUX runtime framework module abstract """
        self.__framework: Flux = self.__validate_hfw(hfw)
        self.__class: type = self.__validate_class(cls)
        self.__injectables: list = []

    def framework(self) -> Flux:
        """ Returns module hosting
        framework instance """
        return self.__framework

    @property
    def hfw(self) -> Flux:
        """ Hosting framework """
        return self.framework()

    def fwm_class(self) -> type:
        """ Returns module type """
        return self.__class

    def fwm_name(self) -> str:
        """ Returns module type name """
        return self.fwm_class().__name__

    def fwm_clearance(self) -> int:
        """ Returns module framework
        service security clearance """
        return self.hfw.class_clearance(cls=self.fwm_class())

    def hfw_service(self, svc: str, **svc_args) -> any:
        """ Execute specified
        framework service """
        return self.hfw.service(requestor=self.fwm_class())[svc](**svc_args)

    def process_proxy(self) -> dict:
        """ Returns hosting framework
        process proxy """
        # TODO: Retrieve process proxy dict directly from hfw instance

    @staticmethod
    def threaded() -> bool: return False

    def console(self, msg: str, error: bool = False, **kwargs) -> None:
        """ Send text to the framework
        console for logging """
        self.hfw_service(svc='console', msg=msg, error=error, **kwargs)

    def exception(self, excinfo: tuple, **kwargs) -> None:
        """ Record module exception
        in framework log """
        self.hfw_service(svc='exception', cls=self.fwm_class(), excinfo=excinfo, **kwargs)

    def load_injector(self, load: list[tuple[str, Callable, int]]) -> None:
        """ Append specified module
        methods to service injector """
        for injectable in load:
            if type(injectable) is tuple:
                _call, _func, _clearance = injectable
                self.__injectables.append(
                    {'call': _call, 'func': _func, 'clearance': _clearance}
                )

    def inject_services(self) -> None:
        """ Send loaded module services
        to framework service host """
        if len(self.__injectables) == 0:
            return
        self.console(msg=f"Injecting {self.fwm_name()} services:")
        for _injectable in self.__injectables:
            self.hfw.inject_service(
                call=_injectable.get('call'),
                cls=self.fwm_class(),
                func=_injectable.get('func'),
                clearance=_injectable.get('clearance')
            )
        self.console(msg=f"Successfully injected {len(self.__injectables)} services")
        self.__injectables.clear()

    def extend_permissions(self, cls: type, **kwargs) -> None:
        """ Extend module permissions
        to another class """
        self.console(msg=f"Extending permissions to {cls.__name__}...")
        self.hfw_service(
            svc='wcls',
            requestor=self.fwm_class(),
            cls=cls,
            admin=kwargs.get('admin', False),
            clearance=kwargs.get('clearance', self.fwm_clearance())
        )

    @staticmethod
    def __invalid_parameter(param: str, value) -> None:
        """ Raises value error on
        an invalid parameter """
        raise ValueError(
            f"Invalid value for {param} parameter: {value}"
        )

    def __validate_hfw(self, hfw) -> Flux:
        """ Validate hosting
        framework parameter """
        try:
            if (hfw.is_rfw()) and (type(hfw) is flxr.Flxr):
                return hfw
            raise AttributeError
        except AttributeError:
            self.__invalid_parameter('hfw', hfw)

    def __validate_class(self, cls) -> type:
        """ Validate class
        type parameter """
        if not isinstance(cls, type):
            self.__invalid_parameter('cls', cls)
        return cls
