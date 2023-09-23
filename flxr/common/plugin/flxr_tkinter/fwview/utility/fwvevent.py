
"""
Base FLUX-Tkinter View Event Handler Module
"""


#   BUILT-IN IMPORTS
import tkinter as tk
from typing import Callable


#   EXTERNAL IMPORTS
from flxr.common.protocols import FwV


#   MODULE CLASS
class FwvEventHandler:
    def __init__(self, ftk: FwV) -> None:
        """ Base framework view event handler """
        self.__ftk: FwV = ftk
        self.__bindings: list[tuple[str, Callable]] = []
        self.__visible: bool = False
        self.__focus_inbounds: bool = False
        self.__mouse_inbounds: bool = False
        self.__SUPER_EVENT_BIND: dict = {
            '<Visibility>': self.__super_visibility_event,
            '<FocusIn> <FocusOut>': self.__super_focus_event,
            '<Enter> <Leave>': self.__super_hover_event,
            '<ButtonPress-1> <ButtonRelease-1>': self.__super_click_event
        }
        for _events, _function in self.__SUPER_EVENT_BIND.items():
            self.bind(event=_events, func=_function)

    def ftk(self) -> FwV:
        return self.__ftk

    def bindings(self) -> list[tuple[str, Callable]]:
        """ Returns list of
        framework view bindings """
        return self.__bindings

    def visible(self) -> bool:
        """ Returns true if framework
        view is currently visible """
        return self.__visible

    def focus_inbounds(self) -> bool:
        """ Returns true if framework
        view currently has focus """
        return self.__focus_inbounds

    def mouse_inbounds(self) -> bool:
        """ Returns true if framework view
        is currently underneath mouse """
        return self.__mouse_inbounds

    def managed_event(self, event: str) -> bool:
        """ Returns true if provided
        event already has a binding """
        return len([_bind for _bind in self.bindings() if _bind[0] == event]) > 0

    def bind(self, event: str, func: Callable) -> None:
        """ Add event binding
        to framework view """
        for _event in event.split(' '):
            if not self.managed_event(_event):
                self.__ftk.bind(_event, func)
            else:
                self.__ftk.bind(_event, func, add='+')
            self.__bindings.append((_event, func))

    def update(self, **kwargs) -> None:
        """ Update framework view event flags """
        if kwargs.get('visibility') is not None:
            if bool(kwargs.get('visibility')) is not self.__visible:
                self.__visible = bool(kwargs.get('visibility'))

        if kwargs.get('focus_inbounds') is not None:
            if bool(kwargs.get('focus_inbounds')) is not self.__focus_inbounds:
                self.__focus_inbounds = bool(kwargs.get('focus_inbounds'))

        if kwargs.get('mouse_inbounds') is not None:
            if bool(kwargs.get('mouse_inbounds')) is not self.__mouse_inbounds:
                self.__mouse_inbounds = bool(kwargs.get('mouse_inbounds'))

    def __super_visibility_event(self, event: tk.Event) -> None:
        """ Handle framework view visibility event """
        if event.state == 'VisibilityUnobscured':
            if self.visible() is False:
                self.update(visibility=True)
                self.__ftk.console(msg=f"view visible")
        else:
            self.__ftk.console(msg=f"Unknown visibility event: {event}", notice=True)

    def __super_focus_event(self, event: tk.Event) -> None:
        """ Handle framework view focus event """
        if str(event).__contains__('FocusIn'):
            if not self.focus_inbounds():
                self.update(focus_inbounds=True)
                self.__ftk.console(msg=f"gained focus")
        elif str(event).__contains__('FocusOut'):
            if self.focus_inbounds():
                self.update(focus_inbounds=False)
                self.__ftk.console(msg=f"lost focus")

    def __super_hover_event(self, event: tk.Event) -> None:
        """ Handle framework view hover event """
        if str(event).__contains__('Enter'):
            self.update(mouse_inbounds=True)
        elif str(event).__contains__('Leave'):
            self.update(mouse_inbounds=False)

    def __super_click_event(self, event: tk.Event) -> None:
        """ Handle framework view click event """
        if str(event).__contains__('Press'):
            if not self.focus_inbounds():
                self.update(focus_inbounds=True)
        elif str(event).__contains__('Release'):
            pass
