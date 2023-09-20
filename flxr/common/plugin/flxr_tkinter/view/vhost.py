
"""
FLUX Framework View Host Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
import tkinter as tk


#   EXTERNAL IMPORTS
from flxr.common import FwV


#   MODULE CLASS
class FwvHost(dict):
    def __init__(self, client: FwV) -> None:
        """ FLUX framework view host """
        super().__init__()
        self.__client_fwv: FwV = client
        self.__child_widgets: list = []
        self.__grid_configured: bool = False
        self.__pack_configured: bool = False

    def count(self) -> int:
        """ Returns number of hosted
        framework views """
        return len(self.keys())

    def has_views(self) -> bool:
        """ Returns true if at least one
        framework view resides in host """
        return self.count() > 0

    def identifiers(self) -> list[str]:
        """ Returns list of hosted
        framework view identifiers """
        return [_id for _id in self.keys()]

    def existing(self, view: str) -> bool:
        """ Returns true if provided framework
        view identifier exists in host """
        return view in self.identifiers()

    def hosted(self) -> list[FwV]:
        """ Returns list of hosted
        framework view instances """
        return [__view for _, __view in self.items()]

    def hosted_types(self) -> list[type]:
        """ Returns list of hosted
        framework view types """
        return [__view.fwm_class() for _, __view in self.hosted()]

    def has_main(self) -> bool:
        """ Returns true if a main
        framework view exists in host """
        for __view in self.hosted():
            if __view.properties.is_main():
                return True
        return False

    def main(self) -> FwV:
        """ Returns main framework
        view instance if any """
        for __view in self.hosted():
            if __view.properties.is_main():
                return __view
        return None

    def visible(self) -> list[FwV]:
        """ Returns list of visible
        framework view instances """
        __visible: list = []
        for __view in self.hosted():
            if __view.event.visible():
                __visible.append(__view)
        return __visible

    def active(self) -> FwV:
        """ Returns active framework
        view instance """
        for __view in self.hosted():
            if __view.event.focus_in_bounds():
                return __view
        return None

    def mouse_in(self) -> FwV:
        """ Returns framework view
        under mouse if any """
        for __view in self.hosted():
            if __view.event.mouse_in_bounds():
                return __view
        return None

    def get(self, view: str) -> FwV:
        """ Returns requested framework view """
        if not self.existing(view):
            return None
        return self[view]

    def place_child(self, child, **pack_args) -> None:
        """ Place child widgets
        in framework view (static) """
        if self.__grid_configured:
            self.__client_fwv.console(
                msg=f"Cannot manually place child in dynamic view",
                error=True
            )
            return
        if not self.__pack_configured:
            self.__pack_configured = True
            self.__client_fwv.properties.update_view_characteristic(dynamic=False)
        try:
            self.__child_widgets.append(child)
            child.pack(**pack_args)
        except Exception as UnexpectedFailure:
            self.__client_fwv.console(
                msg=f"Failed to place {child} in '{self.__client_fwv.identifier()}' view",
                error=True
            )
            self.__client_fwv.console(msg=UnexpectedFailure, error=True)

    def place_view(self, uid: str, view: type, **pack_args) -> None:
        """ Manually place views
        in framework view (static) """
        if self.__grid_configured:
            self.__client_fwv.console(
                msg=f"Cannot manually place '{uid}' in dynamic view",
                error=True
            )
            return
        if not self.__pack_configured:
            self.__pack_configured = True
            self.__client_fwv.properties.update_view_characteristic(dynamic=False)
        try:
            self.__client_fwv.console(
                msg=f"Initializing {view.__name__} '{uid}'..."
            )
            self.__client_fwv.extend_permissions(cls=view, admin=True)
            self[uid] = view(
                hfw=self.__client_fwv.hfw(),
                uid=uid,
                parent=self.__client_fwv
            )
            self[uid].pack(**pack_args)
            self.__client_fwv.console(
                msg=f"{view.__name__} '{uid}' initialization complete"
            )
        except Exception as UnexpectedFailure:
            self.__client_fwv.console(
                msg=f"Failed to manually place '{uid}' view",
                error=True
            )
            self.__client_fwv.console(msg=UnexpectedFailure, error=True)

    def __configure_view_grid(self) -> None:
        """ Configure client
        framework view grid """
        if not self.__grid_configured:
            self.__client_fwv.rowconfigure(0, weight=1)
            self.__client_fwv.columnconfigure(0, weight=1)
            self.__grid_configured = True
            self.__client_fwv.properties.update_view_characteristic(dynamic=True)

    def populate(self, views: list[tuple[str, type]]) -> None:
        """ Populate framework view
        with provided views (dynamic) """
        if self.__pack_configured:
            self.__client_fwv.console(
                msg="Cannot populate views in static view",
                error=True
            )
            return
        if not self.__grid_configured:
            self.__configure_view_grid()
        for _VF in views:
            try:
                _identifier, _type = _VF
                self.__client_fwv.console(
                    msg=f"Initializing {_type.__name__} '{_identifier}'..."
                )
                self.__client_fwv.extend_permissions(cls=_type, admin=True)
                self[_identifier] = _type(
                    hfw=self.__client_fwv.hfw(),
                    uid=_identifier,
                    parent=self.__client_fwv
                )
                self[_identifier].grid(column=0, row=0)
                self.__client_fwv.console(
                    msg=f"{_type.__name__} '{_identifier}' initialization complete"
                )
            except Exception as UnexpectedFailure:
                self.__client_fwv.console(
                    msg=f"Failed to initialize {_VF} in '{self.__client_fwv.identifier()}'",
                    error=True
                )
                self.__client_fwv.console(msg=str(UnexpectedFailure), error=True)

    def remove(self, view: str) -> None:
        """ Remove specified view from host """
        if not self.existing(view):
            return
        self[view].destroy()
        del self[view]
