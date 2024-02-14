
"""
Base FLUX Framework Tkinter Window Module
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
class FTkWindow(FwVm):
    def __init__(self, hfw: Flux, cls: type, uid: str, parent: any = None, **kwargs) -> None:
        """ Base FLUX runtime framework tkinter window view """
        super().__init__(hfw=hfw, cls=cls, uid=uid, parent=parent, **kwargs)
        self.__initial_coordinates: tuple[int, int] = kwargs.get('coord', self.default_coordinates())
        self.__last_width: int = None
        self.__last_height: int = None
        self.__last_x_position: int = None
        self.__last_y_position: int = None
        self.__size_last_updated: DateTime = None
        self.__position_last_updated: DateTime = None
        self.__size_recapture: bool = False
        self.__position_recapture: bool = False
        self.event.new_bind(event='<Configure>', func=self.__window_configure_event)

    def view_type(self) -> str: return FTkWindow.__name__

    def console(self, msg: str, error: bool = False, **kwargs) -> None:
        """ Send text to the framework
        console for logging """
        super().console(
            msg=f"( {self.fwm_name()}: {self.identifier()} ) - {msg}",
            error=error,
            **kwargs
        )

    def initial_coordinates(self) -> tuple[int, int]:
        """ Returns window intital
        spawn coordinates """
        return self.__initial_coordinates

    def center_x_position(self) -> int:
        """ Returns window
        center x coordinate """
        if self.hfw_service('tkinterAlive') is False:
            return int((self.uclient.display_width()/2)-(self.properties.relative_width()/2))
        return int((self.uclient.display_width()/2)-(self.properties.width()/2))

    def center_y_position(self) -> int:
        """ Returns window
        center y coordinate """
        if self.hfw_service('tkinterAlive') is False:
            return int((self.uclient.display_height()/2)-(self.properties.relative_height()/2))
        return int((self.uclient.display_height()/2)-(self.properties.height()/2))

    def default_coordinates(self) -> tuple[int, int]:
        """ Returns window
        default coordinates """
        return self.center_x_position(), self.center_y_position()

    def minimize(self) -> None:
        """ Minimize window """
        self.iconify()
        self.event.update_visibility(visible=False)
        self.console(msg=f"Minimized '{self.identifier()}' window")

    def maximize(self) -> None:
        """ Maximize window """
        self.state('zoomed')
        self.event.update_visibility(visible=True)
        self.console(msg=f"Maximized '{self.identifier()}' window")

    def hide(self) -> None:
        """ Hide window """
        self.withdraw()
        self.event.update_visibility(visible=False)
        self.console(msg=f"'{self.identifier()}' window hidden")

    def show(self, lift: bool = True) -> None:
        """ Show window """
        self.deiconify()
        if lift:
            self.lift()
        self.event.update_visibility(visible=True)
        self.console(msg=f"'{self.identifier()}' window visible")

    def take_focus(self) -> None:
        """ Give window focus """
        self.focus_set()

    def close(self) -> None:
        """ Close window """
        self.event.update_visibility(visible=False)
        self.event.update_focus(focus=False)
        self.event.update_mouse(inbounds=False)
        self.destroy()
        self.console(msg=f"Closed '{self.identifier()}' window")

    def __last_updated(self, var: DateTime) -> tuple[int, int, int, int, int, int]:
        """ Returns time since
        provided datetime object """
        if var is None:
            return None
        return var.until(self.hfw_service('getDatetime'))

    def __capture_window_size(self) -> None:
        """ Record window current size """
        size: tuple = (self.properties.width(), self.properties.height())
        if not ((size[0] != self.__last_width) or (size[1] != self.__last_height)):
            return
        if self.__size_last_updated is None:
            self.__last_width = size[0]
            self.__last_height = size[1]
        elif self.__last_updated(self.__size_last_updated)[-1] > 0:
            self.__last_width = size[0]
            self.__last_height = size[1]
            self.console(
                msg=f"Captured window size @ [{self.__last_width}x{self.__last_height}]"
            )
            if self.__size_recapture is True:
                self.__size_recapture = False
        elif (self.__last_updated(self.__size_last_updated)[-1] <= 1) and (self.__size_recapture is False):
            self.__size_recapture = True
            self.after(1000, self.__capture_window_size)
            return
        self.__size_last_updated = self.hfw_service('getDatetime')

    def __capture_window_position(self) -> None:
        """ Record window current position """
        coord: tuple = self.properties.coordinates()[0]
        if not ((coord[0] != self.__last_x_position) or (coord[1] != self.__last_y_position)):
            return
        if self.__position_last_updated is None:
            self.__last_x_position = coord[0]
            self.__last_y_position = coord[1]
        elif self.__last_updated(self.__position_last_updated)[-1] > 0:
            self.__last_x_position = coord[0]
            self.__last_y_position = coord[1]
            self.console(
                msg=f"Captured window coord @ [{self.__last_x_position}, {self.__last_y_position}]"
            )
            if self.__position_recapture is True:
                self.__position_recapture = False
        elif (self.__last_updated(self.__position_last_updated)[-1] <= 1) and (self.__position_recapture is False):
            self.__position_recapture = True
            self.after(1300, self.__capture_window_position)
            return
        self.__position_last_updated = self.hfw_service('getDatetime')

    def __window_configure_event(self, event: tk.Event) -> None:
        """ Handle window configure event """
        self.__capture_window_size()
        self.__capture_window_position()
