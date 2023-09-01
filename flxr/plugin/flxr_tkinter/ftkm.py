
"""
FLUX Runtime Framework Tkinter Manager Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
pass


#   EXTERNAL IMPORTS
from flxr.constant import SvcVars
from flxr.core.fwmod import FrameworkModule
from .flux_window import FluxWindow
from .winhost import FluxWindowHost


#   MODULE CLASS
class FlxrTkinterManager(FrameworkModule):
    def __init__(self, hfw) -> None:
        """ Framework tkinter manager """
        super().__init__(hfw=hfw, cls=FlxrTkinterManager)
        self._mainloop_open: bool = False
        self._window_host: FluxWindowHost = FluxWindowHost()
        self.console(msg="Tkinter window host ready")
        self.extend_permissions(cls=FluxWindow, admin=True)
        self.to_service_injector(
            load=[
                ('windowIds', self.window_identifiers, SvcVars.MED),
                ('getWindows', self.tkinter_windows, SvcVars.HIGH),
                ('activeWindow', self.active_window, SvcVars.HIGH),
                ('getMainWindow', self.main_window, SvcVars.HIGH),
                ('activeWinId', self.active_window_identifier, SvcVars.MED),
                ('mainWinId', self.main_window_identifier, SvcVars.MED),
                ('activeWinType', self.active_window_type, SvcVars.ANY),
                ('mainWinType', self.main_window_type, SvcVars.ANY),
                ('hostedWinCount', self.window_quantity, SvcVars.ANY),
                ('liveWindowCount', self.dispatched_window_quantity, SvcVars.ANY),
                ('windowWidth', self.window_width, SvcVars.ANY),
                ('windowHeight', self.window_height, SvcVars.ANY),
                ('windowCoord', self.window_coordinates, SvcVars.LOW),
                ('createWindow', self.create_window, SvcVars.HIGH),
                ('deleteWindow', self.delete_window, SvcVars.HIGH),
                ('minimize', self.minimize_window, SvcVars.MED),
                ('maxamize', self.maxamize_window, SvcVars.MED),
                ('hideWindow', self.hide_window, SvcVars.HIGH),
                ('hideAll', self.hide_all_windows, SvcVars.HIGH),
                ('showWindow', self.show_window, SvcVars.HIGH),
                ('showAll', self.show_all_windows, SvcVars.HIGH),
                ('closeWindow', self.close_window, SvcVars.HIGH),
                ('closeAll', self.close_all_windows, SvcVars.HIGH),
                ('startTkinter', self.start_module, SvcVars.HIGH),
                ('tkinterAlive', self.mainloop_alive, SvcVars.ANY)
            ]
        )
        self.inject_services()

    def mainloop_alive(self) -> bool:
        """ Returns true if the tkinter
        mainloop is running """
        return self._mainloop_open

    def window_identifiers(self) -> list[str]:
        """ Returns the list of hosted FLUX
        tkinter window identifiers """
        return self._window_host.identifiers()

    def tkinter_windows(self) -> list[FluxWindow]:
        """ Returns the list of hosted FLUX
        tkinter window instances """
        pass

    def active_window(self) -> FluxWindow:
        """ Returns the active FLUX tkinter
        window instance """
        pass

    def main_window(self) -> FluxWindow:
        """ Returns the main FLUX tkinter
        window instance """
        pass

    def active_window_identifier(self) -> str:
        """ Returns the active FLUX tkinter
        window identifier """
        pass

    def main_window_identifier(self) -> str:
        """ Returns the main FLUX tkinter
        window identifier """
        pass

    def active_window_type(self) -> type:
        """ Returns the active FLUX tkinter
        window type """
        pass

    def main_window_type(self) -> type:
        """ Returns the main FLUX tkinter
        window type """
        return self._window_host.main_window_type()

    def window_quantity(self) -> int:
        """ Returns the number of hosted FLUX
        tkinter windows """
        pass

    def dispatched_window_quantity(self) -> int:
        """ Returns the number of hosted FLUX
         tkinter windows displaying on screen"""
        pass

    def window_width(self, window) -> int:
        """ Returns the width of the hosted FLUX
         tkinter window provided """
        pass

    def window_height(self, window) -> int:
        """ Returns the height of the hosted FLUX
         tkinter window provided """
        pass

    def window_coordinates(self, window) -> tuple[list, list, list, list]:
        """ Returns the coordinates of the hosted
        FLUX tkinter window provided """
        pass

    def create_window(self, identifier: str, **kwargs) -> FluxWindow:
        """ Create new FLUX tkinter window instance """
        if self._existing_identifier(identifier):
            return

        self.console(msg=f"Creating '{identifier}' window...")
        self._window_host[identifier] = FluxWindow(
            hfw=self.framework(),
            cls=FluxWindow,
            identifier=identifier,
            **kwargs
        )

    def delete_window(self, window) -> None:
        """ Remove FLUX tkinter window from
        window host """
        pass

    def start_module(self) -> None:
        """ Start tkinter main loop """
        if self._mainloop_open:
            return
        if not self._window_host.has_windows():
            self.console(msg=f"Cannot start FluxTkinter with no windows", notice=True)
            return

        self._mainloop_open = True
        if not self._window_host.has_main_window():
            self._window_host.force_main()
            self.console(msg=f"Forced '{self.main_window_type().__name__}' as main window")
        self.console(msg="Starting application mainloop...")
        self._window_host.main_window().mainloop()
        self.console(msg="Application mainloop closed")

    def minimize_window(self, window) -> None:
        """ Minimize hosted FLUX tkinter
        window provided """
        pass

    def maxamize_window(self, window) -> None:
        """ Maxamize hosted FLUX tkinter
        window provided """
        pass

    def hide_window(self, window) -> None:
        """ Hide hosted FLUX tkinter window
        provided """
        pass

    def hide_all_windows(self) -> None:
        """ Hide all hosted FLUX tkinter
        windows """
        pass

    def show_window(self, window, lift: bool = True) -> None:
        """ Show hosted FLUX tkinter window
        provided """
        pass

    def show_all_windows(self) -> None:
        """ Show all hosted FLUX tkinter
        windows """
        pass

    def close_window(self, window) -> None:
        """ Close hosted FLUX tkinter window
        provided """
        pass

    def close_all_windows(self, main: bool = True) -> None:
        """ Close all hosted FLUX tkinter
        windows """
        pass

    def _existing_identifier(self, identifier: str) -> bool:
        """ Returns true if identifier exists
        in window host """
        return identifier in self._window_host.identifiers()
