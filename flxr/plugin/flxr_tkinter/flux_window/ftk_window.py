
"""
FLUX Tkinter Window Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
import tkinter as tk


#   EXTERNAL IMPORTS
from simplydt import DateTime
from flxr.plugin.flxr_tkinter.flux_view import FluxViewPort
from .ftk import FluxTk
from .viewhost import FluxViewportHost


#   MODULE CLASS
class FluxWindow(FluxTk):

    __MAIN_LOCK: bool = False

    def __init__(self, hfw, cls, identifier: str, main: bool = False, **kwargs) -> None:
        """ FLUX runtime framework tkinter window """
        super().__init__(hfw=hfw, cls=cls, **kwargs)
        self._identifier: str = self._validate_identifier(identifier)
        self._is_main: bool = False
        if (main is True) and (not self.__MAIN_LOCK):
            self._set_as_main()
        self._current_width = self._current_height = 0
        self._current_x_pos = self._current_y_pos = 0
        self._size_last_updated: DateTime = None
        self._position_last_updated: DateTime = None
        self._size_recapture: bool = False
        self._position_recapture: bool = False
        self._MASTER_EVENT_BIND: dict = {
            '<Enter> <Leave>': self._master_hover_event,
            '<Button-1> <Button-3>': self._master_click_event,
            '<FocusIn> <FocusOut>': self._master_focus_event,
            '<Configure>': self._master_configure_event,
        }
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        for _events, _function in self._MASTER_EVENT_BIND.items():
            for _event in _events.split(' '):
                self.new_bind(_event, _function)
        self._viewport_host: FluxViewportHost = FluxViewportHost()

    def identifier(self) -> str:
        """ Returns window identifier """
        return self._identifier

    def is_main(self, force: bool = None) -> bool:
        """ Returns true if window is
        main window """
        if force is True:
            self._set_as_main()
        return self._is_main

    def viewport_count(self) -> int:
        """ Returns the number of hosted
        FLUX viewports """
        return self._viewport_host.viewport_count()

    def has_viewports(self) -> bool:
        """ Returns true if at least one
        FLUX viewport resides in the host """
        return self._viewport_host.has_viewports()

    def viewport_identifiers(self) -> list[str]:
        """ Returns list of hosted FLUX
        viewport identifiers """
        return self._viewport_host.identifiers()

    def existing_viewport(self, identifier: str) -> bool:
        """ Returns true if hosted FLUX
        viewport exists """
        return self._viewport_host.existing_viewport(identifier)

    def hosted_viewports(self) -> list[FluxViewPort]:
        """ Returns list of FLUX
        viewport instances """
        return self._viewport_host.hosted_viewports()

    def active_viewport(self) -> FluxViewPort:
        """ Returns active hosted FLUX viewport """
        return self._viewport_host.active_viewport()

    def active_viewport_type(self) -> type:
        """ Returns active hosted FLUX
        viewport type """
        return self._viewport_host.active_viewport_type()

    def active_viewport_identifier(self) -> str:
        """ Returns active hosted FLUX
        viewport identifier """
        return self._viewport_host.active_viewport_identifier()

    def get_viewport(self, identifier: str) -> FluxViewPort:
        """ Returns hosted FLUX viewport
        requested """
        return self._viewport_host.get_viewport(identifier)

    def viewport_width(self, identifier: str) -> int:
        """ Returns hosted FLUX viewport width """
        return self._viewport_host.viewport_width(identifier)

    def viewport_height(self, identifier: str) -> int:
        """ Returns hosted FLUX viewport height """
        return self._viewport_host.viewport_height(identifier)

    def viewport_coordinates(self, identifier: str) -> tuple[list, list, list, list]:
        """ Returns hosted FLUX viewport
        4-corner coordinates """
        return self._viewport_host.viewport_coordinates(identifier)

    def size_last_updated(self) -> tuple[int, int, int, int, int, int]:
        """ Returns time since window
        size was last updated """
        if self._size_last_updated is None:
            return None
        return self._size_last_updated.until(self._current_datetime())

    def position_last_updated(self) -> tuple[int, int, int, int, int, int]:
        """ Returns time since window
        position was last updated """
        if self._position_last_updated is None:
            return None
        return self._position_last_updated.until(self._current_datetime())

    def display_viewport(self, identifier: str) -> None:
        """ Give the hosted FLUX viewport
        requested focus """
        self._viewport_host.display_viewport(identifier)

    def delete_viewport(self, identifier: str) -> None:
        """ Delete hosted FLUX viewport instance """
        self._viewport_host.delete_viewport(identifier)

    def populate(self, viewports: list[tuple[str, type]]) -> None:
        """ Place provided FLUX viewport
        type(s) in window """
        for _VP in viewports:
            try:
                _identifier, _type = _VP
                self.console(
                    msg=f"Initializing [{_type.__name__} '{_identifier}'] in '{self.identifier()}' window:"
                )
                self.extend_permissions(cls=_type, admin=True)
                self._viewport_host[_identifier] = _type(
                    hfw=self.framework(),
                    cls=_type,
                    master=self,
                    identifier=_identifier
                )
                self._viewport_host[_identifier].grid(column=0, row=0, sticky=tk.NSEW)
                self.console(
                    msg=f"{_type.__name__} '{_identifier}' initialization complete"
                )
            except Exception as UnexpectedFailure:
                self.console(
                    msg=f"Failed to initialize {_VP} in '{self.identifier()}' window",
                    error=True
                )
                self.console(msg=str(UnexpectedFailure), error=True)

    def console(self, msg: str, error: bool = False, **kwargs) -> None:
        """ Send text to the framework log """
        super().console(msg=f"@{self.window_class().__name__} - {msg}", error=error, **kwargs)

    def _current_datetime(self) -> DateTime:
        """ Returns the current datetime """
        return self.fw_svc('getDatetime')

    def _validate_identifier(self, identifier) -> str:
        """ Evaluate and return the provided
        window identifier """
        if type(identifier) is not str:
            self._invalid_identifier(identifier)
        return identifier

    def _master_configure_event(self, event: tk.Event) -> None:
        """ Handle window configure event """
        self._capture_window_coordinates()
        self._capture_window_size()

    def _master_focus_event(self, event: tk.Event) -> None:
        """ Handle window focus event """
        if str(event).__contains__('FocusIn'):
            if not self.has_focus():
                self.has_focus(True)
                self.console(msg=f"'{self.identifier()}' gained focus")
        elif str(event).__contains__('FocusOut'):
            self.has_focus(False)
            self.console(msg=f"'{self.identifier()}' lost focus")

    def _master_hover_event(self, event: tk.Event) -> None:
        """ Handle window hover event """
        if str(event).__contains__('Enter'):
            self.mouse_in_bounds(True)
            if not self.has_focus():
                self.console(msg=f"Mouse in '{self.identifier()}' bounds")
        elif str(event).__contains__('Leave'):
            self.mouse_in_bounds(False)

    def _master_click_event(self, event: tk.Event) -> None:
        """ Handle window click event """
        pass

    def _capture_window_size(self) -> None:
        """ Record window current size """
        size: tuple = (self.winfo_width(), self.winfo_height())
        if not ((size[0] != self._current_width) or (size[1] != self._current_height)):
            return

        if self._size_last_updated is None:
            self._current_width = size[0]
            self._current_height = size[1]
        elif self.size_last_updated()[-1] > 0:
            self._current_width = size[0]
            self._current_height = size[1]
            self.console(
                msg=f"Captured '{self.identifier()}' window size @ [{self._current_width}x{self._current_height}]"
            )
            if self._size_recapture is True:
                self._size_recapture = False
        elif (self.size_last_updated()[-1] <= 1) and (self._size_recapture is False):
            self.console(msg=f"Scheduling '{self.identifier()}' size recapture...")
            self._size_recapture = True
            self.after(1500, self._capture_window_size)
            return
        self._size_last_updated = self._current_datetime()

    def _capture_window_coordinates(self) -> None:
        """ Record window current position """
        coord: tuple = self.coordinates()[0]
        if not ((coord[0] != self._current_x_pos) or (coord[1] != self._current_y_pos)):
            return

        if self._position_last_updated is None:
            self._current_x_pos = coord[0]
            self._current_y_pos = coord[1]
        elif self.position_last_updated()[-1] > 0:
            self._current_x_pos = coord[0]
            self._current_y_pos = coord[1]
            self.console(
                msg=f"Captured '{self.identifier()}' window coord @ "
                    f"[{self._current_x_pos}, {self._current_y_pos}]"
            )
            if self._position_recapture is True:
                self._position_recapture = False
        elif (self.position_last_updated()[-1] <= 1) and (self._position_recapture is False):
            self.console(msg=f"Scheduling '{self.identifier()}' coordinate recapture...")
            self._position_recapture = True
            self.after(1500, self._capture_window_coordinates)
            return
        self._position_last_updated = self._current_datetime()

    def _set_as_main(self) -> None:
        """ Set window as main window """
        self.console(msg=f"'{self._identifier}' set as main")
        self._is_main = True
        self.__MAIN_LOCK = True

    @staticmethod
    def _invalid_identifier(identifier) -> None:
        """ Raises value error on invalid
        window identifiers """
        raise ValueError(
            f"Invalid window identifier: {identifier}"
        )
