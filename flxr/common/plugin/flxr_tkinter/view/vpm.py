
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
        self.__min_size: tuple = kwargs.get('minsize', (0, 0))
        self.__max_size: tuple = kwargs.get('maxsize')
        self.__relative_width: float = kwargs.get('rel_width', 40)/100
        self.__relative_height: float = kwargs.get('rel_height', 30)/100

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

    def relative_width(self) -> int:
        """ Returns framework view
        calculated relative width """
        if self.__fwv_master is None:
            return int(self.__fwv.uclient.display_width()*self.__relative_width)
        else:
            try:
                return int(self.parent().properties.width()*self.__relative_width)
            except AttributeError:
                return int(self.parent().winfo_width()*self.__relative_width)

    def relative_height(self) -> int:
        """ Returns framework view
        calculated relative height """
        if self.__fwv_master is None:
            return int(self.__fwv.uclient.display_height()*self.__relative_height)
        else:
            try:
                return int(self.parent().properties.height()*self.__relative_height)
            except AttributeError:
                return int(self.parent().winfo_height()*self.__relative_height)

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
        if width < self.__min_size[0]:
            return
        if self.__max_size is not None:
            if width > self.__max_size[0]:
                return
        if self.__fwv.view_type() == 'FTkWindow':
            self.__fwv.geometry(f'{width}x{self.height()}')
        elif self.__fwv.view_type() == 'FTkView':
            self.__fwv.config(width=width)

    def set_height(self, height: int) -> None:
        """ Set framework view height """
        if height < self.__min_size[1]:
            height = self.__min_size[1]
        if self.__max_size is not None:
            if height > self.__max_size[1]:
                height = self.__max_size[1]
        if self.__fwv.view_type() == 'FTkWindow':
            self.__fwv.geometry(f'{self.width()}x{height}')
        elif self.__fwv.view_type() == 'FTkView':
            self.__fwv.config(height=height)

    def set_relative_width(self, width: int) -> None:
        """ Set framework view relative width """
        if (width < 0) or (width > 100):
            return
        if self.__fwv_master is None:
            _relative_width = int(self.__fwv.uclient.display_width()*(width/100))
        else:
            try:
                _relative_width = int(self.parent().properties.width()*(width/100))
            except AttributeError:
                _relative_width = int(self.parent().winfo_width()*(width/100))
        if self.__fwv.view_type() == 'FTkWindow':
            self.__fwv.geometry(
                f'{_relative_width}x{self.height()}'
            )
        elif self.__fwv.view_type() == 'FTkView':
            self.__fwv.config(width=_relative_width)

    def set_relative_height(self, height: int) -> None:
        """ Set framework view relative height """
        if (height < 0) or (height > 100):
            return
        if self.__fwv_master is None:
            _relative_height = int(self.__fwv.uclient.display_height()*(height/100))
        else:
            try:
                _relative_height = int(self.parent().properties.height()*(height/100))
            except AttributeError:
                _relative_height = int(self.parent().winfo_height()*(height/100))
        if self.__fwv.view_type() == 'FTkWindow':
            self.__fwv.geometry(
                f'{self.width()}x{_relative_height}'
            )
        elif self.__fwv.view_type() == 'FTkView':
            self.__fwv.config(height=_relative_height)
