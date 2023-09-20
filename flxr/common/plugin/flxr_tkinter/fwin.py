
"""
FLUX Framework Tkinter Window Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
import tkinter as tk


#   EXTERNAL IMPORTS
from .view import FTkWindow
from flxr.common.protocols import Flux


#   MODULE CLASS
class FluxWindow(tk.Tk, FTkWindow):
    def __init__(self, hfw: Flux, cls: type, uid: str, parent: any = None, **kwargs) -> None:
        """ Base FLUX runtime framework tkinter window """
        tk.Tk.__init__(self)
        FTkWindow.__init__(self, hfw=hfw, cls=cls, uid=uid, parent=parent, **kwargs)
        self.overrideredirect(kwargs.get('borderless', False))
        # self.protocol("WM_DELETE_WINDOW", self.close)
        self.title(kwargs.get('title', self.identifier()))
        self.minsize(
            width=self.properties.min_size()[0],
            height=self.properties.min_size()[1]
        )
        if self.properties.max_size() is not None:
            self.maxsize(
                width=self.properties.max_size()[0],
                height=self.properties.max_size()[1]
            )
        self.geometry(
            f'{self.properties.min_size()[0]}x{self.properties.min_size()[1]}'
            f'+{self.initial_coordinates()[0]}+{self.initial_coordinates()[1]}'
        )
        self.resizable(
            kwargs.get('resizability', (True, True))[0],
            kwargs.get('resizability', (True, True))[1]
        )
        # Visibility bind here (see old 'ftk.py' for more details)
