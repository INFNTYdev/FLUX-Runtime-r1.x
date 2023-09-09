
"""
FLUX Runtime Framework Threaded Module Abstraction
"""


#   BUILT-IN IMPORTS
from abc import ABC, abstractmethod


#   EXTERNAL IMPORTS
from flxr.common.protocols import Flux
from .fwm import Fwm


#   ABSTRACTION
class FwmT(Fwm, ABC):
    def __init__(self, hfw: Flux, cls: type) -> None:
        super(Fwm, self).__init__(hfw=hfw, cls=cls)

    def start_module(self) -> None: ...
    def stop_module(self) -> None: ...
    def last_update_made(self, datetime) -> None: ...
    def polling_rate(self) -> float: ...
    def last_updated(self) -> any: ...
    def set_poll(self, requestor, rate: float) -> None: ...
    def reset_poll(self) -> None: ...
