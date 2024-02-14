
"""
FLUX Tkinter Window Viewport Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
pass


#   EXTERNAL IMPORTS
from flxr.plugin.flxr_tkinter.flux_view import FluxViewPort


#   MODULE CLASS
class FluxViewportHost(dict):
    def __init__(self) -> None:
        """ FLUX tkinter window viewport host """
        super().__init__()

    def viewport_count(self) -> int:
        """ Returns the number of hosted
        FLUX viewports """
        return len(self.keys())

    def has_viewports(self) -> bool:
        """ Returns true if at least one
        FLUX viewport resides in the host """
        return self.viewport_count() > 0

    def identifiers(self) -> list[str]:
        """ Returns list of hosted FLUX
        viewport identifiers """
        return [_id for _id in self.keys()]

    def existing_viewport(self, identifier: str) -> bool:
        """ Returns true if hosted FLUX
        viewport exists """
        return identifier in self.identifiers()

    def hosted_viewports(self) -> list[FluxViewPort]:
        """ Returns list of FLUX
        viewport instances """
        return [__viewport for _, __viewport in self.items()]

    def active_viewport(self) -> FluxViewPort:
        """ Returns active hosted FLUX viewport """
        for __viewport in self.hosted_viewports():
            if __viewport.has_focus():
                return __viewport
        return None

    def active_viewport_type(self) -> type:
        """ Returns active hosted FLUX
        viewport type """
        return self.active_viewport().view_class()

    def active_viewport_identifier(self) -> str:
        """ Returns active hosted FLUX
        viewport identifier """
        return self.active_viewport().identifier()

    def get_viewport(self, identifier: str) -> FluxViewPort:
        """ Returns hosted FLUX viewport
        requested """
        if not self.existing_viewport(identifier):
            return None
        return self[identifier]

    def viewport_width(self, identifier: str) -> int:
        """ Returns hosted FLUX viewport width """
        return self.get_viewport(identifier).width()

    def viewport_height(self, identifier: str) -> int:
        """ Returns hosted FLUX viewport height """
        return self.get_viewport(identifier).height()

    def viewport_coordinates(self, identifier: str) -> tuple[list, list, list, list]:
        """ Returns hosted FLUX viewport
        4-corner coordinates """
        return self.get_viewport(identifier).coordinates()

    def display_viewport(self, identifier: str) -> None:
        """ Give the hosted FLUX viewport
        requested focus """
        self.get_viewport(identifier).take_focus()

    def delete_viewport(self, identifier: str) -> None:
        """ Delete hosted FLUX viewport instance """
        for _id, __viewport in self.items():
            __viewport: FluxViewPort
            if __viewport.identifier() == identifier:
                del self[_id]
                return
