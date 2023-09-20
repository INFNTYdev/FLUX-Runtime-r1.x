
"""
FLUX Framework View Event Handler Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
import tkinter as tk


#   EXTERNAL IMPORTS
from flxr.common import FwV


#   MODULE CLASS
class FwvEventHandler:
    def __init__(self, client: FwV) -> None:
        """ FLUX framework view event handler """
        self.__fwv: FwV = client
        self.__bindings: list[tuple] = []
        self.__visible: bool = False
        self.__focus_in_bounds: bool = False
        self.__mouse_in_bounds: bool = False
        self.__MASTER_EVENT_BIND: dict = {
            '<Visibility>': self.__master_visibility_event,
            '<FocusIn> <FocusOut>': self.__master_focus_event,
            '<Enter> <Leave>': self.__master_hover_event,
            '<Button-1> <Button-3>': self.__master_click_event,
        }
        for _events, _function in self.__MASTER_EVENT_BIND.items():
            self.new_bind(_events, _function)

    def visible(self) -> bool:
        """ Returns true if framework
        view is visible """
        return self.__visible

    def focus_in_bounds(self) -> bool:
        """ Returns true if focus
        is inside framework view """
        return self.__focus_in_bounds

    def mouse_in_bounds(self) -> bool:
        """ Returns true if mouse
        is inside framework view """
        return self.__mouse_in_bounds

    def managed_event(self, event: str) -> bool:
        """ Returns true if provided
        event already has a binding """
        for _bind in self.__bindings:
            if _bind[0] == event:
                return True
        return False

    def new_bind(self, event: str, func) -> None:
        """ Add binding to framework view """
        for _event in event.split(' '):
            if not self.managed_event(_event):
                self.__fwv.bind(_event, func)
            else:
                self.__fwv.bind(_event, func, add='+')
            self.__bindings.append((_event, func))

    def update_visibility(self, visible: bool) -> None:
        """ Update framework
        view visibility flag """
        if visible is not self.__visible:
            self.__visible = visible

    def update_focus(self, focus: bool) -> None:
        """ Update framework
        view focus flag """
        if focus is not self.__focus_in_bounds:
            self.__focus_in_bounds = focus

    def update_mouse(self, inbounds: bool) -> None:
        """ Update framework view
        mouse inbounds flag """
        if inbounds is not self.__mouse_in_bounds:
            self.__mouse_in_bounds = inbounds

    def __master_visibility_event(self, event: tk.Event) -> None:
        """ Handle framework view visibility event """
        if event.state == 'VisibilityUnobscured':
            self.update_visibility(visible=True)
            self.__fwv.console(msg=f"view visible")

    def __master_focus_event(self, event: tk.Event) -> None:
        """ Handle framework view focus event """
        if str(event).__contains__('FocusIn'):
            self.update_focus(focus=True)
            self.__fwv.console(msg=f"gained focus")
        elif str(event).__contains__('FocusOut'):
            self.update_focus(focus=False)
            self.__fwv.console(msg=f"lost focus")

    def __master_hover_event(self, event: tk.Event) -> None:
        """ Handle framework view hover event """
        if str(event).__contains__('Enter'):
            self.update_mouse(inbounds=True)
        elif str(event).__contains__('Leave'):
            self.update_mouse(inbounds=False)

    def __master_click_event(self, event: tk.Event) -> None:
        """ Handle framework view click event """
        self.update_focus(focus=True)
