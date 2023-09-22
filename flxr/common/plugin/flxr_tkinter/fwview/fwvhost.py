
"""
FLUX Runtime Framework Tkinter Manager Module
"""


#   EXTERNAL IMPORTS
from flxr.common.protocols import FwV


#   MODULE CLASS
class FwvHost(dict):
    def __init__(self, fwv: FwV) -> None:
        """ Framework view host """
        super().__init__()
        self.__fwv: FwV = fwv
        self.__widgets: list = []
        self.__grid_configured: bool = False
        self.__pack_configured: bool = False

    def count(self) -> int:
        """ Returns quantity of
        hosted framework views """
        return len(self.keys())

    def widget_count(self) -> int:
        """ Returns quantity of
        placed child widgets """
        return len(self.__widgets)

    def has_views(self) -> bool:
        """ Returns true if at least one
        framework view resides in host """
        return self.count() > 0

    def has_widgets(self) -> bool:
        """ Returns true if at least
        one widget resides in host """
        return self.widget_count() > 0

    def identifiers(self) -> list[str]:
        """ Returns list of hosted
        framework view identifiers """
        return [_id for _id in self.keys()]

    def existing(self, view: str) -> bool:
        """ Returns true if provided framework
        view unique identifier exists in host """
        return view in self.identifiers()

    def hosted(self) -> list[FwV]:
        """ Returns list of hosted
        framework view instances """
        return [__view for _, __view in self.items()]

    def widgets(self) -> list[any]:
        """ Returns list of child
        framework view widgets """
        return self.__widgets

    def hosted_classes(self) -> list[type]:
        """ Returns list of hosted
        framework view classes """
        return [__view.fwm_class() for __view in self.hosted()]

    def hosted_view_types(self) -> list[str]:
        """ Returns list of hosted
        framework view base types """
        return [__view.view_type() for __view in self.hosted()]

    def main(self) -> FwV:
        """ Returns main framework
        view instance if any """
        for _view in self.hosted():
            if _view.properties.is_main() is True:
                return _view
        return None

    def has_main(self) -> bool:
        """ Returns true if framework
        view has a main view """
        return self.main() is not None

    def visible(self) -> list[FwV]:
        """ Returns list of currently visible
        hosted framework view instances if any """
        _visible: list = []
        for _view in self.hosted():
            if _view.event.visible() is True:
                _visible.append(_view)
        return _visible

    def focus_in(self) -> FwV:
        """ Returns hosted framework view
        instance currently focused if any """
        for _view in self.hosted():
            if _view.event.focus_inbounds() is True:
                return _view
        return None

    def mouse_in(self) -> FwV:
        """ Returns hosted framework view
        instance currently under mouse if any """
        for _view in self.hosted():
            if _view.event.mouse_inbounds() is True:
                return _view
        return None

    def get(self, view: str) -> FwV:
        """ Returns requested hosted
        framework view instance """
        if not self.existing(view):
            return None
        return self[view]

    def place_widget(self, widget, **pack_args) -> None:
        """ Manually pack child widget
        on framework view (static) """
        if self.__grid_configured:
            self.__fwv.console(msg=f"Cannot manually place child in dynamic view", error=True)
            return
        if not self.__pack_configured:
            self.__pack_configured = True
            self.__fwv.properties.set_characteristic(dynamic=False)
        try:
            self.__widgets.append(widget)
            widget.pack(**pack_args)
        except Exception as UnexpectedFailure:
            self.__fwv.console(msg=f"Failed to place {widget} in '{self.__fwv.uid()}' view", error=True)
            self.__fwv.console(msg=UnexpectedFailure, error=True)

    def place_view(self, uid: str, view: type, **pack_args) -> None:
        """ Manually pack framework view
        on hosting framework view (static) """
        if self.__grid_configured:
            self.__fwv.console(msg=f"Cannot manually place '{uid}' in dynamic view", error=True)
            return
        if not self.__pack_configured:
            self.__pack_configured = True
            self.__fwv.properties.set_characteristic(dynamic=False)
        try:
            self.__fwv.console(msg=f"Initializing {view.__name__} '{uid}'...")
            self.__fwv.extend_permissions(cls=view, admin=True)
            self[uid] = view(
                hfw=self.__fwv.framework(),
                uid=uid,
                parent=self.__fwv
            )
            self[uid].pack(**pack_args)
            self.__fwv.console(msg=f"{view.__name__} '{uid}' initialization complete")
        except Exception as UnexpectedFailure:
            self.__fwv.console(msg=f"Failed to manually place '{uid}' view", error=True)
            self.__fwv.console(msg=UnexpectedFailure, error=True)

    def __configure_view_grid(self) -> None:
        """ Configure framework view grid """
        if self.__grid_configured or self.__pack_configured:
            return
        self.__fwv.rowconfigure(0, weight=1)
        self.__fwv.columnconfigure(0, weight=1)
        self.__grid_configured = True
        self.__fwv.properties.set_characteristic(dynamic=True)

    def populate(self, views: list[tuple[str, type]]) -> None:
        """ Populate provided framework views
        in hosting framework view (dynamic) """
        if self.__pack_configured:
            self.__fwv.console(msg="Cannot populate views in static view", error=True)
            return
        if not self.__grid_configured:
            self.__configure_view_grid()
        for _VF in views:
            try:
                _identifier, _type = _VF
                self.__fwv.console(msg=f"Initializing {_type.__name__} '{_identifier}'...")
                self.__fwv.extend_permissions(cls=_type, admin=True)
                self[_identifier] = _type(
                    hfw=self.__fwv.framework(),
                    uid=_identifier,
                    parent=self.__fwv
                )
                self[_identifier].grid(column=0, row=0)
                self.__fwv.console(msg=f"{_type.__name__} '{_identifier}' initialization complete")
            except Exception as UnexpectedFailure:
                self.__fwv.console(msg=f"Failed to initialize {_VF} in '{self.__fwv.uid()}'", error=True)
                self.__fwv.console(msg=str(UnexpectedFailure), error=True)

    def remove(self, view: str) -> None:
        """ Remove specified hosted framework
        view from host and display """
        if not self.existing(view):
            return
        self[view].destroy()
        del self[view]
