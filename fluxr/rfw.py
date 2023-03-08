
""" FLUX Runtime-Engine Framework """

#   MODULE IMPORTS
from fluxr import *
from .sys_stat import FrameworkStatusManager
from .exc import FrameworkExceptionManager
from .svc import ServiceProvider
from .sys_thread import SystemThreadManager
from .sys_datetime import SystemDatetimeManager
from .sys_rt import SystemRuntimeClock
from .sys_console import SystemConsoleManager
from .sys_io import SystemFileIOManager
from .sys_watch import SystemMonitor

#   MODULE PACKAGE
__package__ = pkg_n()


#   MODULE CLASSES
class RuntimeFramework:
    __SYS_MODULES: list = [
        [SystemThreadManager, False],
        [SystemDatetimeManager, True],
        [SystemRuntimeClock, True],
        [SystemConsoleManager, True],
        [SystemFileIOManager, True],
        [SystemMonitor, True],
    ]

    def __init__(self, dev: bool = False, **kwargs):
        """ Runtime-engine framework """
        self.run: bool = True
        self.dev: bool = dev
        self.__start_up: bool = True
        self.__app_active: bool = False
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
                self.__whitelist_class(self, module[0], clearance='high')
                self.__asset_chain[module[0]] = module[0](fw=self, svc_c=self.service_call)
                if module[1]:
                    try:
                        self.console_out(f"Starting {module[0].__name__}...")
                        self.asset_function(module[0], 'start')
                        self.console_out(f"{module[0].__name__} thread active")
                    except BaseException as Unknown:
                        self.exception(self, Unknown, sys.exc_info(), unaccounted=True,
                                       pointer='__init__()')
                        self.console_out(f"Failed to start {module[0].__name__} thread", error=True)
                else:
                    self.__set_module_status(module[0], True)
                    self.console_out(f"{module[0].__name__} ready")
            except BaseException as Unknown:
                self.exception(self, Unknown, sys.exc_info(), unaccounted=True,
                               pointer='__init__()')
                self.console_out(f"An error occurred initializing {str(module[0].__name__)}", error=True)

        if self.__core_status():
            if kwargs.get('application') is not None:
                self.console_out("Initializing application...")
                self.__whitelist_class(self, kwargs.get('application'), clearance='high')
                try:
                    self.__APPLICATION = kwargs.get('application')(fw=self, svc_c=self.app_service_call)
                except TypeError as ImproperAppArgSetup:
                    self.__fatal_error = True
                    self.exception(self, ImproperAppArgSetup, sys.exc_info(), pointer='__init__()')
                    self.console_out(MISSING_APP_ARGS, error=True)
                except BaseException as Unknown:
                    self.__fatal_error = True
                    self.exception(self, Unknown, sys.exc_info(), unaccounted=True,
                                   pointer='__init__()')
                    self.console_out("An error occurred intializing the application", error=True)
                if not self.__fatal_error:
                    self.__set_module_status('application', True)
                    self.console_out("Application ready")
                else:
                    self.console_out(APP_FAIL_NOTICE, error=True)
            else:
                self.console_out("No application provided")
            if not self.__fatal_error:
                self.__start_up = False
                self.console_out("Runtime framework ready")
                self.__set_module_status(self, True)
                return
            else:
                self.console_out("FAILED TO INTIALIZE APPLICATION", error=True)
                self.asset_function(SystemConsoleManager, 'pause')
                input(APP_FAIL_NOTICE)
                self.system_exit(code=APP_FAILURE)
        else:
            self.asset_function(SystemConsoleManager, 'pause')
            input(RFW_FAIL_NOTICE)
            self.system_exit(code=RFW_FAILURE)

    # CORE METHODS
    def console_out(self, text: str, **kwargs):
        """ Send text to the console """
        self.__master_console_out(text=text, **kwargs)
        return

    def invoke_application(self):
        """ Launch embedded application """
        try:
            self.console_out("Launching application...")
            self.__app_active = True
            self.__APPLICATION.mainloop()
        except BaseException as Unknown:
            self.__app_active = False
            self.exception(self, Unknown, sys.exc_info(), unaccounted=True,
                           pointer='invoke_application()')
            self.console_out("A fatal error occurred in the application", error=True)
        finally:
            self.__app_active = False
            self.console_out("Application has stopped")
            self.system_exit(code=CLEAN)

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

    def app_service_call(self, requestor: any) -> dict:
        """ Returns services to application """
        if requestor.rfw_executable():
            return self.__svc.serve(self)
        return

    def asset_function(self, cls: type or str, func: str, **kwargs):
        """ Execute the function of a system asset """
        for asset in self.__asset_chain.keys():
            if inspect.isclass(cls):
                if asset is cls:
                    if func[:2] == '__':
                        return getattr(self.__asset_chain[cls], str('_' + func[2:]))(**kwargs)
                    else:
                        return getattr(self.__asset_chain[cls], func)(**kwargs)
            elif type(cls) is str:
                if str(asset) == cls:
                    if func[:2] == '__':
                        return getattr(self.__asset_chain[asset], str('_' + func[2:]))(**kwargs)
                    else:
                        return getattr(self.__asset_chain[asset], func)(**kwargs)
        return

    def run_status(self) -> bool:
        """ Returns frameworks run status """
        return self.run

    def system_exit(self, **kwargs):
        """ Shutdown runtime-engine """
        self.console_out("Shutting down runtime-engine...")
        for __module in self.__SYS_MODULES:
            if __module[1] is True:
                self.console_out(f"Stopping {__module[0].__name__}...")
                self.__asset_chain[__module[0]].stop()
        self.run = False
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

    def __core_status(self) -> bool:
        """ Determines if required modules are active """
        return self.__stat.core_systems_active()

    def __all_status(self) -> bool:
        """ Determines if all modules are actvie """
        return self.__stat.all_systems_active()

    # SERVICE METHODS
    def __whitelist_class(self, requestor: any, cls: any, **kwargs):
        """ Add a class to the providers whitelist """
        self.__svc.whitelist_class(requestor=requestor, cls=cls, **kwargs)
        self.console_out(f"Added '{cls}' to provider whitelist")
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
    def bus_assetc(self, requestor: any) -> dict:
        if type(requestor) == SystemMonitor:
            return self.__asset_chain

    def __inject_base_services(self):
        """ Add low-level framework services to provider """
        self.__implement_service('runstat', self, self.run_status)
        self.__implement_service('console', self, self.console_out)
        self.__implement_service('exc', self.__exc, self.exception)
        self.__implement_service('exit', self, self.system_exit)
        self.__implement_service('getstat', self.__stat, self.__get_module_status)
        self.__implement_service('setstat', self.__stat, self.__set_module_status, clearance='low')
        self.__implement_service('corestat', self.__stat, self.__core_status)
        self.__implement_service('allstat', self.__stat, self.__all_status)
        self.__implement_service('nsvc', self.__svc, self.__implement_service)
        self.__implement_service('wcls', self.__svc, self.__whitelist_class)
        self.__implement_service('acls', self.__svc, self.__authorize_class)
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
                t: str = kwargs.get('text')
                del kwargs['text']
                self.asset_function(SystemConsoleManager, 'console_out', text=t, **kwargs)
        except BaseException as Unknown:
            self.exception(self, Unknown, sys.exc_info(), unaccounted=True,
                           pointer='__master_console_out()')
            self.console_out("There was an issue printing the previous console request", root=True, error=True)
        finally:
            return
