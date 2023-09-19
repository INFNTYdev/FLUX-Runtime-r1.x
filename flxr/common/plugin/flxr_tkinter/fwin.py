
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
