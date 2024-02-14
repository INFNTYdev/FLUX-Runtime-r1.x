
"""
FLUX Tkinter Window Host Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
pass


#   EXTERNAL IMPORTS
from flxr.plugin.flxr_tkinter.flux_window import FluxWindow


#   MODULE CLASS
class FluxWindowHost(dict):
    def __init__(self) -> None:
        """ FLUX tkinter window host """
        super().__init__()

    def hosted_window_count(self) -> int:
        """ Returns number of hosted FLUX
        tkinter windows """
        return len(self.keys())

    def visible_window_count(self) -> int:
        """ Returns number of visible hosted
        FLUX tkinter window instances """
        return len([_id for _id, __win in self.items() if __win.is_visible()])

    def has_windows(self) -> bool:
        """ Returns true if at least one FLUX
        tkinter window resides in host """
        return self.hosted_window_count() > 0

    def identifiers(self) -> list[str]:
        """ Returns the list of FLUX tkinter
        window identifiers """
        return [_id for _id in self.keys()]

    def existing_window(self, identifier: str) -> bool:
        """ Returns true if hosted FLUX tkinter
        window exists """
        return identifier in self.identifiers()

    def hosted_windows(self) -> list[FluxWindow]:
        """ Returns the list of FLUX tkinter
        window instances """
        return [__window for _, __window in self.items()]

    def has_main_window(self) -> bool:
        """ Returns true if window host contains
        a main FLUX tkinter window """
        for __window in self.hosted_windows():
            if __window.is_main():
                return True
        return False

    def main_window(self) -> FluxWindow:
        """ Returns main hosted FLUX tkinter window """
        for __window in self.hosted_windows():
            if __window.is_main():
                return __window
        return None

    def main_window_type(self) -> type:
        """ Returns main hosted FLUX tkinter
        window type """
        return self.main_window().window_class()

    def main_window_identifier(self) -> str:
        """ Returns main hosted FLUX
        tkinter window identifier """
        return self.main_window().identifier()

    def active_window(self) -> FluxWindow:
        """ Returns active hosted FLUX tkinter window """
        for __window in self.hosted_windows():
            if __window.has_focus():
                return __window
        return None

    def active_window_type(self) -> type:
        """ Returns active hosted FLUX tkinter
        window type """
        return self.active_window().window_class()

    def active_window_identifier(self) -> str:
        """ Returns active hosted FLUX
        tkinter window identifier """
        return self.active_window().identifier()

    def get_window(self, identifier: str) -> FluxWindow:
        """ Returns hosted FLUX tkinter
        window requested """
        if not self.existing_window(identifier):
            return None
        return self[identifier]

    def window_width(self, identifier: str) -> int:
        """ Returns hosted FLUX tkinter window width """
        return self.get_window(identifier).width()

    def window_height(self, identifier: str) -> int:
        """ Returns hosted FLUX tkinter window height """
        return self.get_window(identifier).height()

    def window_coordinates(self, identifier: str) -> tuple[list, list, list, list]:
        """ Returns hosted FLUX tkinter window
        4-corner coordinates """
        return self.get_window(identifier).coordinates()

    def delete_window(self, identifier: str) -> None:
        """ Delete hosted FLUX tkinter window
        instance """
        for _id, __window in self.items():
            __window: FluxWindow
            if identifier == _id:
                if __window.is_visible():
                    __window.close()
                del self[identifier]
                return

    def minimize_window(self, identifier: str) -> None:
        """ Minimize hosted FLUX tkinter
        window provided """
        for _id, __window in self.items():
            __window: FluxWindow
            if identifier == _id:
                __window.minimize()
                return

    def maximize_window(self, identifier: str) -> None:
        """ Maximize hosted FLUX tkinter
        window provided """
        for _id, __window in self.items():
            __window: FluxWindow
            if identifier == _id:
                __window.maximize()
                return

    def hide_window(self, identifier: str) -> None:
        """ Hide hosted FLUX tkinter window
        provided """
        for _id, __window in self.items():
            __window: FluxWindow
            if identifier == _id:
                __window.hide()
                return

    def hide_all_windows(self, main: bool = True) -> None:
        """ Hide all hosted FLUX tkinter
        windows """
        for __window in self.hosted_windows():
            if (not main) and (not __window.is_main()):
                __window.hide()
            elif main is True:
                __window.hide()

    def show_window(self, identifier: str, lift: bool = True) -> None:
        """ Show hosted FLUX tkinter window
        provided """
        for _id, __window in self.items():
            __window: FluxWindow
            if identifier == _id:
                __window.show(lift=lift)
                return

    def show_all_windows(self) -> None:
        """ Show all hosted FLUX tkinter
        windows """
        for __window in self.hosted_windows():
            __window.show()

    def close_window(self, identifier: str) -> None:
        """ Close hosted FLUX tkinter window
        provided """
        for _id, __window in self.items():
            __window: FluxWindow
            if identifier == _id:
                __window.close()
                return

    def close_all_windows(self, main: bool = True) -> None:
        """ Close all hosted FLUX tkinter
        windows """
        for __window in self.hosted_windows():
            if (not main) and (not __window.is_main()):
                __window.close()
            elif main is True:
                __window.close()

    def set_main(self, identifier: str) -> None:
        """ Force first hosted FLUX tkinter
        window as main """
        self.get_window(identifier).is_main(force=True)

    def force_main(self) -> None:
        """ Force first hosted FLUX tkinter
        window as main """
        self[self.identifiers()[0]].is_main(force=True)
