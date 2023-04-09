
""" Framework status module """


# MODULE IMPORTS
from flxr import *

# MODULE PACKAGE
__package__ = pkg_n()


# MODULE CLASSES
class StatusManager:
    def __init__(self, fwmods: list, svc: dict):
        """
        Framework status manager

        :param fwmods: Framework module manifest
        """

        self._svc: dict = svc

        self._status: dict = {}
        self._populate_status(fwmods)

    def set(self, module: any, active: bool):
        """ Set the active status of a system module """
        try:
            self._status[module][1] = active
            if active is True:
                self._svc['console'](f"{module.__name__} ready")
        except Exception:
            for m in self._status.keys():
                if self._same_type(type_a=m, type_b=module):
                    self._status[m][1] = active
                    if active is True:
                        self._svc['console'](f"{module.__class__.__name__} ready")
                    return

    def get(self, module: any) -> bool:
        """ Returns the active status of a system module """
        try:
            return self._status[module][1]
        except Exception:
            for m in self._status.keys():
                if self._same_type(type_a=m, type_b=module):
                    return self._status[m][1]

    def include(self, module: any, core: bool = False, activity: bool = False):
        """ Include a module class into the status manager """
        if inspect.isclass(module):
            self._status[module] = [core, activity]
            self._svc['console'](f"Added '{module.__name__}' module to status manager")
        else:
            self._status[module.__class__] = [core, activity]
            self._svc['console'](f"Added '{module.__class__.__name__}' module to status manager")

    def core_modules_active(self) -> bool:
        """ Determnies if all required modules are active """
        for cls, stats in self._status.items():
            if (stats[0] is True) and (stats[1] is False):
                return False
        return True

    def all_modules_active(self) -> bool:
        """ Determines if all modules are active """
        for cls, stats in self._status.items():
            if stats[1] is False:
                return False
        return True

    @staticmethod
    def _same_type(type_a: any, type_b: any) -> bool:
        """ Compares two items for relation """
        if ('object' in str(type_a)) and ('object' in str(type_b)):
            if type_a.__class__ is type_b.__class__:
                return True
        elif (inspect.isclass(type_a)) and (inspect.isclass(type_b)):
            if type_a is type_b:
                return True
        elif (inspect.isclass(type_a)) and ('object' in str(type_b)):
            if isinstance(type_b, type_a):
                return True
        elif ('object' in str(type_a)) and (inspect.isclass(type_b)):
            if isinstance(type_a, type_b):
                return True
        return False

    def _populate_status(self, modules: list):
        """ Populate framework module status' """
        for m in modules:
            if m[0][-1] == '*':
                self._status[m[1]] = [True, False]
            else:
                self._status[m[1]] = [False, False]
