
"""
Base FLUX-Tkinter View Property Manager Module
"""


#   EXTERNAL IMPORTS
from flxr.common.protocols import FwV


#   MODULE CLASS
class FwvPropertyManager:
    def __init__(self, ftk: FwV, master, **kwargs) -> None:
        """ Base framework view property manager """
        self.__ftk: FwV = ftk
        self.__master = master
        self.__main: bool = False
        self.__dynamic: bool = None
        self.__size_lock: bool = False
        self.__background: str = kwargs.get('bg')

    def is_main(self) -> bool:
        """ Returns true if framework
        view is main view """
        return self.__main

    def is_dynamic(self) -> bool:
        """ Returns true if framework view
        is of dynamic characteristic """
        return self.__dynamic is True

    def is_static(self) -> bool:
        """ Returns true if framework view
        is of static characteristic """
        return self.__dynamic is False

    def background(self) -> str:
        """ Returns framework view
        hexadecimal background color """
        return self.__background

    def size_locked(self) -> bool:
        """ Returns true if framework
        view size is locked """
        return self.__size_lock

    def parent(self) -> any:
        """ Returns framework
        view parent if any """
        return self.__master

    def width(self) -> int:
        """ Returns framework view width """
        if self.__ftk.hfw_service('tkinterAlive') is False:
            return 1
        return self.__ftk.winfo_width()

    def height(self) -> int:
        """ Returns framework view height """
        if self.__ftk.hfw_service('tkinterAlive') is False:
            return 1
        return self.__ftk.winfo_height()

    def coordinates(self) -> tuple[tuple, tuple, tuple, tuple]:
        """ Returns framework view
        4-corner coordinates """
        x1, y1 = (self.__ftk.winfo_rootx(), self.__ftk.winfo_rooty())
        y2, x3 = (y1+self.__ftk.winfo_height(), x1+self.__ftk.winfo_width())
        return (x1, y1), (x1, y2), (x3, y2), (x3, y1)

    def set_as_main(self, main: bool = True) -> None:
        """ Set framework view
        as main view """
        if main is not self.__main:
            self.__main = main

    def set_characteristic(self, **kwargs) -> None:
        """ Update framework
        view characteristics """
        if kwargs.get('dynamic') is not None:
            if bool(kwargs.get('dynamic')) is not self.__dynamic:
                self.__dynamic = bool(kwargs.get('dynamic'))

        if kwargs.get('main') is not None:
            if bool(kwargs.get('main')) is not self.__main:
                self.__main = bool(kwargs.get('main'))

    def set_background(self, bg: str) -> None:
        """ Set framework view background """
        if bg == self.__background:
            return
        self.__ftk.config(bg=bg)
        self.__background = bg

    def lock_size(self) -> None:
        """ Lock framework view size """
        if not self.size_locked():
            self.__size_lock = True

    def unlock_size(self) -> None:
        """ Unlock framework view size """
        if self.size_locked():
            self.__size_lock = False

    def set_size(self, width: int, height: int) -> None:
        """ Set framework view size """
        if (width == self.width()) and (height == self.height()):
            return
        if self.__size_lock:
            return
        if self.__ftk.view_type() == 'FTkWindow':
            self.__ftk.geometry(f"{width}x{height}")
            self.__ftk.update()
        elif self.__ftk.view_type() == 'FTkView':
            self.__ftk.config(width=width, height=height)

    def set_relative_size(self, width: float, height: float) -> None:
        """ Set framework view relative size """
        if self.parent() is None:
            self.set_size(
                width=int(self.__ftk.uclient.display_width()*width),
                height=int(self.__ftk.uclient.display_height()*height)
            )
        else:
            try:
                self.set_size(
                    width=int(self.parent().properties.width()*width),
                    height=int(self.parent().properties.height()*height)
                )
            except AttributeError:
                self.set_size(
                    width=int(self.parent().winfo_width()*width),
                    height=int(self.parent().winfo_height()*height)
                )

    def set_width(self, width: int) -> None:
        """ Set framework view width """
        if width != self.width():
            self.set_size(width=width, height=self.height())

    def set_height(self, height: int) -> None:
        """ Set framework view height """
        if height != self.height():
            self.set_size(width=self.width(), height=height)

    def set_relative_width(self, width: float) -> None:
        """ Set framework view relative width """
        # TODO: Determine how the relative width will be set

    def set_relative_height(self, height: float) -> None:
        """ Set framework view relative height """
        # TODO: Determine how the relative height will be set
