
"""
FLUX Tkinter Window Host Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
pass


#   EXTERNAL IMPORTS
from .flux_window import FluxWindow


#   MODULE CLASS
class FluxWindowHost(dict):
    def __init__(self) -> None:
        """ FLUX tkinter window host """
        super().__init__()

    def identifiers(self) -> list[str]:
        """ Returns the list of FLUX tkinter
        window identifiers """
        return [_id for _id in self.keys()]
