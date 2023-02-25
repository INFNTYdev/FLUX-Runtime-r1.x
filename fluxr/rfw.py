
""" FLUX Runtime-Engine Framework """


#   MODULE IMPORTS
from fluxr import *
from .stat import FrameworkStatusManager
from .exc import FrameworkExceptionManager
from .svc import ServiceProvider
...


#   MODULE PACKAGE
__package__ = pkg_n()


#   MODULE VARS
__SYS_MODULES: list = [
    None,
]


#   MODULE CLASSES
class RuntimeFramework:
    def __init__(self, dev: bool = True, **kwargs):
        """ Runtime-engine framework """
        self.run: bool = True
        self.dev: bool = dev
        self.__start_up: bool = True
        self.__fatal_error: bool = False
        self.__asset_chain: dict = {}
        self.__META_REF = kwargs.get('meta')
        self.__APPLICATION = kwargs.get('application')

        self.__status: FrameworkStatusManager = FrameworkStatusManager()
        return

    def system_exit(self, **kwargs):
        """ Shutdown runtime-engine """
        return

    def __runnable(self) -> bool:
        """ Determines if system conditions are appropriate """
        return

    def __console_out(self):
        """ Send text to the console """
        return

    def __master_console_out(self, **kwargs):
        """ Master console output """
        return
