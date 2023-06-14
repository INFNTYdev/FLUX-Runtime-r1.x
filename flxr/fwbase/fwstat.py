
""" Framework Status Module """

#   MODULE IMPORTS
from flxr import *


#   MODULE CLASSES
class StatusManager:
    def __init__(self, fwmods: list, svc: dict) -> None:
        """
        FLUX Runtime-Engine status manager

        :param fwmods: The list of deployable framework modules
        :param svc: Hosting framework base services
        """

        self._svc: dict = svc
        self._status: dict = {}
        self._populate(fwmods)

    def set(self, module: any, status: bool) -> None:
        """
        Set the status of a framework module
        
        :param module: Any registered framework module class
        :param status: The status in which to set the module
        """
        if class_of(module) in self._status.keys():
            self._status[class_of(module)][1] = status
            if status is True:
                self._svc['console'](msg=f'{class_of(module).__name__} ready')
            return

        raise KeyError(
            f"Invalid status set request for non-existing '{class_of(module).__name__}' module"
        )

    def get(self, module: any) -> bool:
        """
        Returns the status of the requested module
        
        :param module: Any registered framework module class
        :return: The status of the requested module
        """
        try:
            return self._status[module][1]
        except KeyError:
            try:
                return self._status[class_of(module)][1]
            except KeyError:
                return False

    def include(self, module: any, core: bool = False, status: bool = False) -> None:
        """
        Include new module class in status manager
        
        :param module: Any registered framework module class
        :param core: Core module indicator
        :param status: Current status of the new module
        """
        if inspect.isclass(module):
            self._status[module] = [core, status]
            self._svc['console'](msg=f'Added {module.__name__} module to status manager')
        else:
            self._status[class_of(module)] = [core, status]
            self._svc['console'](msg=f'Added {class_of(module).__name__} module to status manager')

    def core_active(self) -> bool:
        """ Determines if all core modules are active """
        return all(_stats[1] for cls, _stats in self._status.items() if _stats[0] is True)

    def all_active(self) -> bool:
        """ Determines if all framework modules are active """
        return all(_stats[1] for cls, _stats in self._status.items())

    @staticmethod
    def _same_type(type_a: any, type_b: any) -> bool:
        """ Compares two items for relation """
        return isinstance(type_a, type_b) or isinstance(type_b, type_a)

    def _populate(self, m: list) -> None:
        """ Populate the framework status dictionary """
        self._status = {
            _mod[1]: [True, False] if _mod[0][-1] == '*'
            else [False, False] for _mod in m
        }
