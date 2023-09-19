
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
    def __init__(self, client: FwV) -> None:
        """ FLUX framework view property manager """
        self.__fwv: FwV = client
        self.__main: bool = False
        self.__dynamic: bool = True
        self.__min_size: tuple = ()
        self.__max_size: tuple = ()
        self.__relative_width: float = None
        self.__relative_height: float = None

    def is_main(self) -> bool:
        """ Returns true if framework
        view is main view """
        return self.__main

    def is_dynamic(self) -> bool:
        """ Returns true if framework
        view is dynamic """
        return self.__dynamic

    def parent(self) -> any:
        """ Returns framework
        view parent if any """
        pass

    def min_size(self) -> tuple[int, int]:
        """ Returns framework view
        minimum screen realestate """
        pass

    def max_size(self) -> tuple[int, int]:
        """ Returns framework view
        maximum screen realestate """
        pass

    def width(self) -> int:
        """ Returns framework view width """
        pass

    def height(self) -> int:
        """ Returns framework view height """
        pass

    def relative_width(self) -> float:
        """ Returns framework view width """
        pass

    def relative_height(self) -> float:
        """ Returns framework view height """
        pass

    def coordinates(self) -> tuple[tuple, tuple, tuple, tuple]:
        """ Returns framework view
        4-corner coordinates """
        pass

    def set_as_main(self, main: bool = True) -> None:
        """ Set framework view as main view """
        self.__main = main

    def set_min_size(self, width: int, height: int) -> None:
        """ Set framework view minimum size """
        pass

    def set_max_size(self, width: int, height: int) -> None:
        """ Set framework view maximum size """
        pass

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

    def capture_view_geometry(self) -> None:
        """ Capture framework view geometry """
        pass
