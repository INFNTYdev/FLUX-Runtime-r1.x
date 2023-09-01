
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
    def __init__(self, hfw, cls, identifier: str, **kwargs) -> None:
        """ FLUX runtime framework tkinter window """
        super().__init__(hfw=hfw, cls=cls)
        self._identifier: str = self._evaluate_identifier(identifier)

    def identifier(self) -> str:
        """ Returns the window identifier """
        return self._identifier

    def _evaluate_identifier(self, identifier) -> str:
        """ Evaluate and return the provided
        window identifier """
        if type(identifier) is not str:
            self._invalid_identifier(identifier)
        return identifier

    @staticmethod
    def _invalid_identifier(identifier) -> None:
        """ Raises value error on invalid
        window identifiers """
        raise ValueError(
            f"Invalid window identifier: {identifier}"
        )
