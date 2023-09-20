
"""
FLUX Framework View Property Manager Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
import tkinter as tk


#   EXTERNAL IMPORTS
from flxr.common import FwV


#   MODULE CLASS
class FwvPropertyManager:
    def __init__(self, client: FwV, parent: FwV, **kwargs) -> None:
        """ FLUX framework view property manager """
        self.__fwv: FwV = client
        self.__fwv_master: FwV = parent
        self.__main: bool = False
        self.__dynamic: bool = True
        self.__min_size: tuple = kwargs.get('minsize', (400, 200))
        self.__max_size: tuple = kwargs.get('maxsize')
        self.__relative_width: float = kwargs.get('rel_width', 50)/100
        self.__relative_height: float = kwargs.get('rel_height', 50)/100

    def is_main(self) -> bool:
        """ Returns true if framework
        view is main view """
        return self.__main

    def is_dynamic(self) -> bool:
        """ Returns true if framework
        view is dynamic """
        return self.__dynamic

    def parent(self) -> FwV:
        """ Returns framework
        view parent if any """
        return self.__fwv_master

    def min_size(self) -> tuple[int, int]:
        """ Returns framework view
        minimum screen realestate """
        return self.__min_size

    def max_size(self) -> tuple[int, int]:
        """ Returns framework view
        maximum screen realestate """
        return self.__max_size

    def __calculate_relative_width(self) -> int:
        """ Returns framework view
        calculated relative width """
        if self.__fwv_master is None:
            pass
        else:
            return int(self.parent().properties.width()*self.__relative_width)

    def __calculate_relative_height(self) -> int:
        """ Returns framework view
        calculated relative height """
        if self.__fwv_master is None:
            pass
        else:
            return int(self.parent().properties.height()*self.__relative_height)

    def width(self) -> int:
        """ Returns framework view width """
        if self.__fwv.hfw_service('tkinterAlive') is False:
            return self.__min_size[0]
        return self.__fwv.winfo_width()

    def height(self) -> int:
        """ Returns framework view height """
        if self.__fwv.hfw_service('tkinterAlive') is False:
            return self.__min_size[1]
        return self.__fwv.winfo_height()

    def coordinates(self) -> tuple[tuple, tuple, tuple, tuple]:
        """ Returns framework view
        4-corner coordinates """
        x1, y1 = (self.__fwv.winfo_rootx(), self.__fwv.winfo_rooty())
        y2, x3 = (y1 + self.__fwv.winfo_height(), x1 + self.__fwv.winfo_width())
        return (x1, y1), (x1, y2), (x3, y2), (x3, y1)

    def set_as_main(self, main: bool = True) -> None:
        """ Set framework view as main view """
        if main is not self.__main:
            self.__main = main

    def set_min_size(self, width: int, height: int) -> None:
        """ Set framework view minimum size """
        self.__min_size = width, height

    def set_max_size(self, width: int, height: int) -> None:
        """ Set framework view maximum size """
        self.__max_size = width, height

    def set_width(self, width: int) -> None:
        """ Set framework view width """
        pass

    def set_height(self, height: int) -> None:
        """ Set framework view height """
        pass

    def set_relative_width(self, width: int) -> None:
        """ Set framework view relative width """
        pass

    def set_relative_height(self, height: int) -> None:
        """ Set framework view relative height """
        pass

    def view_geometry_event(self, event: tk.Event) -> None:
        """ Capture framework view geometry """
        pass
