
"""
Base FLUX Framework Tkinter Window Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
pass


#   EXTERNAL IMPORTS
from .fwvm import FwVm
from flxr.common.protocols import Flux
from simplydt import DateTime


#   MODULE CLASS
class FTkWindow(FwVm):
    def __init__(self, hfw: Flux, cls: type, uid: str, parent: any = None, **kwargs) -> None:
        """ Base FLUX runtime framework tkinter window """
        super().__init__(hfw=hfw, cls=cls, uid=uid, parent=parent, **kwargs)
        self.__initial_coordinates: tuple[int, int] = ()
        self.__last_width: int = None
        self.__last_height: int = None
        self.__last_x_position: int = None
        self.__last_y_position: int = None
        self.__size_last_updated: DateTime = None
        self.__position_last_updated: DateTime = None
        self.__size_recapture: bool = False
        self.__position_recapture: bool = False

    def initial_coordinates(self) -> tuple[int, int]:
        """ Returns window intital
        spawn coordinates """
        pass

    def center_x_position(self) -> int:
        """ Returns window
        center x coordinate """
        pass

    def center_y_coordinate(self) -> int:
        """ Returns window
        center y coordinate """
        pass

    def default_coordinates(self) -> tuple[int, int]:
        """ Returns window
        default coordinates """
        pass

    def minimize(self) -> None:
        """ Minimize window """
        pass

    def maximize(self) -> None:
        """ Maximize window """
        pass

    def hide(self) -> None:
        """ Hide window """
        pass

    def show(self) -> None:
        """ Show window """
        pass

    def take_focus(self) -> None:
        """ Give window focus """
        pass

    def close(self) -> None:
        """ Close window """
        pass
