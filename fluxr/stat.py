
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
        return

    def set(self, module: any, status: bool):
        """ Set the status of a system module """
        return

    def core_systems_active(self) -> bool:
        """ Determines if required modules are active """
        return

    def all_systems_active(self) -> bool:
        """ Determines if all modules are actvie """
        return

    def __status_exist(self, module: any) -> bool:
        """ Determines if the provided modules status exist """
        return
