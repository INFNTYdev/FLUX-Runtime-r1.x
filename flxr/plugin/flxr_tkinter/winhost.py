
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

    def has_windows(self) -> bool:
        """ Returns true if at least one FLUX
        tkinter window resides in host """
        return len(self.identifiers()) > 0

    def hosted_window_count(self) -> int:
        """ Returns number of hosted FLUX
        tkinter windows """
        return len(self.keys())

    def identifiers(self) -> list[str]:
        """ Returns the list of FLUX tkinter
        window identifiers """
        return [_id for _id in self.keys()]

    def hosted_windows(self) -> list[FluxWindow]:
        """ Returns the list of FLUX tkinter
        window instances """
        return [__window for _, __window in self.items()]

    def has_main_window(self) -> bool:
        """ Returns true if window host contains
        a main FLUX tkinter window """
        for _id, __window in self.items():
            __window: FluxWindow
            if __window.is_main():
                return True
        return False

    def main_window_type(self) -> type:
        """ Returns main hosted FLUX tkinter
        window type """
        for _id, __window in self.items():
            __window: FluxWindow
            if __window.is_main():
                return type(__window)
        return None

    def main_window(self) -> FluxWindow:
        """ Returns main hosted FLUX tkinter window """
        for _id, __window in self.items():
            __window: FluxWindow
            if __window.is_main():
                return __window
        return None

    def existing_window(self, identifier: str) -> bool:
        """ Returns true if hosted FLUX tkinter
        window exists """
        for _id, __window in self.items():
            __window: FluxWindow
            if identifier == __window.identifier():
                return True
        return False

    def get_window(self, identifier: str) -> FluxWindow:
        """ Returns hosted FLUX tkinter
        window requested """
        if not self.existing_window(identifier):
            return None
        return self[identifier]

    def get_active(self) -> FluxWindow:
        """ Returns active hosted FLUX
        tkinter window instance """
        for _id, __window in self.items():
            __window: FluxWindow
            if __window.has_focus():
                return __window
        return None

    def active_window_identifier(self) -> str:
        """ Returns active hosted FLUX
        tkinter window identifier """
        return self.get_active().identifier()

    def active_window_type(self) -> type:
        """ Returns active hosted FLUX
        tkinter window type """
        return self.get_active().window_class()

    def force_main(self) -> None:
        """ Force first hosted FLUX tkinter
        window as main """
        self[self.identifiers()[0]].is_main(force=True)

    def delete_window(self, identifier: str) -> None:
        """ Delete hosted FLUX tkinter window
        instance """
        pass
