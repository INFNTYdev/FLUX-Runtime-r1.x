
"""
FLUX Runtime Framework Subsidiary Window
"""


#   BUILT-IN IMPORTS
import tkinter as tk
import ctypes


#   EXTERNAL IMPORTS
from .fwview import FTkWindow


#   MODULE CLASS
class FluxSubWindow(tk.Toplevel, FTkWindow):
    def __init__(self, hfw, cls: type, uid: str, parent: any = None, **kwargs) -> None:
        """ FLUX subsidiary window """
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        tk.Toplevel.__init__(self)
        FTkWindow.__init__(
            self,
            hfw=hfw,
            cls=cls,
            uid=uid,
            parent=parent,
            bg=kwargs.get('bg'),
            minsize=kwargs.get('minsize', (250, 250)),
            maxsize=kwargs.get('maxsize'),
            coord=kwargs.get('coord'),
            title=kwargs.get('title', uid),
            borderless=kwargs.get('borderless', False),
            resizability=kwargs.get('resizability', (True, True)),
            trans_key=kwargs.get('trans_key'),
            opacity=kwargs.get('opacity', 1.0)
        )
        self.config(bg=self.properties.background())
        self.attributes('-alpha', self.properties.opacity())
        if self.properties.transparency_key() is not None:
            self.wm_attributes("-transparent", self.properties.transparency_key())
            self.update()
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
            f"{self.properties.min_size()[0]}x{self.properties.min_size()[1]}"
            f"+{self.properties.initial_coordinates()[0]}+{self.properties.initial_coordinates()[1]}"
        )
        self.title(self.properties.title())
        self.overrideredirect(self.properties.borderless())
        self.resizable(self.properties.resizability()[0], self.properties.resizability()[0])
        self.state(kwargs.get('state', 'normal'))
