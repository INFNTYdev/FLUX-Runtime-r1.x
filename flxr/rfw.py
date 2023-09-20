
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

    __INSTANCE: bool = False

    def __init__(self, main: type = None, **kwargs) -> None:
        """
        FLUX Runtime Framework Instance

        :param main: Main application window class or None
        :param kwargs: Additional args such as 'dev' and 'process_proxy'
        """
        try:
            self.__dev: bool = kwargs.get('dev', False)
            self.__console_out(msg=FlxrMsgs.FWM_001, pointer=False)
            self.__console_out(msg=FlxrMsgs.FWM_F_002.format(v=flxr.fwversion()), pointer=False)

            TSTART: float = time.perf_counter()
            self.__run: bool = True
            self.__shutdown: bool = False
            self.__fatal_error: bool = False
            self.__startup_load_wait: float = .0
            self.__thread_load_wait: float = .0
            # ClientManager here
            self.__fw_chain: AssetChain = AssetChain()
            self.__process_proxy: ProcessProxy = ProcessProxy()
            self.__status: StatusManager = StatusManager(
                hfw=self,
                deployable=self.__fw_deployable()
            )
            self.__service_call = None

            if kwargs.get('process_proxy') is not None:
                if type(kwargs.get('process_proxy')) is not list:
                    raise ValueError(ErrMsgs.ERRM_002)
                for process in kwargs.get('process_proxy'):
                    self.__process_proxy.append_process(process)

            self.__console_out(msg=FlxrMsgs.FWM_F_003.format(q=self.deployable_count()))
            for index, _module in enumerate(self.__fw_deployable()):
                try:
                    self.__console_out(
                        msg=FlxrMsgs.FWM_F_004.format(
                            module=_module[1].__name__,
                            index=index + 1,
                            max=self.deployable_count()
                        )
                    )
                    self.__module_initialization(module=_module[1])
                    self.__post_module_initialization(module=_module[1])
                except Exception as ModuleInitFailure:
                    self.__console_out(
                        msg=f"[ FAILED TO INITIALIZE {_module[1].__name__} MODULE ]",
                        error=True
                    )
                    self.__console_out(msg=f"Reason: {ModuleInitFailure}", error=True)

            LSTART: float = time.perf_counter()
            self.__wait_for_modules()
            self.__thread_load_wait = round(time.perf_counter() - LSTART, 2)
            self.__startup_load_wait = round(time.perf_counter() - TSTART, 2)
            self.__console_out(msg=FlxrMsgs.FWM_F_010.format(s=self.__thread_load_wait))
            self.__console_out(msg=FlxrMsgs.FWM_F_011.format(s=self.__startup_load_wait))

            if self.__fatal_error is True:
                self.framework_exit()
            else:
                self.__console_out(msg=FlxrMsgs.FWM_F_012.format(q=len(self.service(self))))
        except RuntimeError as FrameworkFailure:
            print(f"\n\n[ FATAL FRAMEWORK ERROR ] : {FrameworkFailure}")
            self.__fatal_error = True
            self.__run = False

    @staticmethod
    def __fw_deployable() -> list[tuple[str, type]]:
        """ Framework deployable module manifest """
        return [
            ('service*', FlxrServiceManager),
            ('thread*', FlxrThreadManager),
            ('datetime*', FlxrDatetimeManager),
            ('runtime', FlxrRuntimeClock),
            ('console*', FlxrConsoleManager),
            # ('fileio*', FlxrFileIOManager),
            ('tkinter', FlxrTkinterManager),
            # ('monitor*', FlxrSystemManager),
        ]

    def developer_mode(self) -> bool:
        """ Returns true if framework
        is in developer mode """
        return self.__dev

    def active(self) -> bool:
        """ Returns true if
        framework is running """
        return self.__run

    def in_shutdown(self) -> bool:
        """ Returns true if framework
        is shutting down """
        return self.__shutdown

    def fatal_error(self) -> bool:
        """ Returns true if framework
        experienced a fatal error """
        return self.__fatal_error

    def startup_time(self) -> float:
        """ Returns framework
        start-up time in seconds """
        return self.__startup_load_wait

    def deployable_count(self) -> int:
        """ Returns number of manifested
        deployable framework modules """
        return len(self.__fw_deployable())

    def services_enabled(self) -> bool:
        """ Returns true if framework
        services are available """
        return self.__service_call is not None

    def base_service(self) -> dict:
        """ Returns framework base services """
        return {
            'console': self.__console_out,
            'exception': self.__log_exception,
            'pproxy': self.__process_proxy.processes,
            'setstat': self.__status.set,
            'getstat': self.__status.get,
            'exit': self.framework_exit
        }

    def service(self, requestor, base: bool = False) -> dict:
        """ Returns appropriate framework
        services to requestor """
        if (not self.services_enabled()) or (base is True):
            return self.base_service()
        return self.__service_call(requestor=requestor)

    def inject_service(self, call: str, cls: type, func, clearance: int = 0) -> None:
        """ Add new service call
        to framework services """
        if not self.services_enabled():
            return
        self.__fw_chain.asset_func(
            asset=FlxrServiceManager,
            _func='new',
            call=call,
            cls=cls,
            func=func,
            clearance=clearance
        )

    def attach_window(self, uid: str, cls: type, **kwargs) -> None:
        """ Add application window to framework """
        pass

    def set_main_window(self, window: str or type) -> None:
        """ Set specified application
        window as main """
        pass

    def run(self) -> None:
        """ Run embedded application """
        pass

    @staticmethod
    def is_rfw() -> bool: return True

    def framework_exit(self) -> None:
        """ Gracefully stop framework and
        all associated components """
        self.__shutdown = True
        self.__console_out(msg=FlxrMsgs.FWM_009)
        for _class, __module in self.__fw_chain.items():
            if __module.threaded():
                __module.stop_module()
            else:
                self.__status.set(module=_class, status=False)
        self.__run = False

    def __log_exception(self, cls, excinfo: tuple, **kwargs) -> None:
        """ Log system exception """
        pass

    def __root_console_output(self, **output) -> None:
        """ Root console output """
        _p_str: str = f"\t{output.get('prefix')}"
        if output.get('pointer') is True:
            _p_str += '- > '
        else:
            _p_str += ' ' * 4
        if output.get('error') is True:
            _p_str += ConsoleVars.ERROR_PREFIX
        elif output.get('warning') is True:
            _p_str += ConsoleVars.WARNING_PREFIX
        elif output.get('notice') is True:
            _p_str += ConsoleVars.NOTICE_PREFIX
        _p_str += output.get('message') + output.get('suffix')
        if output.get('skip') is True:
            _p_str = f"\n{_p_str}"
        if self.developer_mode():
            print(_p_str)

    def __master_console_output(self, **output) -> None:
        """ Master console output """
        try:
            if self.__status.get(FlxrConsoleManager) is False:
                raise AttributeError
            self.__fw_chain.asset_func(
                asset=FlxrConsoleManager,
                _func='queue_output',
                **output
            )
        except AttributeError:
            self.__root_console_output(**output)

    def __console_out(self, msg: str, error: bool = False, **kwargs) -> None:
        """ Send text to framework
        console for logging """
        print_config: dict = {
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
        self.__master_console_output(**print_config)

    def __module_initialization(self, module: type) -> None:
        """ Initialize deployable framework module """
        if self.services_enabled():
            self.__fw_chain.asset_func(
                asset=FlxrServiceManager,
                _func='authorize',
                requestor=Flxr,
                cls=module
            )
        self.__fw_chain[module] = module(hfw=self)
        if self.__fw_chain[module].threaded():
            self.__fw_chain[module].start_module()
        else:
            self.__status.set(module=module, status=True)

    def __wait_for_modules(self) -> None:
        """ Wait for all framework modules """
        self.__console_out(msg=FlxrMsgs.FWM_008)
        lclock: float = .0
        while not self.__status.all_active():
            time.sleep(.1)
            lclock += .1
            if 10 <= lclock <= 10.1:
                self.__console_out(msg="Startup is taking longer than usual", notice=True, prefix='!')
            elif 20 <= lclock <= 20.1:
                self.__fatal_error = True
                self.__console_out(msg="Framework startup took too long", error=True, prefix='!')
                # Start up error notification
                break

    def __post_module_initialization(self, module: type) -> None:
        """ Complete module specific
        tasks after initialization """
        if module is FlxrServiceManager:
            self.__console_out(msg=FlxrMsgs.FWM_005)
            self.__service_call = self.__fw_chain.asset_func(FlxrServiceManager, 'serve_call')
            self.__console_out(msg=FlxrMsgs.FWM_006)
            self.__fw_chain.asset_func(
                asset=FlxrServiceManager,
                _func='authorize',
                requestor=Flxr,
                cls=StatusManager
            )
