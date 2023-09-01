
"""
FLUX Tkinter Window Host Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
pass


#   EXTERNAL IMPORTS
from .flux_window import FluxWindow


#   MODULE CLASS
class FluxWindowHost(dict):
    def __init__(self) -> None:
        """ FLUX tkinter window host """
        super().__init__()

    def identifiers(self) -> list[str]:
        """ Returns the list of FLUX tkinter
        window identifiers """
        return [_id for _id in self.keys()]

    def has_windows(self) -> bool:
        """ Returns true if at least one FLUX
        tkinter window resides in host """
        return len(self.identifiers()) > 0

    def has_main_window(self) -> bool:
        """ Returns true if window host contains
        a main FLUX tkinter window """
        for _id, __window in self.items():
            __window: FluxWindow
            if __window.is_main():
                return True
        return False

    def main_window_type(self) -> type:
        """ Returns the main hosted FLUX tkinter
        window type """
        for _id, __window in self.items():
            __window: FluxWindow
            if __window.is_main():
                return type(__window)
        return None

    def main_window(self) -> FluxWindow:
        """ Returns the main hosted FLUX tkinter
        window """
        for _id, __window in self.items():
            __window: FluxWindow
            if __window.is_main():
                return __window
        return None

    def force_main(self) -> None:
        """ Force first hosted FLUX tkinter
        window as main """
        self[self.identifiers()[0]].is_main(force=True)
