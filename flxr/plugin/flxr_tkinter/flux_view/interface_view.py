
"""
FLUX Tkinter Window View Package
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
import tkinter as tk


#   EXTERNAL IMPORTS
pass


#   MODULE CLASS
class FluxView(tk.Frame):
    def __init__(self, hfw, cls, master, identifier: str, **kwargs) -> None:
        """ Base FLUX tkinter interface view """
        if hfw.is_rfw():
            self.__framework = hfw
            self.__type: type = cls
            self._identifier: str = self._validate_identifier(identifier)
            self._injectables: list = []
            self._parent = master
            self._view_visible: bool = False
            self._view_relative_width: float = 0.
            self._view_relative_height: float = 0.
            self._validate_relativity(
                w=kwargs.get('rel_width', 100),
                h=kwargs.get('rel_height', 100)
            )
            self._mouse_in_bounds: bool = False
            self._view_bindings: list[tuple] = []
            self._view_widgets: list = []
            self._VIEW_CONFIGURATION: dict = kwargs.get('config', {})

            super().__init__(
                master=master,
                width=self._calculate_relative_width(),
                height=self._calculate_relative_height(),
                padx=kwargs.get('padx', 0),
                pady=kwargs.get('pady', 0),
                highlightthickness=kwargs.get('border', 0),
                highlightbackground=kwargs.get('border_bg', 'black'),
                bg=kwargs.get('bg', 'gray'),
                cursor=kwargs.get('cursor', 'arrow'),
                relief=kwargs.get('relief', 'flat')
            )
            self.pack_propagate(kwargs.get('propagate', False))
            self.console(msg=f"Successfully built '{self._identifier}'")

    def identifier(self) -> str:
        """ Returns FLUX tkinter view identifier """
        return self._identifier

    def parent(self) -> any:
        """ Returns FLUX tkinter view
        parent widget """
        return self._parent

    def width(self) -> int:
        """ Returns FLUX tkinter view width """
        if self.fw_svc('tkinterAlive') is False:
            return self._calculate_relative_width()
        return self.winfo_width()

    def height(self) -> int:
        """ Returns FLUX tkinter view height """
        if self.fw_svc('tkinterAlive') is False:
            return self._calculate_relative_height()
        return self.winfo_height()

    def display_width(self) -> int:
        """ Returns client display width """
        return self.parent().display_width()

    def display_height(self) -> int:
        """ Returns client display height """
        return self.parent().display_height()

    def coordinates(self) -> tuple[list, list, list, list]:
        """ Returns FLUX tkinter view
        4-corner coordinates """
        x1, y1 = (self.winfo_rootx(), self.winfo_rooty())
        y2, x3 = (y1+self.winfo_height(), x1+self.winfo_width())
        return [x1, y1], [x1, y2], [x3, y2], [x3, y1]

    def mouse_in_bounds(self, _set: bool = None) -> bool:
        """ Returns true if the mouse is in
        the FLUX tkinter view bounds """
        pass

    def has_focus(self, _set: bool = None) -> bool:
        """ Returns true if the FLUX tkinter
        view has focus """
        pass

    def is_visible(self) -> bool:
        """ Returns true if the FLUX tkinter
        view is visible """
        pass

    def ref(self, key: str) -> any:
        """ Returns custom FLUX tkinter
        view class configuration """
        pass

    def managed_event(self, event: str) -> bool:
        """ Returns true if provided event
        is managed by FLUX tkinter view """
        pass

    def new_bind(self, event: str, func) -> None:
        """ Bind event to FLUX tkinter view """
        for _event in event.split(' '):
            if not self.managed_event(_event):
                self.bind(_event, func)
            else:
                self.bind(_event, func, add='+')
            self._view_bindings.append((_event, func))

    def take_focus(self) -> None:
        """ Give FLUX tkinter view focus """
        pass

    def console(self, msg: str, error: bool = False, **kwargs) -> None:
        """ Send text to the framework log """
        self.__framework.service(requestor=self.__type)['console'](
            msg=f"< @{self.view_class().__name__}: {self.identifier()} > - {msg}",
            error=error,
            **kwargs
        )

    def exception(self, cls, excinfo: tuple, **kwargs) -> None:
        """ Send an exception to the framework log """
        self.__framework.service(requestor=self.__type)['exception'](cls=cls, excinfo=excinfo, **kwargs)

    def process_proxy(self) -> dict:
        """ Returns the processes in the
        framework proxy """
        pass

    def framework(self) -> any:
        """ Returns hosting framework instance """
        return self.__framework

    def view_class(self) -> type:
        """ Returns FLUX tkinter view type """
        return self.__type

    def fw_svc(self, svc: str, **kwargs) -> any:
        """ Execute specified framework service """
        return self.__framework.service(requestor=self.__type)[svc](**kwargs)

    def fw_clearance(self) -> int:
        """ Returns security clearance of
        the FLUX tkinter view """
        return self.fw_svc(svc='clvl', cls=self.__type)

    def to_service_injector(self, load: list[tuple]) -> None:
        """ Load injector with new services """
        for injectable in load:
            if type(injectable) is tuple:
                _call, _func, _clearance = injectable
                self._injectables.append({'call': _call, 'func': _func, 'clearance': _clearance})

    def inject_services(self) -> None:
        """ Inject loaded services into the framework """
        self.console(msg=f"Injecting {self.__type.__name__} services:")
        for _injectable in self._injectables:
            self.__framework.inject_service(
                call=_injectable.get('call'),
                cls=self.__type,
                func=_injectable.get('func'),
                clearance=_injectable.get('clearance')
            )
        self._injectables.clear()

    def extend_permissions(self, cls: type, **kwargs) -> None:
        """ Extend framework service permissions to dependant """
        self.console(msg=f"Extending permissions to {cls.__name__}...")
        self.fw_svc(
            svc='wcls',
            requestor=self.__type,
            cls=cls,
            admin=kwargs.get('admin', False),
            clearance=kwargs.get('clearance', 1)
        )

    def _calculate_relative_width(self) -> int:
        """ Returns calculated FLUX tkinter
        view width """
        return int(self._parent.width()*self._view_relative_width)

    def _calculate_relative_height(self) -> int:
        """ Returns calculated FLUX tkinter
        view height """
        return int(self._parent.height()*self._view_relative_height)

    def _validate_identifier(self, identifier) -> str:
        """ Evaluate and return the provided
        FLUX tkinter view identifier """
        if type(identifier) is not str:
            self._invalid_identifier(identifier)
        return identifier

    def _validate_relativity(self, w: int, h: int) -> None:
        """ Evaluate and set FLUX tkinter view
        relative values """
        if w > 100 or w < 0:
            raise ValueError(
                f'Invalid relative width percentage: {w}%'
            )
        if h > 100 or h < 0:
            raise ValueError(
                f'Invalid relative height percentage: {h}%'
            )
        self._view_relative_width = float(w/100)
        self._view_relative_height = float(h/100)

    def _invalid_identifier(self, identifier) -> None:
        """ Raises value error on invalid
        FLUX tkinter view identifiers """
        raise ValueError(
            f"Invalid {self.__type.__name__} identifier: {identifier}"
        )
