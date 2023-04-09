
""" FLUX Runtime-Engine Framework """


# MODULE IMPORTS
from flxr.tklib import *

# MODULE PACKAGE
__package__ = tkpkg_n()


# MODULE CLASSES
class FlxrTkinterLibrary:

    __LIB_MODULES: list = [
        (TkinterWindowDispatcher, MED),
        (tk.Tk, MED),
        (TkinterWindow, MED)
    ]

    def __init__(self, fw: any, svc: any):
        """
        FLUX Runtime-Engine tkinter library

        :param fw: Hosting framework
        :param svc: Framework service call
        """

        self.__FW = fw_obj(fw)
        self.__S = svc

        for __lib_mod in self.__LIB_MODULES:
            self.__S(self)['wcls'](
                requestor=self,
                cls=__lib_mod[0],
                clearance=__lib_mod[1]
            )

        self.__dispatcher: TkinterWindowDispatcher = TkinterWindowDispatcher(
            fw=fw,
            svc=svc
        )
        self._inject_services()

    def dispatch_new_window(self, identifier: str, **kwargs) -> TkinterWindow:
        """ Dispatch a new tkinter window """
        return self.__dispatcher.new_window(
            identifier=identifier,
            title=kwargs.get('title', identifier),
            borderless=kwargs.get('borderless'),
            width=kwargs.get('width'),
            height=kwargs.get('height'),
            bg=kwargs.get('bg', '#F2F7F9'),
        )

    def _inject_services(self):
        """ Inject datetime services into distributor """
        injectables: list = [
            ('TkWindow', TkinterWindowDispatcher, self.dispatch_new_window, LOW),
        ]
        for new in injectables:
            self.__S(self)['nsvc'](
                call=new[0],
                cls=new[1],
                func=new[2],
                clearance=new[3]
            )
