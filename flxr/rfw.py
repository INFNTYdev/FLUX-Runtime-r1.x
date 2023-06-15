
""" FLUX Runtime-Engine Framework """


#   MODULE IMPORTS
from flxr import *


#   MODULE CLASSES
class Flxr:

    __FW_DEPLOYABLE: list = [
        ['thread*', FlxrThreadManager, False, False],
        ['datetime*', FlxrDatetimeManager, True, False],
        ['runtime', FlxrRuntimeClock, True, False],
        ['console*', FlxrConsoleManager, True, False],
        ['fileio*', FlxrFileIOManager, True, False],
        ['tkinter', FlxrTkinterManager, False, True],
        # ['monitor*', FlxrRuntimeMonitor, True, True],
    ]

    def __init__(self, main: any = None, dev: bool = False) -> None:
        """
        FLUX Runtime-Engine
        
        :param main: The main application instance in which the framework focuses
        :param dev: Framework developer status
        """

        self._dev: bool = dev
        self._app_main = main

        self._TSTART: float = time.perf_counter()
        self._module_load_wait: float = 0.0
        self._startup_load_wait: float = 0.0

        self._run: bool = True
        self._startup: bool = True
        self._fatal_error: bool = False
        self._active_environment: bool = False

        self.__fw_assets: AssetChain = AssetChain()

        try:
            self.__status: StatusManager = StatusManager(
                fwmods=self.__FW_DEPLOYABLE,
                svc=self.base_services()
            )
            self.__fw_assets[StatusManager] = self.__status
            self.__status.include(module=FlxrExceptionManager, core=True)
            self.__status.include(module=ServiceHost, core=True)
        except Exception as StatFailure:
            self._premature_failure(
                cls=StatusManager,
                exc=StatFailure,
                ecode=STATUS_FAIL_EXIT
            )
        
        self._console_out("Preparing framework exception handler...")
        try:
            self.__exc_handler: FlxrExceptionManager = FlxrExceptionManager(
                hfw=self,
                svc=self.base_services()
            )
            self.__fw_assets[FlxrExceptionManager] = self.__exc_handler
            self.__status.set(FlxrExceptionManager, True)
        except Exception as ExcFailure:
            self._premature_failure(
                cls=FlxrExceptionManager,
                exc=ExcFailure,
                ecode=EXCEPTION_FAIL_EXIT
            )
        
        self._console_out("Preparing framework service host...")
        try:
            self.__svc_host: ServiceHost = ServiceHost(
                hfw=self,
                svc=self.base_services()
            )
            self.__fw_assets[ServiceHost] = self.__svc_host
            self.__status.set(ServiceHost, True)
            self.__svc_host.whitelist(
                requestor=self,
                cls=StatusManager,
                clearance=MED
            )
            self.__svc_host.new(
                call='sstat',
                cls=StatusManager,
                func=self.__status.set,
                clearance=LOW
            )
        except Exception as SvcFailure:
            self._exception(
                cls=self,
                excinfo=sys.exc_info(),
                pointer='__init__()',
                critical=True
            )
        
        self._console_out(f"Preparing {len(self.__FW_DEPLOYABLE)} framework modules...")
        for index, _module in enumerate(self.__FW_DEPLOYABLE):
            try:
                self._console_out(f"Initializing {_module[1].__name__} - ({index+1}/{len(self.__FW_DEPLOYABLE)})...")
                self.__svc_host.whitelist(
                    requestor=self,
                    cls=_module[1],
                    clearance=MED
                )

                if _module[3] is True:
                    self.__svc_host.authorize(
                        requestor=self,
                        cls=_module[1]
                    )

                self.__fw_assets[_module[1]] = _module[1](
                    hfw=self,
                    svc=self.__svc_host.serve
                )

                if _module[2] is True:
                    self.__fw_assets.asset_func(
                        asset=_module[1],
                        func='start_module'
                    )
                else:
                    self.__status.set(module=_module[1], status=True)
            except Exception as ModuleInitFailure:
                self._exception(
                    cls=self,
                    excinfo=sys.exc_info(),
                    pointer='__init__()',
                )
                self._console_out(msg=f"Failed to initialize {_module[1].__name__}", error=True)
                if _module[0][-1] == '*':
                    self._console_out(f"Core module required to start runtime", error=True)
                    self._fatal_error = True
                    self._core_module_failure(
                        mod=_module[1],
                        exc=ModuleInitFailure,
                        ecode=RTE_FAIL_EXIT
                    )
        
        while not self.__status.all_active():
            if self._module_load_wait == 0:
                self._console_out("Waiting for framework modules...")
            time.sleep(.1)
            self._module_load_wait += .1
            if 10 <= self._module_load_wait <= 10.1:
                self._console_out("Startup is taking longer than usual...")
                if self.__status.core_active():
                    self._console_out("Core modules ready, finishing remainders in background...")
                    self._console_out("WARNING: modules still preparing in background")
                    break
            elif 20 <= self._module_load_wait <= 20.1:
                self._console_out("Framework startup took too long", error=True)
                self._fatal_error = True
                self.system_exit()

        if main is not None:
            self.set_main(main)

        self._startup = False
        self._active_environment = True
        self._TEND: float = time.perf_counter()
        self._startup_load_wait = round(self._TEND-self._TSTART, 5)
        self._console_out(f"Startup time: {round(self._TEND-self._TSTART, 2)} seconds")
        self._console_out("Runtime framework ready")

        if main is not None:
            self._run_application()
        else:
            self._console_out(msg="No application provided")

    def dev(self) -> bool:
        """ Returns the runtime-engine developer status """
        return self._dev

    def running(self) -> bool:
        """ Returns the framework run status """
        return self._run
    
    def active(self) -> bool:
        """ Returns the runtime-engine run status """
        return self._run and self._active_environment
    
    def in_startup(self) -> bool:
        """ Returns the runtime-engine start-up status """
        return self._startup

    def startup_time(self) -> float:
        """ Returns the framework startup time """
        return self._startup_load_wait
    
    def fatal_error(self) -> bool:
        """ Returns the runtime-engine fatal error status """
        return self._fatal_error

    def set_main(self, window: type) -> None:
        """ Set the framework main application window """
        self._app_main = window
        self.__fw_assets.asset_func(FlxrTkinterManager, 'set_main', window=window)
        self._run_application()
    
    def base_services(self) -> dict:
        """ Returns base framework functionality """
        return {
            'console': self._console_out,
            'exc': self._exception
        }

    def service(self) -> any:
        """ Returns the framework service call """
        return self.__svc_host.serve
    
    def system_exit(self, **kwargs) -> None:
        """ Runtime-Engine shutdown sequence """
        self._console_out("Shutting down runtime framework...")
        self._startup = False
        self._active_environment = False

        for __module in self.__FW_DEPLOYABLE:
            if __module[2] is True:
                self._console_out(f"Stopping {__module[1].__name__}...")
                pass
        
        self._run = False
        exit(kwargs.get('ecode', DEFAULT_EXIT))
    
    @staticmethod
    def is_rfw() -> bool:
        return True

    def _run_application(self) -> None:
        """ Run the framework application """
        if not self._startup:
            if self._app_main is None:
                self._console_out("No application available to start", error=True)
                return

            self._console_out(msg="Launching application window...")
            self.__fw_assets.asset_func(FlxrTkinterManager, 'start_main')
            self.system_exit(ecode=CLEAN_EXIT)
        else:
            self._console_out(msg="Framework is not ready to launch application", error=True)
    
    def _console_out(self, msg: str, error: bool = False, **kwargs) -> None:
        """ Send text to the framework log """
        self._master_console_output(
            m=msg,
            error=error,
            skip=kwargs.get('skip', False),
            prefix=kwargs.get('prefix', ''),
            seperator=kwargs.get('seperator', '|'),
            show_date=kwargs.get('show_date', True),
            show_time=kwargs.get('show_time', True),
            pconfig=kwargs.get('pconfig')
        )
    
    def _exception(self, cls: any, excinfo: tuple, **kwargs) -> None:
        """ Handles framework exceptions """
        self.__exc_handler.exception(
            _from=cls,
            excinfo=excinfo,
            pointer=kwargs.get('pointer'),
            critical=kwargs.get('critical', False)
        )

    def _master_console_output(self, m: str, **kwargs) -> None:
        """ Master console output """
        if self.__status.get(FlxrConsoleManager):
            self.__fw_assets.asset_func(
                asset=FlxrConsoleManager,
                func='queue_output',
                msg=m,
                pconfig=kwargs.get('pconfig'),
                error=kwargs.get('error', False)
            )
        else:
            p_str: str = f"\t{kwargs.get('prefix', '')}- >  "
            if kwargs.get('error', False) is True:
                p_str += "[ ERROR ] : "
            p_str += m
            if kwargs.get('skip', False):
                p_str = f'\n{p_str}'
            if self._dev:
                print(p_str)
    
    def _premature_failure(self, cls: type, exc: Exception, **kwargs) -> None:
        """ Runtime-Engine premature failure sequence """
        print(
            f'\n\n\t[ FATAL RUNTIME ERROR ] : {exc}'
            f'\n\t- Failed to start {cls.__name__} module'
        )
        input('\n\tPress enter to exit...')
        self.system_exit(**kwargs)
    
    def _core_module_failure(self, mod: type, exc: Exception, ecode: int) -> None:
        """ Runtime-Engine core module failure sequence """
        print(
            f'\n\n\t[ FATAL RUNTIME ERROR ] : {exc}'
            f'\n\t- Failed to start core {mod.__name__} module'
        )
        input('\n\tPress enter to exit...')
        self.system_exit(ecode=ecode)
