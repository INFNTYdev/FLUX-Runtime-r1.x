
"""
FLUX Runtime Framework Protocol
"""


#   BUILT-IN IMPORTS
from typing import Protocol, Union
from flxr.utility import ClientManager


#   PROTOCOL
class Flux(Protocol):
    """ FLUX runtime framework class protocol """
    def developer_mode(self) -> bool: ...
    def active(self) -> bool: ...
    def in_shutdown(self) -> bool: ...
    def fatal_error(self) -> bool: ...
    def startup_time(self) -> float: ...
    def deployable_count(self) -> int: ...
    def services_enabled(self) -> bool: ...
    def base_service(self) -> dict: ...
    def client(self) -> ClientManager: ...
    def class_clearance(self, cls: type) -> int: ...
    def service(self, requestor, base: bool = False) -> dict: ...
    def inject_service(self, call: str, cls: type, func, clearance: int = 0) -> None: ...
    def attach_window(self, cls: type, **kwargs) -> None: ...
    def set_main_window(self, window: Union[str, type]) -> None: ...
    def run(self) -> None: ...

    @staticmethod
    def is_rfw() -> bool: ...

    def framework_exit(self) -> None: ...
