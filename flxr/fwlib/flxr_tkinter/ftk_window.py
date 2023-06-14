
"""
FLUX Runtime-Framework Tkinter Window
"""


#   THIRD-PARTY IMPORTS
import ctypes


#   BUILT-IN IMPORTS
pass


#   EXTERNAL IMPORTS
from flxr.fwlib.flxr_tkinter import *


#   MODULE CLASS
class FTkWindow(tk.Tk):

    _DEFAULT_SIZE: tuple = (300, 200)
    _DEFAULT_RESIZE: tuple = (True, True)

    def __init__(self, fw: any, svc: any, root: tk.Tk, identifier: str, **kwargs) -> None:
        """
        FLUX tkinter application window

        :param fw: Hosting framework instance
        :param svc: Hosting framework service call
        :param root: Root tkinter.Tk window instance
        :param identifier: Window unique identifier
        :param kwargs: Additional base window configuration arguments
        """
        #self.__HFW = fw_obj(fw)
        self.__S = svc
        self.__root_window = root
        self.__identifier: str = identifier

        self._window_ready: bool = False
        self._window_min: tuple = kwargs.get('minsize', self._DEFAULT_SIZE)
        self._window_max: tuple = kwargs.get('maxsize')
        self._initial_x_pos, self._initial_y_pos = kwargs.get('coord', (self.center_screen_x(), self.center_screen_y()))
        self._resizability: tuple = kwargs.get('resizability', self._DEFAULT_RESIZE)
        self._active_window: bool = False
        self._mouse_in_bounds: bool = None
        self._focus_in_bounds: bool = None
        self._MASTER_BIND_EVENT: dict = {
            '<Enter> <Leave>': self._master_hover_event,
            '<Button-1> <Button-3>': self._master_click_event,
            '<FocusIn> <FocusOut>': self._master_focus_event,
            '<Configure>': self._master_configure_event,
        }
        self._WINDOW_CONFIGURATION: dict = kwargs.get('config', {})
        super().__init__()
        self.overrideredirect(kwargs.get('borderless', False))
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.title(kwargs.get('title', self.__identifier))
        self.minsize(
            width=self._window_min[0],
            height=self._window_min[1]
        )
        if self._window_max is not None:
            self.maxsize(
                width=self._window_max[0],
                height=self._window_max[1]
            )
        self.geometry(
            f"{self._window_min[0]}x{self._window_min[1]}"
            f"+{self._initial_x_pos}+{self._initial_y_pos}"
        )
        self.resizable(self._resizability[0], self._resizability[1])
        for _events, _function in self._MASTER_BIND_EVENT.items():
            for _event in _events.split(' '):
                self.bind(_event, _function, add="+")
        self._window_ready = True

    def minimize(self) -> None:
        """ Minimize the application window """
        self.iconify()
        self.console(f"Minimized window")

    def maximize(self) -> None:
        """ Maximize the application window """
        self.state('zoomed')
        self.console(f"Maximized window")

    def hide(self) -> None:
        """ Hide the application window """
        self.withdraw()
        self.console(f"Window hidden")

    def show(self, lift: bool = True) -> None:
        """ Show the application window """
        self.deiconify()
        if lift:
            self.lift()
        self.console(f"Window visible")

    def close(self) -> None:
        """ Close the application window """
        self._active_window = False
        self.destroy()
        self.console(f"Closed window")

    def identifier(self) -> str:
        """ Returns the application window unique identifier """
        return self.__identifier

    def width(self) -> int:
        """ Returns the width of the application window """
        if not self._window_ready:
            return self._window_min[0]
        return self.winfo_width()

    def height(self) -> int:
        """ Returns the height of the application window """
        if not self._window_ready:
            return self._window_min[1]
        return self.winfo_height()

    def screen_width(self) -> int:
        """ Returns the width of the user screen """
        return self._user_system().GetSystemMetrics(0)

    def screen_height(self) -> int:
        """ Returns the height of the user screen """
        return self._user_system().GetSystemMetrics(1)

    def coordinates(self) -> tuple[list, list, list, list]:
        """ Returns the coordinates of the application window """
        x1, y1 = (self.winfo_rootx(), self.winfo_rooty())
        y2, x3 = (y1+self.winfo_height(), x1+self.winfo_width())
        return [x1, y1], [x1, y2], [x3, y2], [x3, y1]

    def mouse_in_bounds(self) -> bool:
        """ Returns the mouse in application window bounds status """
        return self._mouse_in_bounds

    def window_focus(self) -> bool:
        """ Returns the application window focus status """
        return self._focus_in_bounds

    def center_screen_x(self) -> int:
        """ Returns the center of screen x-coordinate """
        return int((self.screen_width()/2)-(self.width()/2))

    def center_screen_y(self) -> int:
        """ Returns the center of screen y-coordinate """
        return int((self.screen_height()/2)-(self.height()/2))

    def ref(self, config: str) -> any:
        """ Returns the specified configuration value """
        if config in self._WINDOW_CONFIGURATION.keys():
            return self._WINDOW_CONFIGURATION[config]

    def console(self, msg: str, error: bool = False) -> None:
        """ Send text to the framework console """
        self.__S(FTkWindow)['console'](msg=f"{self.identifier()}: {msg}", error=error)

    @staticmethod
    def _user_system() -> ctypes.WinDLL:
        """ Returns the user system WinDLL """
        return ctypes.windll.user32

    def _master_configure_event(self, event: tk.Event) -> None:
        """ Handle window configuration events """
        pass

    def _master_focus_event(self, event: tk.Event) -> None:
        """ Handle window focus events """
        if str(event).__contains__('FocusIn'):
            if self._active_window is False:
                self._active_window = True
            self.console(f"Gained focus")
        elif str(event).__contains__('FocusOut'):
            self._focus_in_bounds = False

    def _master_hover_event(self, event: tk.Event) -> None:
        """ Handle window hover events """
        if str(event).__contains__('Enter'):
            self._mouse_in_bounds = True
        elif str(event).__contains__('Leave'):
            self._mouse_in_bounds = False

    def _master_click_event(self, event: tk.Event) -> None:
        """ Handle window click events """
        if self._focus_in_bounds is False:
            self._focus_in_bounds = True

        if str(event).__contains__('num=1'):
            pass
        elif str(event).__contains__('num=3'):
            pass
