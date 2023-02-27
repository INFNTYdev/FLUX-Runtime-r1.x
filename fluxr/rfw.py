
""" FLUX Runtime-Engine Framework """


#   MODULE IMPORTS
from fluxr import *
from .stat import FrameworkStatusManager
from .exc import FrameworkExceptionManager
from .svc import ServiceProvider
from .sys_thread import SystemThreadManager
...


#   MODULE PACKAGE
__package__ = pkg_n()


#   MODULE CLASSES
class RuntimeFramework:

    __SYS_MODULES: list = [
        [SystemThreadManager, False],
    ]

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
            self.__svc: ServiceProvider = ServiceProvider(
                fw=self,
                whitelist=[(self.__stat, 'high'), (self.__exc, 'high')]
            )
            self.__asset_chain[ServiceProvider] = self.__svc
            self.__set_module_status(ServiceProvider, True)
            self.console_out("Successfully initialized service provider")
            self.__inject_base_services()
        except SvcFailureError as SvcFailure:
            self.console_out(SvcFailure.notice, error=True)
            self.system_exit(code=SVC_FAILURE)
        except BaseException as SvcFailure:
            self.console_out(f"\n\n\t[ RUNTIME SVC ERROR ] : {SvcFailure}")
            self.system_exit(code=SVC_FAILURE)

        for module in self.__SYS_MODULES:
            try:
                self.console_out(f"Initializing {module[0].__name__}...")
            except BaseException as Unknown:
                self.exception(self, Unknown, sys.exc_info(), unaccounted=True,
                               pointer='__init__()')
                self.console_out(f"An error occurred initializing {str(module[0].__name__)}", error=True)

        if kwargs.get('application') is not None:
            pass
        else:
            pass

        self.__start_up = False
        self.console_out("Runtime framework ready")
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

    def service_call(self, requestor: any) -> dict:
        """ Returns appropriate services to requestor """
        if self.__get_module_status(ServiceProvider):
            return self.__svc.serve(requestor)
        return

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

    # SERVICE METHODS
    def __whitelist_class(self, requestor: any, cls: any, **kwargs):
        """ Add a class to the providers whitelist """
        self.__svc.whitelist_class(requestor=requestor, cls=cls, **kwargs)
        self.console_out(f"Added '{requestor}' to provider whitelist")
        return

    def __authorize_class(self, requestor: any, cls: any):
        """ Add a class to the providers administration """
        self.__svc.authorize_class(requestor=requestor, cls=cls)
        return

    def __implement_service(self, call: str, cls: any, func: any, **kwargs):
        """ Add a function reference to the service provider """
        self.__svc.new_service(call=call, cls=cls, func=func, **kwargs)
        self.console_out(f"Successfully added '{self.__readable_func_name(func)}' to services")
        return

    # BASEMENT METHODS
    def __inject_base_services(self):
        """ Add low-level framework services to provider """
        self.__implement_service('gstat', self.__stat, self.__get_module_status, clearance='any')
        self.__implement_service('sstat', self.__stat, self.__set_module_status, clearance='low')
        self.__implement_service('cstat', self.__stat, self.__core_active, clearance='any')
        self.__implement_service('astat', self.__stat, self.__stat.all_systems_active, clearance='any')
        self.__implement_service('exc', self.__exc, self.__all_active, clearance='any')
        self.__implement_service('nsvc', self.__svc, self.__implement_service, clearance='any')
        self.__implement_service('wcls', self.__svc, self.__whitelist_class, clearance='any')
        self.__implement_service('acls', self.__svc, self.__authorize_class, clearance='any')
        return

    def __runnable(self) -> bool:
        """ Determines if system conditions are appropriate """
        return

    @staticmethod
    def __readable_func_name(func: any) -> str:
        """ Format function name to readable text """
        n: str = ''
        for index in range(0, len(str(func.__name__))):
            if str(func.__name__)[index] != '_':
                n += str(func.__name__)[index]
            else:
                if index > 1:
                    n += ' '
        return n

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
