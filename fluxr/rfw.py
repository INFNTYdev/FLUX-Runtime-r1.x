
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
    def __init__(self, dev: bool = False, **kwargs):
        """ Runtime-engine framework """
        self.run: bool = True
        self.dev: bool = dev
        self.__start_up: bool = True
        self.__fatal_error: bool = False
        self.__asset_chain: dict = {}
        self.__META_REF = kwargs.get('meta')
        self.__APPLICATION = kwargs.get('application')
        self.__stat: FrameworkStatusManager = FrameworkStatusManager()
        self.__asset_chain[FrameworkStatusManager] = self.__stat
        self.console_out("Initializing runtime framework...", skip=True)
        
        try:
            self.__exc: FrameworkExceptionManager = FrameworkExceptionManager(fw=self)
            self.__asset_chain[FrameworkExceptionManager] = self.__exc
            self.__set_module_status(FrameworkExceptionManager, True)
            self.console_out("Successfully initialized exception manager")
        except ExcFailureError as ExcFailure:
            self.console_out(ExcFailure.notice, error=True)
            self.system_exit(code=EXC_FAILURE)
        except BaseException as ExcFailure:
            self.console_out(f"\n\n\t[ RUNTIME EXC ERROR ] : {ExcFailure}")
            self.system_exit(code=EXC_FAILURE)

        try:
            self.__svc: ServiceProvider = ServiceProvider(fw=self)
            self.__asset_chain[ServiceProvider] = self.__svc
            self.__set_module_status(ServiceProvider, True)
            self.console_out("Successfully initialized service provider")
        except SvcFailureError as SvcFailure:
            self.console_out(SvcFailure.notice, error=True)
            self.system_exit(code=SVC_FAILURE)
        except BaseException as SvcFailure:
            self.console_out(f"\n\n\t[ RUNTIME SVC ERROR ] : {SvcFailure}")
            self.system_exit(code=SVC_FAILURE)

        ...
        return

    # CORE METHODS
    def console_out(self, text: str, **kwargs):
        """ Send text to the console """
        self.__master_console_out(text=text, **kwargs)
        return

    def exception(self, cls: any, exc_o: any, exc_info: tuple, **kwargs):
        """ Handle system raised exceptions """
        self.__exc.exception(cls, exc_o, exc_info, **kwargs)
        return

    def base_services(self) -> dict:
        """ Provides access to basic framework services """
        return {
            'console': self.console_out,
            'exc': self.exception,
            'exit': self.system_exit
        }

    def system_exit(self, **kwargs):
        """ Shutdown runtime-engine """
        exit(kwargs.get('code', DEFAULT_EXIT))

    @staticmethod
    def is_fw() -> bool:
        """ Confirm runtime-engine object """
        return True

    # STATUS METHODS
    def __set_module_status(self, module: any, status: bool):
        """ Set the status of a system module """
        self.__stat.set(module, status)
        return

    def __get_module_status(self, module: any) -> bool:
        """ Get the current status of a system module """
        return self.__stat.get(module)

    def __core_active(self) -> bool:
        """ Determines if required modules are active """
        return self.__stat.core_systems_active()

    def __all_active(self) -> bool:
        """ Determines if all modules are actvie """
        return self.__stat.all_systems_active()

    # EXCEPTION METHODS
    pass

    # BASEMENT METHODS
    def __runnable(self) -> bool:
        """ Determines if system conditions are appropriate """
        return

    def __master_console_out(self, **kwargs):
        """ Master console output """
        try:
            if (kwargs.get('root', False)) or (not self.__get_module_status('console')):
                p_str: str = f"\t{kwargs.get('prefix', '')}- >  "
                if kwargs.get('error', False):
                    p_str += "[ ERROR ] : "
                p_str += kwargs.get('text')
                if kwargs.get('skip', False):
                    p_str = f'\n{p_str}'
                if self.dev:
                    print(p_str)
            else:
                pass
        except BaseException as Unknown:
            pass
        finally:
            return
