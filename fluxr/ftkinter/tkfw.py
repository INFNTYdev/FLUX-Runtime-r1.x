
""" FLUX Tkinter Application Framework """


#   MODULE IMPORTS
from fluxr.ftkinter import *

#   MODULE PACKAGE
__package__ = tkpkg_n()


#   MODULE CLASSES
class TkinterLibFramework:

    __FW_MODULES: list = [
        [tkhost.TkWindowHost, True, 'tk-winhost']
    ]

    def __init__(self, fw: any, svc_c: any):
        """ FLUX Tkinter library framework """
        self.__FW = fw
        self.__S = svc_c

        self.__out(f"Preparring {tkpkg_n()} modules...")
        self.__asset_chain: dict = {}
        try:
            for _module in self.__FW_MODULES:
                try:
                    self.__out(f"Initializing {tkpkg_n()}.{str(_module[0].__name__)}...")
                    if str(_module[0].__name__).__contains__('TkWindowHost'):
                        self.__exe(service='wcls', requestor=self, cls=_module[0], admin=True)
                    else:
                        self.__exe(service='wcls', requestor=self, cls=_module[0], clearance='m')
                    self.__asset_chain[_module[0]] = _module[0](fw=fw, svc_c=svc_c)
                    if _module[1]:
                        try:
                            self.__out(f"Starting {str(_module[0].__name__)}...")
                            self.__new_thread(
                                handle=_module[2],
                                thread=Thread(
                                    target=self.__asset_chain[list(self.__asset_chain.keys())[-1]].start_process
                                ),
                                start=True
                            )
                            self.__out(f"{str(_module[0].__name__)} thread active")
                        except Exception as Unknown:
                            self.__status(False)
                            self.__exc(self, Unknown, exc_info=sys.exc_info(), unaccounted=True,
                                       pointer='__init__()')
                            self.__out(f"An error occurred starting {str(_module[0].__name__)} thread", error=True)
                            raise ReferenceError
                except Exception as Unknown:
                    self.__status(False)
                    self.__exc(self, Unknown, exc_info=sys.exc_info(), unaccounted=True,
                               pointer='__init__()')
                    self.__out(f"An error occurred initializing {str(_module[0].__name__)}", error=True)
                    raise AttributeError
        except Exception as Unknown:
            self.__status(False)
            self.__exc(self, Unknown, exc_info=sys.exc_info(), unaccounted=True,
                       pointer='__init__()')
            self.__out("An error occurred initializing the TkinterLibFramework", error=True)
        finally:
            return

    def new_window(self, identifier: str, **kwargs) -> TkWindow:
        """ Create a new application window """
        return self.__asset_chain[TkWindowHost].new_window(
            identifier=identifier,
            **kwargs
        )

    def add_window(self, window: TkWindow):
        """ Add a TkWindow to the window host """
        self.__asset_chain[TkWindowHost].add_to_window_host(
            window=window
        )
        return

    def invoke_window(self, window: TkWindow or str):
        """ | """
        self.__asset_chain[TkWindowHost].invoke_window(window)
        return

    # FRAMEWORK SERVICE BOILER PLATE - Top Lvl
    def __inject_services(self):
        """ Add class functions to service provider """
        pass

    def __out(self, text: str, **kwargs):
        """ Send text to the console """
        self.__S(self)['console'](text, **kwargs)
        return

    def __status(self, status: bool):
        """ Update the modules status """
        self.__S(self)['setstat'](self, status)
        return

    def __date(self) -> str:
        """ Returns the current date """
        return self.__S(self)['date']()

    def __time(self) -> str:
        """ Returns the current time """
        return self.__S(self)['time']()

    def __runtime(self) -> str:
        """ Returns the current runtime """
        return self.__S(self)['rt']()

    def __fw_stable(self) -> bool:
        """ Determines if required system modules are active """
        return self.__S(self)['corestat']()

    def __fw_active(self) -> bool:
        """ Returns frameworks run status """
        return self.__S(self)['runstat']()

    def __new_service(self, call: str, cls: any, func: any, **kwargs):
        """ Add a function reference to the service provider """
        self.__S(self)['nsvc'](call, cls, func, **kwargs)
        return

    def __pause_console(self):
        """ Pause the console queue output """
        self.__S(self)['pauseConsole']()
        return

    def __resume_console(self):
        """ Resume the console queue output """
        self.__S(self)['resumeConsole']()
        return

    def __files(self) -> list:
        """ Returns the list of file names in the registry """
        return self.__S(self)['fileHost']()

    def __get_file(self, fn: str) -> str:
        """ Returns the contents of the
        requested file from the file host """
        return self.__S(self)['getFile'](fn)

    def __read_file(self, fp: str) -> str:
        """ Read the updated contents of a file """
        return self.__S(self)['readFile'](fp)

    def __load_file(self, fp: str, **kwargs):
        """ Add a file to the file registry """
        self.__S(self)['loadFile'](fp, **kwargs)
        return

    def __remove_file(self, fn: str):
        """ Remove a file from the registry """
        self.__S(self)['removeFile'](fn)
        return

    def __threads(self) -> list:
        """ Returns a list of stored thread handles """
        return self.__S(self)['threads']()

    def __new_thread(self, handle: str, thread: Thread, **kwargs):
        """ Establish new thread in thread host """
        self.__S(self)['nthread'](handle, thread, **kwargs)
        return

    def __delete_thread(self, handle: str):
        """ Delete requested thread """
        self.__S(self)['dthread'](handle)
        return

    def __exc(self, cls: any, exc_o: any, exc_info: tuple, **kwargs):
        """ Handle system raised exceptions """
        self.__S(self)['exc'](cls, exc_o, exc_info, **kwargs)
        return

    def __exe(self, service: str, **kwargs) -> any:
        """ Execute a specified service call """
        return self.__S(self)[service](**kwargs)
