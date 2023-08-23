
"""
Framework Status Manager Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
pass


#   EXTERNAL IMPORTS
from flxr.constant import GlobalFuncs
from .fwmod import FrameworkModule


#   MODULE CLASS
class StatusManager(FrameworkModule):
    def __init__(self, deployable: list, hfw) -> None:
        """ Framework module status manager """
        super().__init__(hfw=hfw, cls=StatusManager)
        self._status: dict = {}

    def set(self, module, status: bool) -> None:
        """ Set the status of a framework module """
        pass

    def get(self, module) -> bool:
        """ Returns the status of a framework module """
        try:
            return self._status[GlobalFuncs.class_of(module)][1]
        except KeyError as InvalidModule:
            return False

    def include(self, module, core: bool = False, status: bool = False) -> None:
        """ Include new framework module in status manager """
        pass

    def core_active(self) -> bool:
        """ Returns true if all core modules are active """
        pass

    def all_active(self) -> bool:
        """ Returns true if all deployable modules are active """
        pass
