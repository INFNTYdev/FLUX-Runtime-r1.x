
"""
FLUX Tkinter Viewframe Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
import tkinter as tk


#   EXTERNAL IMPORTS
from .interface_view import FluxView


#   MODULE CLASS
class FluxViewFrame(FluxView):
    def __init__(self, hfw, cls, master, identifier: str, **kwargs) -> None:
        """ FLUX interface viewframe """
        super().__init__(
            hfw=hfw,
            cls=cls,
            master=master,
            identifier=identifier,
            **kwargs
        )

    def place(self, child, **pack_args) -> None:
        """ Place provided widget in
        viewframe using pack manager """
        try:
            self.new_child(child)
            child.pack(**pack_args)
        except Exception as UnexpectedFailure:
            self.console(
                msg=f"Failed to place {child} in '{self.identifier()}' viewframe",
                error=True
            )
            self.console(msg=str(UnexpectedFailure), error=True)
