
"""
Base FLUX Tkinter Window Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
import ctypes
import tkinter as tk


#   EXTERNAL IMPORTS
from flxr.constant import SvcVars


#   MODULE CLASS
class FluxTk(tk.Tk):
    def __init__(self, hfw, cls, **kwargs) -> None:
        """ Base FLUX tkinter window """
        if not hfw.is_rfw():
            raise ValueError(
                f"Invalid framework parameter provided for {cls.__name__}"
            )

        self.__framework = hfw
        self.__type: type = cls
        self._injectables: list = []
        self._window_visible: bool = False
        self._window_min_size: tuple = kwargs.get('minsize')
        self._window_max_size: tuple = kwargs.get('maxsize')
        self._initial_x_pos, self._initial_y_pos = \
            kwargs.get('coord', self.default_coordinates())
        self._resizability: tuple = kwargs.get('resizability', (True, True))
        self._is_active_window: bool = False
        self._mouse_in_bounds: bool = False
        self._window_bindings: list[tuple] = []
        self._window_widgets: list = []
        self._WINDOW_CONFIGURATION: dict = kwargs.get('config', {})

        super().__init__()
        self.overrideredirect(kwargs.get('borderless', False))
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.title(kwargs.get('title', self.__type.__name__))
        self.minsize(width=self._window_min_size[0], height=self._window_min_size[1])
        if self._window_max_size is not None:
            self.maxsize(width=self._window_max_size[0], height=self._window_max_size[1])
        self.geometry(
            f'{self._window_min_size[0]}x{self._window_min_size[1]}'
            f'+{self._initial_x_pos}+{self._initial_y_pos}'
        )
        self.resizable(self._resizability[0], self._resizability[1])
        self.new_bind('<Visibility>', self._super_visibility_event)

    def test_func(self, event: tk.Event):
        self.console(msg="#", notice=True)

    def width(self) -> int:
        """ Returns FLUX tkinter window width """
        if self.fw_svc('tkinterAlive') is False:
            return self._window_min_size[0]
        return self.winfo_width()

    def height(self) -> int:
        """ Returns FLUX tkinter window height """
        if self.fw_svc('tkinterAlive') is False:
            return self._window_min_size[1]
        return self.winfo_height()

    def min_size(self) -> tuple[int, int]:
        """ Returns FLUX tkinter window
        minimum size """
        return self._window_min_size

    def max_size(self) -> tuple[int, int]:
        """ Returns FLUX tkinter window
        maximum size """
        return self._window_max_size

    def display_width(self) -> int:
        """ Returns client display width """
        return self._client_system().GetSystemMetrics(0)

    def display_height(self) -> int:
        """ Returns client display height """
        return self._client_system().GetSystemMetrics(1)

    def coordinates(self) -> tuple[list, list, list, list]:
        """ Returns FLUX tkinter window
        4-corner coordinates """
        x1, y1 = (self.winfo_rootx(), self.winfo_rooty())
        y2, x3 = (y1+self.winfo_height(), x1+self.winfo_width())
        return [x1, y1], [x1, y2], [x3, y2], [x3, y1]

    def default_coordinates(self) -> tuple[int, int]:
        """ Returns default FLUX tkinter window
        spawn position (x, y) """
        return self.center_x_position(), self.center_y_position()

    def initial_coordinates(self) -> tuple[int, int]:
        """ Returns initial FLUX tkinter window
        spawn position (x, y) """
        return self._initial_x_pos, self._initial_y_pos

    def mouse_in_bounds(self, _set: bool = None) -> bool:
        """ Returns true if the mouse is in
        the FLUX tkinter window bounds """
        if _set is not None:
            self._mouse_in_bounds = bool(_set)
            return
        return self._mouse_in_bounds

    def has_focus(self, _set: bool = None) -> bool:
        """ Returns true if the FLUX tkinter
        window has focus """
        if _set is not None:
            self._is_active_window = bool(_set)
            return
        return self._is_active_window

    def is_visible(self) -> bool:
        """ Returns true if the FLUX tkinter
        window is visible """
        return self._window_visible

    def center_x_position(self) -> int:
        """ Returns FLUX tkinter window
        center x coordinate """
        return int((self.display_width()/2)-(self.width()/2))

    def center_y_position(self) -> int:
        """ Returns FLUX tkinter window
        center y coordinate """
        return int((self.display_height()/2)-(self.height()/2))

    def ref(self, key: str) -> any:
        """ Returns custom FLUX tkinter
        window class configuration """
        pass

    def managed_event(self, event: str) -> bool:
        """ Returns true if provided event
        is managed by FLUX tkinter window """
        for _bind in self._window_bindings:
            if _bind[0] == event:
                return True
        return False

    def place(self, child, **pack_args) -> None:
        """ Place child widget on FLUX
        tkinter window """
        self._window_widgets.append(child)
        child.pack(**pack_args)

    def new_bind(self, event: str, func) -> None:
        """ Bind event to FLUX tkinter window """
        for _event in event.split(' '):
            if not self.managed_event(_event):
                self.bind(_event, func)
            else:
                self.bind(_event, func, add='+')
            self._window_bindings.append((_event, func))

    def minimize(self) -> None:
        """ Minimize FLUX tkinter window """
        self.iconify()
        self._window_visible = False
        self.console(msg=f"Minimized '{self._identifier}' window")

    def maximize(self) -> None:
        """ Maximize FLUX tkinter window """
        self.state('zoomed')
        self._window_visible = True
        self.console(msg=f"Maximized '{self._identifier}' window")

    def take_focus(self) -> None:
        """ Give FLUX tkinter window focus """
        pass

    def hide(self) -> None:
        """ Hide FLUX tkinter window """
        self.withdraw()
        self._window_visible = False
        self.console(msg=f"Hid '{self._identifier}' window")

    def show(self, lift: bool = True) -> None:
        """ Show FLUX tkinter window """
        self.deiconify()
        if lift:
            self.lift()
        self._window_visible = True
        self.console(msg=f"'{self._identifier}' window visible")

    def close(self) -> None:
        """ Close FLUX tkinter window """
        self._window_visible = False
        self._is_active_window = False
        self._mouse_in_bounds = False
        self.destroy()
        self.console(msg=f"Closed '{self._identifier}' window")

    def console(self, msg: str, error: bool = False, **kwargs) -> None:
        """ Send text to the framework log """
        self.__framework.service(requestor=self.__type)['console'](msg=msg, error=error, **kwargs)

    def exception(self, cls, excinfo: tuple, **kwargs) -> None:
        """ Send an exception to the framework log """
        self.__framework.service(requestor=self.__type)['exception'](cls=cls, excinfo=excinfo, **kwargs)

    def process_proxy(self) -> dict:
        """ Returns the processes in the
        framework proxy """
        pass

    def framework(self) -> any:
        """ Returns the hosting framework instance """
        return self.__framework

    def window_class(self) -> type:
        """ Returns the FLUX tkinter type """
        return self.__type

    def fw_svc(self, svc: str, **kwargs) -> any:
        """ Execute the specified framework service """
        return self.__framework.service(requestor=self.__type)[svc](**kwargs)

    def fw_clearance(self) -> int:
        """ Returns the security clearance of
        the FLUX tkinter module """
        return self.fw_svc(svc='clvl', cls=self.__type)

    def to_service_injector(self, load: list[tuple]) -> None:
        """ Load injector with new services """
        for injectable in load:
            if type(injectable) is tuple:
                _call, _func, _clearance = injectable
                self._injectables.append({'call': _call, 'func': _func, 'clearance': _clearance})

    def inject_services(self) -> None:
        """ Inject loaded services into the framework """
        self.console(msg=f"Injecting {self.__type.__name__} services:")
        for _injectable in self._injectables:
            self.__framework.inject_service(
                call=_injectable.get('call'),
                cls=self.__type,
                func=_injectable.get('func'),
                clearance=_injectable.get('clearance')
            )
        self._injectables.clear()

    def extend_permissions(self, cls: type, **kwargs) -> None:
        """ Extend framework service permissions to dependant """
        self.console(msg=f"Extending permissions to {cls.__name__}...")
        self.fw_svc(
            svc='wcls',
            requestor=self.__type,
            cls=cls,
            admin=kwargs.get('admin', False),
            clearance=kwargs.get('clearance', SvcVars.LOW)
        )

    @staticmethod
    def _client_system() -> ctypes.WinDLL:
        """ Returns the client system WinDLL """
        return ctypes.windll.user32

    def _super_visibility_event(self, event: tk.Event) -> None:
        """ Handle FLUX tkinter module visibility event """
        self._window_visible = True
