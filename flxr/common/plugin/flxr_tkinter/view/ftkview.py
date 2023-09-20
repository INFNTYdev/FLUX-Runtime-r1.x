
"""
Base FLUX Framework Tkinter View Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
import tkinter as tk


#   EXTERNAL IMPORTS
from .fwvm import FwVm
from flxr.common.protocols import Flux
from simplydt import DateTime


#   MODULE CLASS
class FTkView(tk.Frame, FwVm):
    def __init__(self, hfw: Flux, cls: type, uid: str, parent: any, **kwargs) -> None:
        """ Base FLUX runtime framework tkinter view """
        tk.Frame.__init__(
            self,
            master=parent,
            padx=kwargs.get('padx', 0),
            pady=kwargs.get('pady', 0),
            highlightthickness=kwargs.get('border', 0),
            highlightbackground=kwargs.get('border_bg', '#000000'),
            bg=kwargs.get('bg', 'gray'),
            cursor=kwargs.get('cursor', 'arrow'),
            relief=kwargs.get('relief', 'flat')
        )
        FwVm.__init__(self, hfw=hfw, cls=cls, uid=uid, parent=parent, **kwargs)
        self.properties.parent().event.new_bind(event='<Configure>', func=self.__view_configure_event)
        self.pack_propagate(False)
        self.grid_propagate(False)

    def view_type(self) -> str: return FTkView.__name__

    def console(self, msg: str, error: bool = False, **kwargs) -> None:
        """ Send text to the framework
        console for logging """
        super().console(
            msg=f"< {self.fwm_name()}: {self.identifier()} > - {msg}",
            error=error,
            **kwargs
        )

    def hide(self) -> None:
        """ Hide view """
        pass

    def show(self) -> None:
        """ Show view """
        pass

    def take_focus(self) -> None:
        """ Give view focus """
        self.tkraise()
        self.focus_set()
        self.event.update_focus(focus=True)
        self.console(msg=f"took focus")

    def __view_configure_event(self, event: tk.Event) -> None:
        """ Handle view configure event """
        if event.width != self.properties.relative_width():
            self.properties.set_width(width=self.properties.relative_width())
        if event.height != self.properties.relative_height():
            self.properties.set_height(height=self.properties.relative_height())
