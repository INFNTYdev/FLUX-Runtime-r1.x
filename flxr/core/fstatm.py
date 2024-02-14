
"""
Framework Status Manager Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
pass


#   EXTERNAL IMPORTS
from flxr.common.core import Fwm
from flxr.constant import GlobalFuncs


#   MODULE CLASS
class StatusManager(Fwm):
    def __init__(self, hfw, deployable: list) -> None:
        """ Framework module status manager """
        super().__init__(hfw=hfw, cls=StatusManager)
        self.__status: dict = {}
        self.__set_initial_modules(deployable)

    def existing_module(self, module) -> bool:
        """ Returns true if provided type is
        recorded in status """
        return GlobalFuncs.class_of(module) in self.__status.keys()

    def get(self, module) -> bool:
        """ Returns status of provided framework module """
        if not self.existing_module(module):
            return False
        return self.__status[GlobalFuncs.class_of(module)]['status']

    def core_active(self) -> bool:
        """ Returns true if all
        core modules are active """
        pass

    def all_active(self) -> bool:
        """ Returns true if all deployable
        modules are active """
        for _module in self.__status.keys():
            if not self.__status[_module]['status']:
                return False
        return True

    def set(self, module, status: bool) -> None:
        """ Set status of provided framework module """
        if not self.existing_module(module):
            return
        self.__status[GlobalFuncs.class_of(module)]['status'] = status
        _indicator: str = 'disabled'
        if status is True:
            _indicator: str = 'ready'
        self.console(msg=f"{GlobalFuncs.class_of(module).__name__} module {_indicator}")

    def include(self, module, core: bool = False, status: bool = False) -> None:
        """ Include new framework module in
        status manager """
        pass

    def __set_initial_modules(self, deployable: list) -> None:
        """ Include initial framework modules
        in status manager """
        for _module in deployable:
            self.__status[_module[1]] = {'core': False, 'status': False}
            if _module[0][-1] == '*':
                self.__status[_module[1]]['core'] = True
