
""" FLUX Runtime-Engine Framework """


# MODULE IMPORTS
from flxr import *

# MODULE PACKAGE
__package__ = pkg_n()


# MODULE CLASSES
class Flxr:

    __SYS_MODS: list = [
        ['thread*', FlxrThreadManager, False],
        ['datetime*', FlxrDatetime, True],
        ['runtime', FlxrRuntimeClock, True],
        ['console', FlxrConsoleManager, True],
        ['io', FlxrFileIOManager, True],
        ['tkinter', FlxrTkinterLibrary, False],
        ['monitor*', FlxrRuntimeMonitor, True],
    ]

    def __init__(self, dev: bool = False, **kwargs):
        """
        FLUX Runtime-Engine

        :param dev: Launch framework in developer mode
        :param main: Main application class
        :param kwargs: Additional framework options
        """

        self._dev: bool = dev
        self._run: bool = True
        self._start_up: bool = True
        self._active_enviroment: bool = False
        self._fatal_error: bool = False
        self._load_wait: float = 0.
        self._app_main = kwargs.get('main')

        self.__sys_assets: AssetChain = AssetChain()

        try:
            self._status: StatusManager = StatusManager(fwmods=self.__SYS_MODS, svc=self.base_services())
            self.__sys_assets[StatusManager] = self._status
            self._status.include(module=ExceptionLogManager, core=True)
            self._status.include(module=ServiceHost, core=True)
        except Exception as StatFailure:
            self._premature_failure(
                symbol='status',
                exception=StatFailure,
                code=STAT_FAIL_EXIT
            )

        self._console_out("Preparing runtime framework...")
        try:
            self._exc_logger: ExceptionLogManager = ExceptionLogManager(svc=self.base_services())
            self.__sys_assets[ExceptionLogManager] = self._exc_logger
            self._status.set(module=ExceptionLogManager, active=True)
        except Exception as ExcFailure:
            self._premature_failure(
                symbol='exception',
                exception=ExcFailure,
                code=EXC_FAIL_EXIT
            )

        try:
            self._service_host: ServiceHost = ServiceHost(fw=self, svc=self.base_services())
            self.__sys_assets[ServiceHost] = self._service_host
            self._status.set(module=ServiceHost, active=True)
            self._service_host.authorize(requestor=self, cls=FlxrTkinterLibrary)
            self._inject_services()
        except Exception as SvcFailure:
            self._exception(self, SvcFailure, sys.exc_info(), known=False, pointer='__init__()')
            self._premature_failure(
                symbol='service',
                exception=SvcFailure,
                code=SVC_FAIL_EXIT
            )

        self._console_out(f"Preparing {len(self.__SYS_MODS)} framework modules...")
        init_count: int = 1
        for module in self.__SYS_MODS:
            try:
                self._console_out(f"Initializing {module[1].__name__} - ({init_count}/{len(self.__SYS_MODS)})...")
                self._service_host.whitelist(
                    requestor=self,
                    cls=module[1],
                    clearance=MED
                )
                self.__sys_assets[module[1]] = module[1](
                    fw=self,
                    svc=self._service_host.serve
                )
                init_count += 1
                if module[2] is True:
                    self.__sys_assets.func(
                        asset=module[1],
                        func='start_module'
                    )
                else:
                    self._status.set(module=module[1], active=True)
            except Exception as ModuleInitFailure:
                self._exception(self, ModuleInitFailure, sys.exc_info(), known=False,
                                pointer='__init__()')
                self._console_out(f"Failed to initialize {module[1].__name__}", error=True)
                if module[0][-1] == '*':
                    self._console_out(f"WARNING! {module[1].__name__} module failed", error=True)
                    self._fatal_error = True

        self._console_out("Waiting for framework modules...")
        while self._run and (not self._status.core_modules_active()):
            time.sleep(0.1)
            self._load_wait += 0.1
            if self._load_wait == 10.0:
                self._console_out("Framework startup taking longer than usual")
            elif self._load_wait == 20.0:
                self._fatal_error = True
                self._console_out("Framework startup took too long")
                self.system_exit()

        self._wait(2)
        if self._status.core_modules_active():
            if not self._fatal_error:
                self._console_out(f"Framework modules ready ({round(self._load_wait, 2)}s)")
                self.test = self._service_host.serve(self)['TkWindow'](
                    identifier='test',
                    width=900,
                    height=400,
                    borderless=False,
                    bg='tan'
                )
                self.test.mainloop()
        else:
            self._console_out("Failed to initialize core modules", error=True)
            self.system_exit()

    def active(self) -> bool:
        """ Returns the frameworks run status """
        return self._run

    def dev_mode(self) -> bool:
        """ Returns the frameworks developer mode status """
        return self._dev

    def base_services(self) -> dict:
        """ Returns base framework services """
        bsvc: dict = {
            'console': self._console_out,
            'exc': self._exception,
            'exit': self.system_exit
        }
        return bsvc

    def system_exit(self, **kwargs):
        """ Framework shutdown sequence """
        self._console_out("Shutting down runtime framework...")
        self._start_up = False
        self._active_enviroment = False

        for __module in self.__SYS_MODS:
            if __module[2] is True:
                self._console_out(f"Stopping {__module[1].__name__}...")
                self.__sys_assets.func(
                    asset=__module[1],
                    func='stop_module'
                )

        self._run = False
        exit(kwargs.get('code', DEFAULT_EXIT))

    @staticmethod
    def is_fw() -> bool:
        return True

    def _console_out(self, text: str, **kwargs):
        """ Send text to the console for output """
        self._master_console_output(
            t=text,
            error=kwargs.get('error', False),
            skip=kwargs.get('skip', False),
            prefix=kwargs.get('prefix', ''),
            seperator=kwargs.get('seperator', '|'),
            show_date=kwargs.get('show_date', True),
            show_time=kwargs.get('show_time', True)
        )

    def _exception(self, cls: any, exc: Exception, excinfo: tuple, **kwargs):
        """ Handles system raised exceptions """
        # Check status first then do below
        self._exc_logger.exception(
            cls=cls,
            exc=exc,
            excinfo=excinfo,
            known=kwargs.get('known'),
            pointer=kwargs.get('pointer'),
            status=kwargs.get('status')
        )

    def _set_fatality_status(self, status: bool):
        """ Set the framework fatal error status """
        self._fatal_error = status

    def _inject_services(self):
        """ Inject core framework services into distributor """
        injectables: list = [
            ('sstat', StatusManager, self._status.set, MED),
            ('gstat', StatusManager, self._status.get, LOW),
            ('nstat', StatusManager, self._status.include, MED),
            ('fstat', Flxr, self._set_fatality_status, MED),
            ('coreStatus', StatusManager, self._status.core_modules_active, ANY),
            ('allStatus', StatusManager, self._status.all_modules_active, ANY),
        ]
        for new in injectables:
            self._service_host.new(
                call=new[0],
                cls=new[1],
                func=new[2],
                clearance=new[3]
            )

    @staticmethod
    def _wait(secs: int):
        """ Freeze main thread for specified time """
        if secs <= 10:
            time.sleep(secs)

    def _master_console_output(self, t: str, **kwargs):
        """ Master console output """
        if self._status.get(FlxrConsoleManager) is True:
            self.__sys_assets[FlxrConsoleManager].console_out(
                text=t,
                **kwargs
            )
        else:
            pconfig: dict = {
                'error_msg': kwargs.get('error', False),
                'skip_line': kwargs.get('skip', False),
                'prefix': kwargs.get('prefix', '')
            }
            p_str: str = f"\t{pconfig['prefix']}- >  "
            if pconfig['error_msg'] is True:
                p_str += "[ ERROR ] : "
            p_str += t
            if kwargs.get('skip', False):
                p_str = f'\n{p_str}'
            if self._dev:
                print(p_str)

    def _premature_failure(self, symbol: str, exception: Exception, **kwargs):
        """ Base module failure sequence """
        print(
            f'\n\n\t[ FATAL RUNTIME ERROR ] : {exception}'
            f'\n\t- Failed to start {symbol} module'
        )
        input('\n\tPress enter to exit...')
        self.system_exit(**kwargs)

    def __asset_chain(self) -> dict:
        """ Returns the frameworks asset chain """
        return self.__sys_assets
