
"""
FLUX Runtime Framework Tkinter Manager Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
pass


#   EXTERNAL IMPORTS
from flxr.common.core import DeployableFwm
from flxr.common.plugin.flxr_tkinter import FluxWindow
from flxr.constant import SvcVars


#   MODULE CLASS
class FlxrTkinterManager(DeployableFwm):
    def __init__(self, hfw, core: bool) -> None:
        """ Framework tkinter manager """
        super().__init__(hfw=hfw, cls=FlxrTkinterManager, core=core)
        self.__tkinter_alive: bool = False
        self.__windows: list[FluxWindow] = []
        self.extend_permissions(cls=FluxWindow, admin=True)
        self.load_injector(
            load=[
                ('windowIds', self.window_identifiers, SvcVars.MED),
                ('hostedWindows', self.managed_windows, SvcVars.HIGH),
                ('activeWindow', self.active_window, SvcVars.HIGH),
                ('mainWindow', self.main_window, SvcVars.HIGH),
                ('getWindow', self.get_window, SvcVars.HIGH),
                ('mainWinId', self.main_window_identifier, SvcVars.MED),
                ('activeWinId', self.active_window_identifier, SvcVars.MED),
                ('hostedWinCount', self.window_count, SvcVars.ANY),
                ('windowWidth', self.get_window_width, SvcVars.ANY),
                ('windowHeight', self.get_window_height, SvcVars.ANY),
                ('windowCoord', self.get_window_coordinates, SvcVars.LOW),
                ('createWindow', self.create_window, SvcVars.HIGH),
                ('addWindow', self.add_window, SvcVars.HIGH),
                # ('deleteWindow', self.delete_window, SvcVars.HIGH),
                # ('minimize', self.minimize_window, SvcVars.MED),
                # ('maximize', self.maximize_window, SvcVars.MED),
                # ('hideWindow', self.hide_window, SvcVars.HIGH),
                # ('hideAll', self.hide_all_windows, SvcVars.HIGH),
                # ('showWindow', self.show_window, SvcVars.HIGH),
                # ('showAll', self.show_all_windows, SvcVars.HIGH),
                # ('closeWindow', self.close_window, SvcVars.HIGH),
                # ('closeAll', self.close_all_windows, SvcVars.HIGH),
                ('startTkinter', self.start_tkinter, SvcVars.HIGH),
                ('stopTkinter', self.stop_tkinter, SvcVars.HIGH),
                ('tkinterAlive', self.tkinter_alive, SvcVars.ANY)
            ]
        )
        self.inject_services()

    def tkinter_alive(self) -> bool:
        """ Returns true if tkinter
        mainloop is open """
        return self.__tkinter_alive

    def window_identifiers(self) -> list[str]:
        """ Returns list of managed
        window identifiers """
        return [_window.identifier() for _window in self.__windows]

    def window_count(self) -> int:
        """ Returns number of
        managed windows """
        return len(self.window_identifiers())

    def has_windows(self) -> bool:
        """ Returns true if at least one managed
        window resides in FLUX tkinter manager """
        return self.window_count() > 0

    def existing_window(self, window: str) -> bool:
        """ Returns true if provided
        window identifier exists """
        return window in self.window_identifiers()

    def managed_windows(self) -> list[FluxWindow]:
        """ Returns list of managed
        window instances """
        return self.__windows

    def get_window(self, window: str) -> FluxWindow:
        """ Returns requested
        managed window instance """
        if not self.existing_window(window):
            return None
        for _window in self.managed_windows():
            if _window.identifier() == window:
                return _window

    def main_window(self) -> FluxWindow:
        """ Returns main managed
        window instance if any """
        for _window in self.managed_windows():
            if _window.properties.is_main():
                return _window
        return None

    def main_window_identifier(self) -> str:
        """ Returns main managed
        window identifier if any """
        if self.main_window() is not None:
            return self.main_window().identifier()
        return None

    def active_window(self) -> FluxWindow:
        """ Returns managed window
        instance holding focus """
        for _window in self.managed_windows():
            if _window.event.focus_in_bounds():
                return _window
        return None

    def active_window_identifier(self) -> str:
        """ Returns active managed
        window identifier if any """
        if self.active_window() is not None:
            return self.active_window().identifier()
        return None

    def get_window_width(self, window: str) -> int:
        """ Returns requested
        managed window width """
        if not self.existing_window(window):
            return None
        return self.get_window(window).properties.width()

    def get_window_height(self, window: str) -> int:
        """ Returns requested
        managed window height """
        if not self.existing_window(window):
            return None
        return self.get_window(window).properties.height()

    def get_window_coordinates(self, window: str) -> tuple[tuple, tuple, tuple, tuple]:
        """ Returns requested managed
        window 4-corner coordinates """
        if not self.existing_window(window):
            return None
        return self.get_window(window).properties.coordinates()

    def minimize_window(self, window: str) -> None:
        """ Minimize specified
        managed window instance """
        pass

    def maximize_window(self, window: str) -> None:
        """ Maximize specified
        managed window instance """
        pass

    def hide_window(self, window: str) -> None:
        """ Hide specified
        managed window instance """
        pass

    def show_window(self, window: str) -> None:
        """ Show specified
        managed window instance """
        pass

    def delete_window(self, window: str) -> None:
        """ Delete specified
        managed window instance """
        pass

    def close_window(self, window: str) -> None:
        """ Close specified
        managed window instance """
        pass

    def hide_all_windows(self, main: bool = True) -> None:
        """ Hide all managed window instances """
        pass

    def show_all_windows(self) -> None:
        """ Show all managed window instances """
        pass

    def close_all_windows(self, main: bool = True) -> None:
        """ Close all managed window instances """
        pass

    def set_main_window(self, window: str or type) -> None:
        """ Set specified window as main """
        pass

    def create_window(self, uid: str, **kwargs) -> None:
        """ Create new managed window instance """
        if self.existing_window(uid):
            return
        self.console(msg=f"Creating '{uid}' window...")
        self.__windows.append(
            kwargs.get('cls', FluxWindow)(
                hfw=self.framework(),
                cls=kwargs.pop('cls', FluxWindow),
                uid=uid,
                **kwargs
            )
        )
        self.console(msg=f"Successfully built '{uid}' window")

    def add_window(self, cls: type, main: bool = False) -> None:
        """ Add new managed window """
        self.console(msg=f"Initializing '{cls.__name__}' window...")
        self.extend_permissions(cls=cls, admin=True)
        self.__windows.append(cls(hfw=self.framework()))
        if main is True:
            self.__windows[-1].properties.set_as_main()
        self.console(msg=f"Successfully attached '{cls.__name__}' window")

    def start_tkinter(self) -> None:
        """ Start tkinter main loop """
        if self.tkinter_alive():
            return
        if not self.has_windows():
            self.console(msg="Cannot start FluxTkinter with no windows", notice=True)
            return

        if self.main_window() is None:
            self.console(msg=f"Forcing '{self.__windows[0].identifier()}' as main window...", notice=True)
            self.__windows[0].properties.set_as_main()
        self.console(msg="Starting tkinter mainloop...")
        try:
            self.__tkinter_alive = True
            self.main_window().mainloop()
            self.__tkinter_alive = False
        except Exception:
            self.__tkinter_alive = False
            self.console(msg="An error occurred during application runtime", error=True)
        self.console(msg="Application mainloop closed")

    def stop_tkinter(self, wait: int = 0) -> None:
        """ Stop tkinter main loop """
        if not self.tkinter_alive():
            return
        self.console(msg="Stopping application mainloop...", notice=True)
        self.close_all_windows(main=True)
