
""" FLUX tkinter window dispatcher """


# MODULE IMPORTS
from flxr.tklib import *

# MODULE PACKAGE
__package__ = tkpkg_n()


# MODULE CLASSES
class TkinterWindow(tk.Tk):
    def __init__(self, fw: any, svc: any, identifier: str, **kwargs):
        """
        FLUX tkinter window instance

        :param fw: Hosting framework
        :param svc: Framework service call
        :param identifier: Window unique identifier
        :param kwargs: Additional window configuration args
        """

        self.__FW = fw_obj(fw)
        self.__S = svc
        self._identifier: str = identifier

        tk.Tk.__init__(self)


class TkinterWindowDispatcher:
    def __init__(self, fw: any, svc: any):
        """
        FLUX tkinter library window dispatcher

        :param fw: Hosting framework
        :param svc: Framework service call
        """

        self.__FW = fw_obj(fw)
        self.__S = svc

        self.__window_host: dict = {}

    def new_window(self, identifier: str) -> TkinterWindow:
        """ Dispatch a new tkinter window """
        window: TkinterWindow = TkinterWindow(
            fw=self.__FW,
            svc=self.__S,
            identifier=identifier
        )
        self.__window_host[identifier] = window
        return window
