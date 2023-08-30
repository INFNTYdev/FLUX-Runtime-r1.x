
"""
Framework Status Manager Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
pass


#   EXTERNAL IMPORTS
from flxr.constant import ErrMsgs, FlxrMsgs


#   MODULE CLASS
class FrameworkModule:
    def __init__(self, hfw, cls) -> None:
        """ Base framework module """
        if hfw.is_rfw():
            self.__framework = hfw
            self.__type: type = cls
            self._injectables: list = []

    def console(self, msg: str, error: bool = False, **kwargs) -> None:
        """ Send text to the framework log """
        self.__framework.service(requestor=self.__type)['console'](msg=msg, error=error, **kwargs)

    def exception(self, cls, excinfo: tuple, **kwargs) -> None:
        """ Send an exception to the framework log """
        self.__framework.service(requestor=self.__type)['exception'](cls=cls, excinfo=excinfo, **kwargs)

    def start_module(self) -> None:
        """ Start framework module if applicable """
        if not self._runnable_module():
            return

        self.console(msg=f"Starting {self.__type.__name__} module...")

    def stop_module(self) -> None:
        """ Stop framework module if applicable """
        pass

    def process_proxy(self) -> dict:
        """ Returns the processes in the
        framework proxy """
        pass

    def framework(self) -> any:
        """ Returns the hosting framework instance """
        return self.__framework

    def to_service_injector(self, load: list[tuple]) -> None:
        """ Load injector with new services """
        for injectable in load:
            if type(injectable) is tuple:
                _call, _func, _clearance = injectable
                self._injectables.append({'call': _call, 'func': _func, 'clearance': _clearance})

    def inject_services(self) -> None:
        """ Inject loaded services into the framework """
        self.console(msg=f"Injecting {self.__type.__name__} services:")
        for _injectable in self._injectables:
            self.__framework.inject_service(
                call=_injectable.get('call'),
                cls=self.__type,
                func=_injectable.get('func'),
                clearance=_injectable.get('clearance')
            )
        self._injectables.clear()

    def _runnable_module(self) -> bool:
        """ Returns true if the framework module is runnable """
        _is_runnable: bool = True
        if '_mainloop' not in self.__dir__():
            self.console(msg=ErrMsgs.ERRM_F_004.format(module=self.__type.__name__), error=True)
            _is_runnable = False
        if '_runnable' not in self.__dir__():
            self.console(msg=ErrMsgs.ERRM_F_005.format(module=self.__type.__name__), error=True)
            _is_runnable = False
        if '_run' not in self.__dir__():
            self.console(msg=ErrMsgs.ERRM_F_006.format(module=self.__type.__name__), error=True)
            _is_runnable = False
        if '_refresh' not in self.__dir__():
            self.console(msg=ErrMsgs.ERRM_F_007.format(module=self.__type.__name__), error=True)
            _is_runnable = False
        return _is_runnable
