
"""
FLUX Runtime-Framework Tkinter Window Dispatcher
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
import random


#   EXTERNAL IMPORTS
from flxr.fwlib.flxr_tkinter import *


#   MODULE CLASS
# noinspection PyStatementEffect
class TkinterWindowDispatcher:
    def __init__(self, hfw: any, svc: any) -> None:
        """ Tkinter window dispatcher """
        self.__hfw = fw_obj(hfw)
        self.__S = svc

        self.__window_host: FTkWindowDatabase = FTkWindowDatabase()

    def set_main(self, window: type) -> None:
        """ Set the main application window """
        if 'main' in self.__window_host.identifiers():
            return

        self.__S(self)['console'](msg=f"Setting {window.__name__} as main application window...")
        self.__S(self)['wcls'](requestor=self, cls=window, clearance=MED)
        try:
            self.__window_host.set_main(
                window=window(
                    hfw=self.__hfw,
                    svc=self.__S
                )
            )
        except TypeError as MissingFlxrArgs:
            self.__S(self)['console'](msg=f"'{window.__name__}' missing 'hfw' or 'svc' parameter", error=True)
            self.__S(self)['console'](msg=f"{MissingFlxrArgs}", error=True)

    def start(self) -> None:
        """ Start the main application loop """
        try:
            self.__window_host['main'].mainloop()
        except KeyboardInterrupt as SuddenExit:
            self.__S(self)['console'](msg="The application was interrupted", error=True)
            self.__S(self)['console'](msg=f"{SuddenExit}", error=True)
        except Exception as Unknown:
            self.__S(self)['console'](msg="An unknown exception occurred", error=True)
            self.__S(self)['console'](msg=f"{Unknown}", error=True)
        self.__S(self)['console'](msg="Main application loop closed")

    def windows(self) -> list[str]:
        """ Returns the list of stored window identifiers """
        return self.__window_host.identifiers()

    def size(self) -> int:
        """ Returns the number of stored windows """
        return len(self.__window_host)

    def new_window(self, **kwargs) -> FTkWindow:
        """ Dispatch new FLUX TkWindow instance """
        _window: FTkWindow = FTkWindow(
            fw=self.__hfw,
            svc=self.__S,
            root=None,
            identifier=self._issue_new_id(kwargs.get('borderless', False)),
            **kwargs
        )
        self.__window_host[_window]
        self.__S(self)['console'](msg=f"Dispatching '{_window.identifier()}' window...")
        return _window

    def close_window(self, identifier: str) -> None:
        """ Close a specified window by identifier """
        self.__window_host[identifier].close()

    def _issue_new_id(self, wm_status: bool) -> str:
        """ Returns a new FTkWindow instance identifier """
        def new_sequence() -> str:
            return str(random.randint(1010101, 9999999))

        _prefix: str = 'FMW-'
        if wm_status is True:
            _prefix: str = 'FUW-'

        _new_id: str = _prefix+new_sequence()
        while _new_id in self.__window_host.identifiers():
            _new_id = _prefix+new_sequence()
        return _new_id
