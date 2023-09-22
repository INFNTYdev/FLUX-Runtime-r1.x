
"""
FLUX Runtime Framework View Abstract
"""


#   BUILT-IN IMPORTS
from abc import ABC, abstractmethod


#   EXTERNAL IMPORTS
from flxr.common.core import Fwm
from .utility import FwvHost, FwvPropertyManager, FwvEventHandler
from flxr.utility import ClientManager


#   MODULE CLASS
class FwVm(Fwm, ABC):
    def __init__(self, hfw, cls: type, uid: str, parent: any = None, **kwargs) -> None:
        """ Framework view module abstract """
        super().__init__(hfw=hfw, cls=cls)
        self.__identifier: str = str(uid)
        self.__view_host: FwvHost = FwvHost(fwv=self)

    def uid(self) -> str:
        """ Returns framework view unique identifier """
        return self.__identifier

    @staticmethod
    @abstractmethod
    def view_type() -> str:
        """ Returns framework view base type """
        ...

    @property
    def uclient(self) -> ClientManager:
        """ Hosting framework client manager """
        return self.hfw.client()

    @property
    @abstractmethod
    def properties(self) -> FwvPropertyManager:
        """ Framework view property manager """
        ...

    @property
    def view(self) -> FwvHost:
        """ Framework view view host """
        return self.__view_host

    @property
    @abstractmethod
    def event(self) -> FwvEventHandler:
        """ Framework view event handler """
        ...

    def present(self, view: str) -> None:
        """ Display specified
        hosted framework view """
        # TODO: Setup view presentation logic

    @abstractmethod
    def hide(self) -> None:
        """ Hide framework view """
        ...

    @abstractmethod
    def show(self) -> None:
        """ Show framework view """
        ...

    @abstractmethod
    def take_focus(self) -> None:
        """ Give framework view focus """
        ...
