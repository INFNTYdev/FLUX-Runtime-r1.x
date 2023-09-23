
"""
Base FLUX Runtime Framework Window View Module
"""


#   BUILT-IN IMPORTS
pass


#   EXTERNAL IMPORTS
from .fwvm import FwVm
from .utility import WindowPropertyManager, WindowEventHandler


#   MODULE CLASS
class FTkWindow(FwVm):
    def __init__(self, hfw, cls: type, uid: str, parent: any = None, **kwargs) -> None:
        """ Base framework window view """
        super().__init__(hfw=hfw, cls=cls, uid=uid, parent=parent, **kwargs)
        self.__properties: WindowPropertyManager = WindowPropertyManager(
            ftk=self,
            master=parent,
            **kwargs
        )
        self.__event: WindowEventHandler = WindowEventHandler(ftk=self)

    @staticmethod
    def view_type() -> str:
        return FTkWindow.__name__

    @property
    def properties(self) -> WindowPropertyManager:
        return self.__properties

    @property
    def event(self) -> WindowEventHandler:
        return self.__event

    def console(self, msg: str, error: bool = False, **kwargs) -> None:
        super().console(msg=f'( {self.fwm_name()}: {self.uid()} ) - {msg}', error=error, **kwargs)

    def hide(self) -> None:
        self.withdraw()
        self.event.update(visibility=False)
        self.console(msg=f"'{self.uid()}' window hidden")

    def show(self, lift: bool = True) -> None:
        self.deiconify()
        if lift is True:
            self.lift()
        self.event.update(visibility=True)
        self.console(msg=f"'{self.uid()}' window visible")

    def take_focus(self) -> None:
        self.focus_set()
