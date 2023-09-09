
"""
FLUX Runtime Framework Module Abstraction
"""


#   BUILT-IN IMPORTS
from abc import ABC, abstractmethod
import time


#   EXTERNAL IMPORTS
from flxr.common.protocols import Flux


#   ABSTRACTION
class Fwm(ABC):
    """ FLUX runtime framework
    module abstraction class """
    def __init__(self, hfw: Flux, cls: type) -> None:
        self.__framework: Flux = self._validate_hfw(hfw)
        self.__type: type = cls
        self.__injectables: list = []

    @property
    def fwm_type(self) -> type: return self.__class__
    @property
    def fw_clearance(self) -> int: return self.fw_svc('clvl')
    @property
    def status(self) -> bool: return self.fw_svc('getstat', module=self.fwm_type)

    @abstractmethod
    def threaded_module(self) -> bool: ...
    @abstractmethod
    def console(self, msg: str, error: bool = False, **kwargs) -> None: ...

    def framework(self) -> Flux: return self.__framework

    def fw_svc(self, svc: str, **kwargs) -> any:
        return self.framework().service(self.__type, root=kwargs.pop('root', False))[svc](**kwargs)

    def process_proxy(self) -> dict: return self.fw_svc('pproxy')

    def set_status(self, status: bool) -> None: self.fw_svc('setstat', module=self.fwm_type, status=status)

    def to_service_injector(self, load: list[tuple]) -> None:
        for _injectable in load:
            if type(_injectable) is tuple:
                self.__injectables.append(
                    {'call': _injectable[0], 'func': _injectable[1], 'clearance': _injectable[2]}
                )

    def inject_services(self) -> None:
        for _injectable in self.__injectables:
            self.__framework.inject_service(
                call=_injectable['call'],
                cls=self.__type,
                func=_injectable['func'],
                clearance=_injectable['clearance']
            )
        self.__injectables.clear()

    def extend_permissions(self, cls: type, **kwargs) -> None:
        self.fw_svc(
            svc='wcls',
            requestor=self.__type,
            cls=cls,
            admin=kwargs.get('admin', False),
            clearance=kwargs.get('clearance', 1)
        )

    def exception(self, cls: type, excinfo: tuple, **kwargs) -> None:
        pass

    @staticmethod
    def wait(secs: float) -> None: time.sleep(secs)

    @staticmethod
    def _validate_hfw(hfw: Flux) -> Flux:
        try:
            if hfw.is_rfw():
                return hfw
        except AttributeError as NonFluxObject:
            pass
