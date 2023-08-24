
"""
Framework Status Manager Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
pass


#   EXTERNAL IMPORTS
pass


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
        print(self._injectables)
        self.__framework.inject_service(
            call=None,
            cls=None,
            clearance=None
        )
