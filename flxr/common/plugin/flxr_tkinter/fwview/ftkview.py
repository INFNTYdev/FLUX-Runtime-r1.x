
"""
Base FLUX Runtime Framework View Module
"""


#   BUILT-IN IMPORTS
pass


#   EXTERNAL IMPORTS
from .fwvm import FwVm


#   MODULE CLASS
class FTkView(FwVm):
    def __init__(self, hfw, cls: type, uid: str, parent: any, **kwargs) -> None:
        """ Base framework view """
        super().__init__(hfw=hfw, cls=cls, uid=uid, parent=parent, **kwargs)

    @staticmethod
    def view_type() -> str:
        return FTkView.__name__

    @property
    def properties(self) -> any:
        pass

    @property
    def event(self) -> any:
        pass

    def hide(self) -> None:
        pass

    def show(self) -> None:
        pass

    def take_focus(self) -> None:
        pass
