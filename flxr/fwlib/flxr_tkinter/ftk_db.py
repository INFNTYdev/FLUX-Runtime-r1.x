
"""
FLUX Runtime-Framework Tkinter Window Database
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
pass


#   EXTERNAL IMPORTS
from flxr.fwlib.flxr_tkinter import *


#   MODULE CLASS
class FTkWindowDatabase:
    def __init__(self) -> None:
        """ FLUX tkinter window database """
        self.__application_windows: dict = {}

    def identifiers(self) -> list:
        """ Returns the list of window identifiers """
        return [_x for _x in self.__application_windows.keys()]

    def set_main(self, window: tk.Tk) -> None:
        """ Set main application window """
        self.__application_windows['main'] = window

    def __getitem__(self, window: any) -> any:
        """ Retrieve or store an FTkWindow instance """
        if type(window) is FTkWindow:
            self.__application_windows[window.identifier()] = window
        elif type(window) is str:
            return self.__application_windows.get(window, None)
        else:
            raise ValueError(
                f'Invalid FTkWindowDatabase entry type: {type(window).__name__}'
            )

    def __len__(self):
        return len(self.__application_windows.keys())
