
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
pass


#   MODULE CLASS
class Flxr:
    def __init__(self, main: type, **kwargs) -> None:
        """
        FLUX Runtime Framework Instance

        :param main: Main application window class or None
        :param kwargs: Additional args such as 'dev' and 'process_proxy'
        """
        self._dev: bool = kwargs.get('dev', False)
        self._app_main: type = main

        self._TSTART: float = time.perf_counter()
        self._startup_load_wait: float = .0
        self._module_load_wait: float = .0

        self._run: bool = True
        self._startup: bool = True
        self._fatal_error: bool = False
        self._active_environment: bool = False

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

    def framework_exit(self) -> None:
        """ Gracefully stop the framework and
        all its components """
        pass

    @staticmethod
    def is_rfw() -> bool:
        return True
