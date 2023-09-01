
"""
FLUX Tkinter Window Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
pass


#   EXTERNAL IMPORTS
from .ftk import FluxTk


#   MODULE CLASS
class FluxWindow(FluxTk):

    __MAIN_LOCK: bool = False

    def __init__(self, hfw, cls, identifier: str, main: bool = False, **kwargs) -> None:
        """ FLUX runtime framework tkinter window """
        super().__init__(hfw=hfw, cls=cls, **kwargs)
        self._identifier: str = self._evaluate_identifier(identifier)
        self._is_main: bool = False
        if (main is True) and (not self.__MAIN_LOCK):
            self.console(msg=f"{self.window_class().__name__} window '{identifier}' set as main")
            self._set_as_main()

    def identifier(self) -> str:
        """ Returns the window identifier """
        return self._identifier

    def is_main(self, force: bool = None) -> bool:
        """ Returns true if window is
        main window """
        if force is True:
            self._set_as_main()
        return self._is_main

    def _evaluate_identifier(self, identifier) -> str:
        """ Evaluate and return the provided
        window identifier """
        if type(identifier) is not str:
            self._invalid_identifier(identifier)
        return identifier

    def _set_as_main(self) -> None:
        """ Set window as main window """
        self._is_main = True
        self.__MAIN_LOCK = True

    @staticmethod
    def _invalid_identifier(identifier) -> None:
        """ Raises value error on invalid
        window identifiers """
        raise ValueError(
            f"Invalid window identifier: {identifier}"
        )
