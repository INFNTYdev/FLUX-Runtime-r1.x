
"""
FLUX Tkinter Window Viewport Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
import tkinter as tk


#   EXTERNAL IMPORTS
from .interface_view import FluxView
from .viewf import FluxViewFrame


#   MODULE CLASS
class FluxViewPort(FluxView):
    def __init__(self, hfw, cls, master, identifier: str, **kwargs) -> None:
        """ FLUX interface viewport """
        super().__init__(
            hfw=hfw,
            cls=cls,
            master=master,
            identifier=identifier,
            **kwargs
        )
        self._viewframes: dict[FluxViewFrame] = {}
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

    def viewframe_count(self) -> int:
        """ Returns the number of hosted
        FLUX viewframes """
        return len(self._viewframes.keys())

    def has_viewframes(self) -> bool:
        """ Returns true if at least one FLUX
        viewframe resides in the viewport """
        return self.viewframe_count() > 0

    def viewframe_identifiers(self) -> list[str]:
        """ Returns list of hosted FLUX
        viewframe identifiers """
        return [_id for _id in self._viewframes.keys()]

    def existing_viewframe(self, identifier: str) -> bool:
        """ Returns true if hosted FLUX
        viewframe exists """
        return identifier in self.viewframe_identifiers()

    def hosted_viewframes(self) -> list[FluxViewFrame]:
        """ Returns list of FLUX
        viewframe instances """
        return [__viewframe for _, __viewframe in self._viewframes.items()]

    def active_viewframe(self) -> FluxViewFrame:
        """ Returns active hosted FLUX viewframe """
        for __viewframe in self.hosted_viewframes():
            if __viewframe.has_focus():
                return __viewframe
        return None

    def active_viewframe_type(self) -> type:
        """ Returns active hosted FLUX
        viewframe type """
        return self.active_viewframe().view_class()

    def active_viewframe_identifier(self) -> str:
        """ Returns active hosted FLUX
        viewframe identifier """
        return self.active_viewframe().identifier()

    def get_viewframe(self, identifier: str) -> FluxViewFrame:
        """ Returns hosted FLUX viewframe
        requested """
        if not self.existing_viewframe(identifier):
            return None
        return self._viewframes[identifier]

    def viewframe_width(self, identifier: str) -> int:
        """ Returns hosted FLUX viewframe width """
        return self.get_viewframe(identifier).width()

    def viewframe_height(self, identifier: str) -> int:
        """ Returns hosted FLUX viewframe height """
        return self.get_viewframe(identifier).height()

    def viewframe_coordinates(self, identifier: str) -> tuple[list, list, list, list]:
        """ Returns hosted FLUX viewframe
        4-corner coordinates """
        return self.get_viewframe(identifier).coordinates()

    def display_viewframe(self, identifier: str) -> None:
        """ Give the hosted FLUX viewframe
        requested focus """
        self.get_viewframe(identifier).take_focus()

    def delete_viewframe(self, identifier: str) -> None:
        """ Delete hosted FLUX viewframe instance """
        for _id, __viewframe in self._viewframes.items():
            __viewframe: FluxViewFrame
            if __viewframe.identifier() == identifier:
                del self._viewframes[identifier]
                return

    def populate(self, viewframes: list[tuple[str, type]]) -> None:
        """ Populate provided FLUX viewframe
        type(s) in viewport grid """
        for _VF in viewframes:
            try:
                _identifier, _type = _VF
                self.console(
                    msg=f"Initializing {_type.__name__} '{_identifier}'..."
                )
                self.extend_permissions(cls=_type, admin=True)
                self._viewframes[_identifier] = _type(
                    hfw=self.framework(),
                    cls=_type,
                    master=self,
                    identifier=_identifier
                )
                self._viewframes[_identifier].grid(column=0, row=0)
                self.console(
                    msg=f"{_type.__name__} '{_identifier}' initialization complete"
                )
            except Exception as UnexpectedFailure:
                self.console(
                    msg=f"Failed to initialize {_VF} in '{self.identifier()}' viewport",
                    error=True
                )
                self.console(msg=str(UnexpectedFailure), error=True)

    def place(self, view: tuple[str, type], **pack_args) -> None:
        """ Manually place provided FLUX view
        type in viewport """
        try:
            _identifier, _type = view
            self.console(
                msg=f"Initializing {_type.__name__} '{_identifier}'..."
            )
            self.extend_permissions(cls=_type, admin=True)
            self._viewframes[_identifier] = _type(
                hfw=self.framework(),
                cls=_type,
                master=self,
                identifier=_identifier
            )
            self._viewframes[_identifier].pack(**pack_args)
            self.console(
                msg=f"{_type.__name__} '{_identifier}' initialization complete"
            )
        except Exception as UnexpectedFailure:
            self.console(
                msg=f"Failed to initialize {view} in '{self.identifier()}' viewport",
                error=True
            )
            self.console(msg=str(UnexpectedFailure), error=True)
