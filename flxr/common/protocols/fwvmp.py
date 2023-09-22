
"""
FLUX Runtime Framework View Module Protocol
"""


#   BUILT-IN IMPORTS
from typing import Protocol
from flxr.utility.clientm import ClientManager
from .fwp import Flux


#   PROTOCOL
class FwV(Protocol):
    """ FLUX runtime framework view module protocol """

    #   Framework View Module (FwVm) Based
    def __init__(self, hfw: Flux, cls: type, uid: str, parent: any = None, **kwargs) -> None: ...
    def uid(self) -> str: ...
    def view_type(self) -> str: ...

    @property
    def uclient(self) -> ClientManager: ...

    @property
    def properties(self) -> any: ...

    @property
    def view(self) -> any: ...

    @property
    def event(self) -> any: ...

    def present(self, view: str) -> None: ...
    def hide(self) -> None: ...
    def show(self) -> None: ...
    def take_focus(self) -> None: ...

    #   Framework Module (Fwm) Based
    def hfw(self) -> Flux: ...
    def framework(self) -> Flux: ...
    def fwm_class(self) -> type: ...
    def fwm_name(self) -> str: ...
    def hfw_service(self, svc: str, **svc_args) -> any: ...
    def console(self, msg: str, error: bool = False, **kwargs) -> None: ...
    def extend_permissions(self, cls, admin): ...

    #   Tkinter Based
    def winfo_width(self): ...
    def winfo_height(self): ...
    def winfo_rootx(self): ...
    def winfo_rooty(self): ...
    def config(self, **kwargs): ...
    def geometry(self, param): ...
    def rowconfigure(self, param, weight): ...
    def columnconfigure(self, param, weight): ...
    def update(self): ...
    def bind(self, event, func, **kwargs): ...
