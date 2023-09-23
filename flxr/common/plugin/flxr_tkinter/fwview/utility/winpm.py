
"""
FLUX-Tkinter Window View Property Manager Module
"""


#   EXTERNAL IMPORTS
from flxr.common.protocols import FwV
from .fwvpm import FwvPropertyManager


#   MODULE CLASS
class WindowPropertyManager(FwvPropertyManager):
    def __init__(self, ftk: FwV, master, **kwargs) -> None:
        """ Framework window view property manager """
        super().__init__(ftk=ftk, master=master, **kwargs)
        self.__min_size: tuple = kwargs.get('minsize')
        self.__max_size: tuple = kwargs.get('maxsize')
        self.__initial_coordinates: tuple = kwargs.get('coord')
        if self.__initial_coordinates is None:
            self.__initial_coordinates = self.default_coordinates()
        self.__title: str = kwargs.get('title')
        self.__override_wm: bool = kwargs.get('borderless')
        self.__resizability: tuple = kwargs.get('resizability')
        self.__transparency_key: str = kwargs.get('trans_key')
        self.__opacity: float = kwargs.get('opacity')

    def min_size(self) -> tuple[int, int]:
        """ Returns framework window
        minimum dimensions """
        return self.__min_size

    def max_size(self) -> tuple[int, int]:
        """ Returns framework window
        maximum dimensions """
        return self.__max_size

    def initial_coordinates(self) -> tuple[int, int]:
        """ Returns framework window
        spawn coordinates """
        return self.__initial_coordinates

    def center_x_position(self) -> int:
        """ Returns framework window
        center x coordinate """
        if self.ftk().hfw_service('tkinterAlive') is False:
            return int((self.ftk().uclient.display_width()/2)-(self.__min_size[0]/2))
        return int((self.ftk().uclient.display_width()/2)-(self.ftk().properties.width()/2))

    def center_y_position(self) -> int:
        """ Returns framework window
        center y coordinate """
        if self.ftk().hfw_service('tkinterAlive') is False:
            return int((self.ftk().uclient.display_height()/2)-(self.__min_size[1]/2))
        return int((self.ftk().uclient.display_height()/2)-(self.ftk().properties.height()/2))

    def default_coordinates(self) -> tuple[int, int]:
        """ Returns framework window
        default center coordinates """
        return self.center_x_position(), self.center_y_position()

    def title(self) -> str:
        """ Returns framework
        window title """
        return self.__title

    def borderless(self) -> bool:
        """ Returns true if framework window is
        configured to override window manager """
        return self.__override_wm

    def resizability(self) -> tuple[bool, bool]:
        """ Returns framework window resizibility
        configuration (width, height) """
        return self.__resizability

    def transparency_key(self) -> str:
        """ Returns framework
        window transparency key """
        return self.__transparency_key

    def opacity(self) -> float:
        """ Returns framework window
        opacity percentage """
        return self.__opacity

    def set_characteristic(self, **kwargs) -> None:
        if kwargs.get('borderless') is not None:
            if bool(kwargs.get('borderless')) is not self.__override_wm:
                self.ftk().overrideredirect(bool(kwargs.get('borderless')))
                self.__override_wm = bool(kwargs.get('borderless'))
        if kwargs.get('trans_key') is not None:
            if kwargs.get('trans_key') != self.__transparency_key:
                self.ftk().wm_attributes("-transparent", kwargs.get('trans_key'))
                self.__transparency_key = kwargs.get('trans_key')
                self.ftk().update()
        super().set_characteristic(
            dynamic=kwargs.get('dynamic'),
            main=kwargs.get('main')
        )

    def set_min_size(self, width: int, height: int) -> None:
        """ Set framework window
        minimum dimensions """
        if self.size_locked():
            return
        if (width != self.min_size()[0]) or (height != self.min_size()[1]):
            self.ftk().minsize(width=width, height=height)
            self.__min_size = width, height

    def set_max_size(self, width: int, height: int) -> None:
        """ Set framework window
        maximum dimensions """
        if self.size_locked():
            return
        if (width != self.max_size()[0]) or (height != self.max_size()[1]):
            self.ftk().maxsize(width=width, height=height)
            self.__max_size = width, height

    def set_coordinates(self, coord: tuple[int, int]) -> None:
        """ Set framework window coordinates """
        if coord != self.coordinates()[0]:
            self.ftk().geometry(f"+{int(coord[0])}+{int(coord[1])}")

    def set_x_position(self, x: int) -> None:
        """ Set framework window x coordinate """
        self.set_coordinates(coord=(x, self.coordinates()[0][1]))

    def set_y_position(self, y: int) -> None:
        """ Set framework window y coordinate """
        self.set_coordinates(coord=(self.coordinates()[0][0], y))

    def set_title(self, title: str) -> None:
        """ Set framework window title """
        if title != self.title():
            self.ftk().title(title)
            self.__title = title
