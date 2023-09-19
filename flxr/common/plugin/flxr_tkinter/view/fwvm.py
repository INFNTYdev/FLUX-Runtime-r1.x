
"""
Base FLUX Framework View Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
from abc import ABC, abstractmethod


#   EXTERNAL IMPORTS
from flxr.common.core import Fwm
from flxr.common.protocols import Flux
from .vpm import FwvPropertyManager
from .vhost import FwvHost
from .vevent import FwvEventHandler


#   MODULE CLASS
class FwVm(Fwm, ABC):
    def __init__(self, hfw: Flux, cls: type, uid: str, parent: any = None, **kwargs) -> None:
        """ Base FLUX runtime framework view module """
        super().__init__(hfw=hfw, cls=cls)
        self.__identifier: str = uid
        self.__properties: FwvPropertyManager = FwvPropertyManager(client=self)
        self.__views: FwvHost = FwvHost(client=self)
        self.__event_handler: FwvEventHandler = FwvEventHandler(client=self)

    def identifier(self) -> str:
        """ Returns framework view identifier """
        return self.__identifier

    @property
    def client(self) -> None:
        """ Returns framework client manager """
        return None

    @property
    def properties(self) -> FwvPropertyManager:
        """ Returns framework view property manager """
        return self.__properties

    @property
    def views(self) -> FwvHost:
        """ Returns view host """
        return self.__views

    @property
    def event(self) -> FwvEventHandler:
        """ Returns framework view event handler """
        return self.__event_handler

    def present(self, view: str) -> None:
        """ Display specified hosted framework view """
        pass

    @abstractmethod
    def hide(self) -> None: ...

    @abstractmethod
    def show(self) -> None: ...

    @abstractmethod
    def take_focus(self) -> None: ...
