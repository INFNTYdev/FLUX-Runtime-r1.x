
"""
FLUX Runtime-Framework Tkinter Manager
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
pass


#   EXTERNAL IMPORTS
from flxr.fwlib.flxr_tkinter import *


#   MODULE CLASS
class FlxrTkinterManager:
    def __init__(self, hfw: any, svc: any) -> None:
        """
        FLUX tkinter library manager

        :param hfw: Hosting framework
        :param svc: Hosting framework services
        """
        self.__hfw = fw_obj(hfw)
        self.__S = svc
        self.__root: tk.Tk = None

        self.__S(self)['wcls'](requestor=self, cls=FTkWindow, clearance=MED)
        self.__S(self)['acls'](requestor=self, cls=TkinterWindowDispatcher)

        self.__dispatcher: TkinterWindowDispatcher = TkinterWindowDispatcher(hfw, svc)
        self._inject_services()

    def set_main(self, window: type) -> None:
        """ Set the root application window """
        if (issubclass(window, tk.Tk)) and (self.__root is None):
            self.__root = window
            self.__dispatcher.set_main(window)

    def start_main(self) -> None:
        """ Start the main application window """
        self.__dispatcher.start()

    def windows(self) -> list[str]:
        """ Returns the list of stored window identifiers """
        return self.__dispatcher.windows()

    def new_window(self, **kwargs) -> FTkWindow:
        """ Dispatch new FLUX TkWindow instance """
        return self.__dispatcher.new_window(**kwargs)

    def close_window(self, identifier: str) -> None:
        """ Close a specified window by identifier """
        self.__dispatcher.close_window(identifier)

    def _inject_services(self) -> None:
        """ Inject the modules services """
        _injectables: list = [
            ('windows', self.windows, LOW),
            ('newWindow', self.new_window, LOW),
            ('closeWindow', self.close_window, MED),
        ]
        for _new in _injectables:
            self.__S(self)['nsvc'](
                call=_new[0],
                cls=self,
                func=_new[1],
                clearance=_new[2]
            )
