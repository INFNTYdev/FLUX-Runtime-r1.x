
"""
FLUX Tkinter Window Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
import tkinter as tk


#   EXTERNAL IMPORTS
from simplydt import DateTime, Date, Time
from .ftk import FluxTk


#   MODULE CLASS
class FluxWindow(FluxTk):

    __MAIN_LOCK: bool = False

    def __init__(self, hfw, cls, identifier: str, main: bool = False, **kwargs) -> None:
        """ FLUX runtime framework tkinter window """
        super().__init__(hfw=hfw, cls=cls, **kwargs)
        self._identifier: str = self._evaluate_identifier(identifier)
        self._is_main: bool = False
        if (main is True) and (not self.__MAIN_LOCK):
            self._set_as_main()
        self._current_x_pos = self._current_y_pos = 0
        self._position_last_updated: DateTime = None
        self._position_recapture: bool = False
        self._MASTER_EVENT_BIND: dict = {
            '<Enter> <Leave>': self._master_hover_event,
            '<Button-1> <Button-3>': self._master_click_event,
            '<FocusIn> <FocusOut>': self._master_focus_event,
            '<Configure>': self._master_configure_event,
        }
        for _events, _function in self._MASTER_EVENT_BIND.items():
            for _event in _events.split(' '):
                self.new_bind(_event, _function)

    def identifier(self) -> str:
        """ Returns window identifier """
        return self._identifier

    def is_main(self, force: bool = None) -> bool:
        """ Returns true if window is
        main window """
        if force is True:
            self._set_as_main()
        return self._is_main

    def position_last_updated(self) -> tuple[int, int, int, int, int, int]:
        """ Returns time since window
        position was last updated """
        return self._position_last_updated.until(self._current_datetime())

    def console(self, msg: str, error: bool = False, **kwargs) -> None:
        """ Send text to the framework log """
        super().console(msg=f"@{self.window_class().__name__} - {msg}", error=error, **kwargs)

    def _current_datetime(self) -> DateTime:
        """ Returns the current datetime """
        return self.fw_svc('getDatetime')

    def _evaluate_identifier(self, identifier) -> str:
        """ Evaluate and return the provided
        window identifier """
        if type(identifier) is not str:
            self._invalid_identifier(identifier)
        return identifier

    def _master_configure_event(self, event: tk.Event) -> None:
        """ Handle window configure event """
        self._capture_window_coordinates()

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
                msg=f"Captured '{self.identifier()}' window @ [{self._current_x_pos}, {self._current_y_pos}]"
            )
            if self._position_recapture is True:
                self._position_recapture = False
        elif (self.position_last_updated()[-1] <= 1) and (self._position_recapture is False):
            self.console(msg=f"Scheduling '{self.identifier()}' coordinate recapture...")
            self._position_recapture = True
            self.after(1500, self._capture_window_coordinates)
            return
        self._position_last_updated = self._current_datetime()

    def _capture_x_coordinate(self, x: int) -> None:
        """ Record window current x coordinate """
        if x == self._current_x_pos:
            return

        if self._position_last_updated is None:
            self._current_x_pos = x
            self._position_last_updated = self._current_datetime()
            self.console(msg=f"Captured initial window x-coord: {x}")
        elif self._position_last_updated.until(self._current_datetime())[-1] <= 1:
            self.console(msg=f"Window x-coord changing: {x}")
        self.console(msg=f"'{self.identifier()}' x last updated: {self._position_last_updated.until(self._current_datetime())[-1]}")

    def _capture_y_coordinate(self, y: int) -> None:
        """ Record window current y coordinate """
        pass

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
