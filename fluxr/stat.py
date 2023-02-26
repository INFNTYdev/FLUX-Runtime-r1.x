
""" FLUX Runtime-Engine Framework Status Manager """


#   MODULE IMPORTS
from fluxr import *


#   MODULE PACKAGE
__package__ = pkg_n()


#   MODULE CLASSES
class FrameworkStatusManager:
    def __init__(self):
        """ Framework status module """
        self.__status: dict = {
            'exception_ready*': [FrameworkExceptionManager, False],
            'service_ready*': [ServiceProvider, False],
            # '#_ready': [None, False],
            # '#_ready': [None, False],
            # '#_ready': [None, False],
            # '#_ready': [None, False],
            # '#_ready': [None, False],
            # '#_ready': [None, False],
            # '#_ready': [None, False],
            # '#_ready': [None, False],
            'framework_ready': [RuntimeFramework, False],
        }
        return

    def get(self, module: any) -> bool:
        """ Returns the status of the requested module """
        if self.__status_exist(module):
            if type(module) is str:
                if self.__is_shortened(module):
                    return bool(self.__status[str(module+'_ready')][1])
                return bool(self.__status[module][1])
            else:
                return self.__get_status_by_class(module)
        else:
            pass
        return

    def set(self, module: any, status: bool):
        """ Set the status of a system module """
        if self.__status_exist(module):
            if type(module) is str:
                if self.__is_shortened(module):
                    self.__status[str(module+'_ready')][1] = status
                else:
                    self.__status[module][1] = status
            else:
                self.__set_status_by_class(module, status)
        else:
            pass
        return

    def core_systems_active(self) -> bool:
        """ Determines if required modules are active """
        for mod in [x for x in self.__status.keys()]:
            if (mod[-1] == '*') and (not bool(self.__status[mod][1])):
                return False
        return True

    def all_systems_active(self) -> bool:
        """ Determines if all modules are actvie """
        for mod in [x for x in self.__status.keys()]:
            if not self.__status[mod][1]:
                return False
        return True

    @staticmethod
    def __is_shortened(s_key: str) -> bool:
        """ Determines if provided status key is shortened """
        if (s_key.lower()).__contains__('_ready'):
            return False
        else:
            if len(s_key) > 0:
                return True
        return False

    @staticmethod
    def __shorten(s_key: str) -> str:
        """ Returns a shortened module status key """
        short: str = ''
        for char in s_key:
            if char != '_':
                short += char
            else:
                break
        return short

    def __get_status_by_class(self, module: any) -> bool:
        """ Retrieves a modules status by class """
        for k in [x for x in self.__status.keys()]:
            if (self.__status[k][0] == type(module))\
                    or (self.__status[k][0] == module):
                return bool(self.__status[k][1])
        return None

    def __set_status_by_class(self, module: any, status: bool):
        """ Set the status of a module by class """
        for k in [x for x in self.__status.keys()]:
            if (self.__status[k][0] == type(module)) \
                    or (self.__status[k][0] == module):
                self.__status[k][1] = status
                break
        return

    def __status_exist(self, module: any) -> bool:
        """ Determines if the provided modules status exist """
        for k in [x for x in self.__status.keys()]:
            if type(module) is str:
                if (module == k) or (module == self.__shorten(k)):
                    return True
            else:
                if (type(module) == self.__status[k][0])\
                        or (module == self.__status[k][0]):
                    return True
        return False
