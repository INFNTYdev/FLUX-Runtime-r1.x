
"""
FLUX Runtime Framework Tkinter Manager Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
pass


#   EXTERNAL IMPORTS
from flxr.core.fwmod import FrameworkModule


#   MODULE CLASS
class FlxrTkinterManager(FrameworkModule):
    def __init__(self, hfw) -> None:
        """ Framework tkinter manager """
        super().__init__(hfw=hfw, cls=FlxrTkinterManager)

    def window_identifiers(self) -> list[str]:
        """ Returns the list of hosted FLUX
        tkinter window identifiers """
        pass

    def tkinter_windows(self) -> list[any]:
        """ Returns the list of hosted FLUX
        tkinter window instances """
        pass

    def active_window(self) -> any:
        """ Returns the active FLUX tkinter
        window instance """
        pass

    def main_window(self) -> any:
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
        pass

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

    def minimize_window(self, window) -> None:
        """ Minimize the hosted FLUX tkinter
        window provided """
        pass

    def maxamize_window(self, window) -> None:
        """ Maxamize the hosted FLUX tkinter
        window provided """
        pass

    def hide_window(self, window) -> None:
        """ Hide the hosted FLUX tkinter
        window provided """
        pass

    def hide_all_windows(self) -> None:
        """ Hide all hosted FLUX tkinter
        windows """
        pass

    def show_window(self, window, lift: bool = True) -> None:
        """ Show the hosted FLUX tkinter
        window provided """
        pass

    def show_all_windows(self) -> None:
        """ Show all hosted FLUX tkinter
        windows """
        pass

    def close_window(self, window) -> None:
        """ Close the hosted FLUX tkinter
        window provided """
        pass

    def close_all_windows(self, main: bool = True) -> None:
        """ Close all hosted FLUX tkinter
        windows """
        pass
