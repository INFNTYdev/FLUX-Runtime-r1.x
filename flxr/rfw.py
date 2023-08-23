
"""
FLUX Runtime Framework Main Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
import time


#   EXTERNAL IMPORTS
pass


#   LOCAL IMPORTS
import flxr
from .constant import ErrMsgs
from .utility import AssetChain, ProcessProxy
from .core import StatusManager, FlxrServiceManager, \
    FlxrThreadManager, FlxrDatetimeManager, FlxrConsoleManager, \
    FlxrFileIOManager


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

            self._console_out(msg="INFINITY Systems 2023")
            self._console_out(msg=f"FLUX Runtime Framework | v{flxr.fwversion()}")

            self._TSTART: float = time.perf_counter()
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

            if kwargs.get('process_proxy') is not None:
                if type(kwargs.get('process_proxy')) is not list:
                    raise ValueError(ErrMsgs.ERRM_002)

                for process in kwargs.get('process_proxy'):
                    self.__process_proxy.append_process(process)

            self._console_out(msg=f"Preparing {self._deployable_count()} framework modules...")
            for index, _module in enumerate(self._fw_deployable()):
                try:
                    self._console_out(
                        msg=f"Initializing {_module[1].__name__} - ({index+1}/{self._deployable_count()})"
                    )

                    if self._service_enabled:
                        pass
                    else:
                        pass

                    self.__fw_chain[_module[1]] = _module[1](hfw=self)
                    if _module[2] is True:
                        self.__fw_chain.asset_func(
                            asset=_module[1],
                            func='start_module'
                        )
                    else:
                        self.__fw_status.set(module=_module[1], status=True)
                except Exception as ModuleInitFailure:
                    print(ModuleInitFailure)
        except Exception as FrameworkFailure:
            print(f"\n\n[ FATAL FRAMEWORK ERROR ]\n{FrameworkFailure}")
            pass

    def dev_mode(self) -> bool:
        """ Returns the framework development flag """
        pass

    def active(self) -> bool:
        """ Determines if any portion of the
        framework is actively running """
        pass

    def is_alive(self) -> bool:
        """ Determines if the framework is
        actively running """
        pass

    def in_startup(self) -> bool:
        """ Determines if the framework is in
        startup """
        pass

    def startup_time(self) -> float:
        """ Returns the framework startup
        time in seconds """
        pass

    def has_fatal_error(self) -> bool:
        """ Returns the framework fatal error flag """
        pass

    def services_enabled(self) -> bool:
        """ Determines if the framework services
        are enabled """
        return self._service_enabled

    def base_service(self) -> dict:
        """ Returns the base framework services """
        return {
            'console': self._console_out,
            'exception': self._log_exception,
            'pproxy': None,
            'exit': self.framework_exit
        }

    def service(self, requestor, base: bool = False) -> dict:
        """ Returns framework services """
        if (not self._service_enabled) or (base is True):
            return self.base_service()
        pass

    #   ^ ^ ^  PUBLIC METHODS ABOVE THIS POINT  ^ ^ ^   #

    def framework_exit(self) -> None:
        """ Gracefully stop the framework and
        all its components """
        pass

    @staticmethod
    def is_rfw() -> bool:
        return True

    @staticmethod
    def _fw_deployable() -> list[list]:
        """ Framework deployable modules """
        return [
            ['service*', FlxrServiceManager, False, False],
            #['thread*', FlxrThreadManager, False, False],
            #['datetime*', FlxrDatetimeManager, True, False],
            # ['runtime', FlxrRuntimeClock, True, False],
            # ['console*', FlxrConsoleManager, True, False],
            # ['fileio*', FlxrFileIOManager, True, False],
            # ['tkinter', FlxrTkinterManager, False, True],
            # ['monitor*', FlxrSystemManager, True, True],
        ]

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
            'notice': kwargs.get('notice', False),
            'skip': kwargs.get('skip', False),
            'prefix': kwargs.get('prefix', ''),
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
            if self.__fw_status.get(None):
                pass
            else:
                self._root_console_output(**kwargs)
        except AttributeError:
            self._root_console_output(**kwargs)

    def _root_console_output(self, **kwargs) -> None:
        """ Root console output """
        _p_str: str = f"\t{kwargs.get('prefix')}- >  "
        if kwargs.get('error') is True:
            _p_str += "[ ERROR ] : "
        elif kwargs.get('notice') is True:
            _p_str += "[ WARNING ] : "
        _p_str += kwargs.get('message') + kwargs.get('suffix')
        if kwargs.get('skip') is True:
            _p_str = f"\n{_p_str}"
        if self._dev:
            print(_p_str)
