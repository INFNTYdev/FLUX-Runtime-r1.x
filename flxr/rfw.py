
"""
FLUX Runtime Framework Main Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
import os
import time


#   EXTERNAL IMPORTS
pass


#   LOCAL IMPORTS
import flxr
from .constant import ErrMsgs, FlxrMsgs, ConsoleVars
from .utility import AssetChain, ProcessProxy
from .core import StatusManager, FlxrServiceManager, \
    FlxrThreadManager, FlxrDatetimeManager, FlxrRuntimeClock, \
    FlxrConsoleManager, FlxrFileIOManager, FlxrSystemManager
from .plugin import FlxrTkinterManager


#   MODULE CLASS
class Flxr:
    def __init__(self, main: type, **kwargs) -> None:
        """
        FLUX Runtime Framework Instance

        :param main: Main application window class or None
        :param kwargs: Additional args such as 'dev' and 'process_proxy'
        """
        try:
            self._dev: bool = kwargs.get('dev', False)
            self._app_main: type = main

            self._console_out(msg=FlxrMsgs.FWM_001, pointer=False)
            self._console_out(msg=FlxrMsgs.FWM_F_002.format(v=flxr.fwversion()), pointer=False)

            TSTART: float = time.perf_counter()
            self._startup_load_wait: float = .0
            self._module_load_wait: float = .0

            self._run: bool = True
            self._startup: bool = True
            self._fatal_error: bool = False
            self._service_enabled: bool = False
            self._active_environment: bool = False

            self.__fw_chain: AssetChain = AssetChain()
            self.__process_proxy: ProcessProxy = ProcessProxy()
            self.__fw_status: StatusManager = StatusManager(
                deployable=self._fw_deployable(),
                hfw=self
            )
            self.__service_call = None

            if kwargs.get('process_proxy') is not None:
                if type(kwargs.get('process_proxy')) is not list:
                    raise ValueError(ErrMsgs.ERRM_002)

                for process in kwargs.get('process_proxy'):
                    self.__process_proxy.append_process(process)

            self._console_out(msg=FlxrMsgs.FWM_F_003.format(q=self._deployable_count()))
            for index, _module in enumerate(self._fw_deployable()):
                try:
                    self._console_out(
                        msg=FlxrMsgs.FWM_F_004.format(
                            module=_module[1].__name__,
                            index=index+1,
                            max=self._deployable_count()
                        )
                    )
                    if self._service_enabled:
                        self.__fw_chain.asset_func(
                            asset=FlxrServiceManager,
                            _func='authorize',
                            requestor=Flxr,
                            cls=_module[1]
                        )
                    else:
                        if index > 1:
                            self._console_out(
                                msg=f"Failed to give {_module[1].__name__} authorization",
                                error=True
                            )

                    self.__fw_chain[_module[1]] = _module[1](hfw=self)
                    if self.__fw_chain[_module[1]].threaded():
                        self.__fw_chain[_module[1]].start_module()
                    else:
                        self.__fw_status.set(module=_module[1], status=True)
                    self._post_module_initialization(_module[1])
                except Exception as ModuleInitFailure:
                    self._console_out(
                        msg=f"[ FAILED TO INITIALIZE {_module[1].__name__} MODULE ]",
                        error=True
                    )
                    self._console_out(msg=f"Reason: {ModuleInitFailure}", error=True)

            self._console_out(msg="Waiting for framework modules...")
            LSTART: float = time.perf_counter()
            lclock: float = .0
            while not self.__fw_status.all_active():
                time.sleep(.1)
                lclock += .1
                if 10 <= lclock <= 10.1:
                    self._console_out(msg="Startup is taking longer than usual", notice=True, prefix='!')
                elif 20 <= lclock <= 20.1:
                    self._console_out(msg="Framework startup took too long", error=True, prefix='!')
                    self._fatal_error = True
                    # Start up error notification
                    break

            self._module_load_wait = round(time.perf_counter()-LSTART, 2)
            self._startup_load_wait = round(time.perf_counter()-TSTART, 2)
            self._console_out(msg=f"Thread load wait: {self._module_load_wait}s")
            self._console_out(msg=f"Startup load wait: {self._startup_load_wait}s")

            if not self._fatal_error:
                self._startup = False
                self._active_environment = True
                self._console_out(msg=f"Runtime framework ready with {len(self.service(self))} services")
            else:
                self.framework_exit()
        except Exception as FrameworkFailure:
            print(f"\n\n[ FATAL FRAMEWORK ERROR ] : {FrameworkFailure}")
            self._fatal_error = True
            self._active_environment = False
            self._service_enabled = False
            self._startup = False

    def dev_mode(self) -> bool:
        """ Returns the framework development flag """
        return self._dev

    def active(self) -> bool:
        """ Determines if any portion of the
        framework is actively running """
        pass

    def is_alive(self) -> bool:
        """ Determines if the framework is
        actively running """
        return self._run

    def in_startup(self) -> bool:
        """ Determines if the framework is in
        startup """
        return self._startup

    def startup_time(self) -> float:
        """ Returns the framework startup
        time in seconds """
        return self._startup_load_wait

    def has_fatal_error(self) -> bool:
        """ Returns the framework fatal error flag """
        return self._fatal_error

    def services_enabled(self) -> bool:
        """ Returns true if the framework
        services are enabled """
        return self._service_enabled

    def base_service(self) -> dict:
        """ Returns the base framework services """
        return {
            'console': self._console_out,
            'exception': self._log_exception,
            'pproxy': self.__process_proxy.processes,
            'setstat': self.__fw_status.set,
            'getstat': self.__fw_status.get,
            'exit': self.framework_exit
        }

    def service(self, requestor, base: bool = False) -> dict:
        """ Returns framework services """
        if (not self._service_enabled) or (base is True):
            return self.base_service()
        return self.__service_call(requestor=requestor)

    def add_window(self, identifier: str, cls: type, **kwargs) -> None:
        """ Add FLUX tkinter window type to host """
        self.__fw_chain.asset_func(
            asset=FlxrTkinterManager,
            _func='add_window',
            identifier=identifier,
            cls=cls,
            **kwargs
        )

    def set_main_window(self, window: str or type, start: bool = False) -> None:
        """ Set FLUX tkinter window as
        main window """
        self.__fw_chain.asset_func(
            asset=FlxrTkinterManager,
            _func='set_main_window',
            window=window,
            start=start
        )

    def inject_service(self, call: str, cls, func, clearance: int = 0) -> None:
        """ Add new service to framework """
        self.__fw_chain.asset_func(
            asset=FlxrServiceManager,
            _func='new',
            call=call,
            cls=cls,
            func=func,
            clearance=clearance
        )

    def run_application(self) -> None:
        """ Run main application supplied """
        self.__fw_chain.asset_func(
            asset=FlxrTkinterManager,
            _func='start_module'
        )
        self.framework_exit()

    def asset_bus(self, requestor) -> AssetChain:
        if not self.is_rfw_manager(requestor):
            return
        return self.__fw_chain

    def is_rfw_manager(self, obj) -> bool:
        """ Returns true if the provided object
        is the framework system manager """
        if type(obj) is not FlxrSystemManager:
            return False
        if obj is not self.__fw_chain[FlxrSystemManager]:
            return False
        return True

    #   ^ ^ ^  PUBLIC METHODS ABOVE THIS POINT  ^ ^ ^   #

    def framework_exit(self) -> None:
        """ Gracefully stop the framework and
        all its components """
        self._console_out(msg="Shutting down runtime framework...")
        for _class, __module in self.__fw_chain.items():
            if __module.threaded():
                __module.stop_module()
            else:
                self.__fw_status.set(
                    module=_class,
                    status=False
                )

        self._active_environment = False
        self._run = False

    def _post_module_initialization(self, module: type) -> None:
        """ Complete module specific tasks
        after initialization """
        if module is FlxrServiceManager:
            self.__fw_chain.asset_func(FlxrServiceManager, 'authorize', requestor=Flxr, cls=StatusManager)
            self._service_enabled = True
            self._console_out(msg=FlxrMsgs.FWM_005)
            self.__service_call = self.__fw_chain.asset_func(FlxrServiceManager, 'serve_call')
            self._console_out(msg=FlxrMsgs.FWM_006)
        elif module is FlxrFileIOManager:
            self._console_out(msg=FlxrMsgs.FWM_F_007.format(q=len(self._fw_file_paths())))
            for _fw_f_path in self._fw_file_paths():
                self.__fw_chain.asset_func(
                    asset=FlxrFileIOManager,
                    _func='link',
                    path=_fw_f_path
                )

    @staticmethod
    def is_rfw() -> bool:
        return True

    @staticmethod
    def _fw_deployable() -> list[list]:
        """ Framework deployable modules """
        return [
            ['service*', FlxrServiceManager],
            ['thread*', FlxrThreadManager],
            ['datetime*', FlxrDatetimeManager],
            ['runtime', FlxrRuntimeClock],
            ['console*', FlxrConsoleManager],
            #['fileio*', FlxrFileIOManager],
            ['tkinter', FlxrTkinterManager],
            # ['monitor*', FlxrSystemManager],
        ]

    @staticmethod
    def _fw_file_paths() -> list[str]:
        """ Returns the list of framework file paths """
        _paths: list = []
        for root, directories, files in os.walk('flxr\\'):
            for file in files:
                if (file.endswith(".py")) and (file != '__init__.py'):
                    _paths.append(os.path.join(root, file))
        return _paths

    def _deployable_count(self) -> int:
        """ Return the number of deployable
        framework modules """
        return len(self._fw_deployable())

    def _run_main(self) -> None:
        """ Run application main loop """
        pass

    def _console_out(self, msg: str, error: bool = False, **kwargs) -> None:
        """ Send text to the framework log """
        _print_config: dict = {
            'message': msg,
            'error': error,
            'warning': kwargs.get('warning', False),
            'notice': kwargs.get('notice', False),
            'skip': kwargs.get('skip', False),
            'prefix': kwargs.get('prefix', ' '),
            'pointer': kwargs.get('pointer', True),
            'suffix': kwargs.get('suffix', ''),
            'seperator': kwargs.get('seperator', '|'),
            'show_date': kwargs.get('show_date', True),
            'show_time': kwargs.get('show_time', True),
        }

        if kwargs:
            _print_config |= kwargs

        self._master_console_output(**_print_config)

    def _log_exception(self, cls, excinfo: tuple, **kwargs) -> None:
        """ Send an exception to the framework log """
        pass

    def _master_console_output(self, **kwargs) -> None:
        """ Master console output """
        try:
            if self.__fw_status.get(FlxrConsoleManager) is True:
                self.__fw_chain.asset_func(
                    asset=FlxrConsoleManager,
                    _func='queue_output',
                    **kwargs
                )
            else:
                self._root_console_output(**kwargs)
        except AttributeError:
            self._root_console_output(**kwargs)

    def _root_console_output(self, **kwargs) -> None:
        """ Root console output """
        _p_str: str = f"\t{kwargs.get('prefix')}"
        if kwargs.get('pointer') is True:
            _p_str += '- > '
        else:
            _p_str += ' '*4
        if kwargs.get('error') is True:
            _p_str += ConsoleVars.ERROR_PREFIX
        elif kwargs.get('warning') is True:
            _p_str += ConsoleVars.WARNING_PREFIX
        elif kwargs.get('notice') is True:
            _p_str += ConsoleVars.NOTICE_PREFIX
        _p_str += kwargs.get('message') + kwargs.get('suffix')
        if kwargs.get('skip') is True:
            _p_str = f"\n{_p_str}"
        if self._dev:
            print(_p_str)
