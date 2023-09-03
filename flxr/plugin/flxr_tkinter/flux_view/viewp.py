
"""
FLUX Tkinter Window Viewport Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
import tkinter as tk


#   EXTERNAL IMPORTS
from .interface_view import FluxView


#   MODULE CLASS
class FluxViewPort(FluxView):
    def __init__(self, hfw, cls, master, identifier: str, **kwargs) -> None:
        """ FLUX interface viewport """
        super().__init__(
            hfw=hfw,
            cls=cls,
            master=master,
            identifier=identifier
        )
