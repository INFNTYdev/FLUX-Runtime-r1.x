
"""
FLUX-Tkinter Window View Event Handler Module
"""


#   BUILT-IN IMPORTS
import tkinter as tk


#   EXTERNAL IMPORTS
from flxr.common.protocols import FwV
from .fwvevent import FwvEventHandler
from simplydt import DateTime


#   MODULE CLASS
class WindowEventHandler(FwvEventHandler):
    def __init__(self, ftk: FwV) -> None:
        """ Framework window view event handler """
        super().__init__(ftk=ftk)
        self.__last_width: int = None
        self.__last_height: int = None
        self.__last_x: int = None
        self.__last_y: int = None
        self.__size_last_updated: DateTime = None
        self.__position_last_updated: DateTime = None
        self.__size_recapture: bool = False
        self.__position_recapture: bool = False
        self.bind(event='<Configure>', func=self.__master_configure_event)

    def window_moving(self) -> bool:
        """ Returns true if the framework
        window is currently moving """
        # TODO: Determine window moving flag logic

    def __last_updated(self, dt: DateTime) -> tuple[int, int, int]:
        """ Returns time since the
        provided datetime (HH:MM:ss) """
        if dt is None:
            return None
        return dt.until(self.ftk().hfw_service('getDatetime'))[-3:]

    def __capture_window_size(self) -> None:
        """ Record framework window size """
        size: tuple = (self.ftk().properties.width(), self.ftk().properties.height())
        if not ((size[0] != self.__last_width) or (size[1] != self.__last_height)):
            return
        if self.__size_last_updated is None:
            self.__last_width = size[0]
            self.__last_height = size[1]
        elif self.__last_updated(self.__size_last_updated)[-1] > 0:
            self.__last_width = size[0]
            self.__last_height = size[1]
            self.ftk().console(msg=f"Captured window size @ [{self.__last_width}x{self.__last_height}]")
            if self.__size_recapture is True:
                self.__size_recapture = False
        elif (self.__last_updated(self.__size_last_updated)[-1] <= 1) and (self.__size_recapture is False):
            self.__size_recapture = True
            self.ftk().after(1000, self.__capture_window_size)
            return
        self.__size_last_updated = self.ftk().hfw_service('getDatetime')

    def __capture_window_position(self) -> None:
        """ Record framework window position """
        coord: tuple = self.ftk().properties.coordinates()[0]
        if not ((coord[0] != self.__last_x) or (coord[1] != self.__last_y)):
            return
        if self.__position_last_updated is None:
            self.__last_x = coord[0]
            self.__last_y = coord[1]
        elif self.__last_updated(self.__position_last_updated)[-1] > 0:
            self.__last_x = coord[0]
            self.__last_y = coord[1]
            self.ftk().console(msg=f"Captured window coord @ ({self.__last_x}, {self.__last_y})")
            if self.__position_recapture is True:
                self.__position_recapture = False
        elif (self.__last_updated(self.__position_last_updated)[-1] <= 1) and (self.__position_recapture is False):
            self.__position_recapture = True
            self.ftk().after(1300, self.__capture_window_position)
            return
        self.__position_last_updated = self.ftk().hfw_service('getDatetime')

    def __master_configure_event(self, event: tk.Event) -> None:
        """ Handle framework window configure event """
        self.__capture_window_size()
        self.__capture_window_position()
