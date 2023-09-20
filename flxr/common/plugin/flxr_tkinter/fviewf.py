
"""
FLUX Framework Tkinter Viewframe Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
import tkinter as tk


#   EXTERNAL IMPORTS
from .view import FTkView
from flxr.common.protocols import Flux


#   MODULE CLASS
class FluxViewframe(FTkView):
    def __init__(self, hfw: Flux, cls: type, uid: str, parent: any, **kwargs) -> None:
        """ Base FLUX runtime framework tkinter viewframe """
        super().__init__(hfw=hfw, cls=cls, uid=uid, parent=parent, **kwargs)
