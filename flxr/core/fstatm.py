
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
        self._set_initial_modules(deployable)

    def set(self, module, status: bool) -> None:
        """ Set the status of a framework module """
        if not self.existing_module(module):
            return

        self._status[GlobalFuncs.class_of(module)]['status'] = status
        _indicator: str = 'disabled'
        if status is True:
            _indicator: str = 'ready'
        self.console(msg=f"{GlobalFuncs.class_of(module).__name__} module {_indicator}")

    def get(self, module) -> bool:
        """ Returns the status of a framework module """
        try:
            return self._status[GlobalFuncs.class_of(module)]['status']
        except KeyError as InvalidModule:
            return False

    def include(self, module, core: bool = False, status: bool = False) -> None:
        """ Include new framework module in
        status manager """
        pass

    def core_active(self) -> bool:
        """ Returns true if all core modules
        are active """
        pass

    def all_active(self) -> bool:
        """ Returns true if all deployable modules
        are active """
        pass

    def existing_module(self, module) -> bool:
        """ Returns true if the provided type is
        recorded in status """
        return GlobalFuncs.class_of(module) in self._status.keys()

    def _set_initial_modules(self, deployable: list) -> None:
        """ Include the initial framework modules
        in status manager """
        for _module in deployable:
            self._status[_module[1]] = {'core': False, 'status': False}
            if _module[0][-1] == '*':
                self._status[_module[1]]['core'] = True
