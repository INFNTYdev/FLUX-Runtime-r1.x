
""" Tkinter Window Host """


#   MODULE IMPORTS
from fluxr.ftkinter import *

#   MODULE PACKAGE
__package__ = tkpkg_n()


#   MODULE CLASSES
class TkWindow(tk.Tk):
    def __init__(self, identifier: str, fw: any, svc_c: any, **kwargs):
        """ Create new Tk window instance """
        self.__p_identifier: str = identifier
        self.__FW = fw
        self.__S = svc_c

        # self.out(f"Initializing {identifier} window...")
        tk.Tk.__init__(self=self)
        if kwargs.get('windowless', False):
            self.geometry(kwargs.get('geometry'))
            self.wm_overrideredirect(True)
        else:
            self.minsize(kwargs.get('minsize'))
            self.maxsize(kwargs.get('maxsize'))
            self.geometry(kwargs.get('geometry', "900x450"))
            self.resizable(
                kwargs.get('h_resize', True),
                kwargs.get('v_resize', True)
            )
            self.title(kwargs.get('title', 'TkWindow'))
        self.pack_propagate(kwargs.get('propogate', True))
        self.grid_propagate(kwargs.get('propogate', True))
        self.configure(
            bg=kwargs.get('bg', '#e6e5df'),
            padx=kwargs.get('winpad', 0),
            pady=kwargs.get('winpad', 0)
        )
        return

    def invoke(self):
        """ Start the windows mainloop """
        try:
            self.mainloop()
        except Exception as Unknown:
            self.exc(self, Unknown, exc_info=sys.exc_info(), unaccounted=True,
                     pointer='invoke()')
            self.out(f"An error occurred with the '{self.__p_identifier}' window", error=True)
        finally:
            return

    def primary_identifier(self) -> str:
        """ Returns the windows primary identifier """
        return self.__p_identifier

    # FW SVC BOILER PLATE - Top Lvl
    def out(self, text: str, **kwargs):
        """ Send text to the console """
        self.__S(self)['console'](text, **kwargs)
        return

    def status(self, status: bool):
        """ Update the modules status """
        self.__S(self)['setstat'](self, status)
        return

    def date(self) -> str:
        """ Returns the current date """
        return self.__S(self)['date']()

    def time(self) -> str:
        """ Returns the current time """
        return self.__S(self)['time']()

    def runtime(self) -> str:
        """ Returns the current runtime """
        return self.__S(self)['rt']()

    def fw_stable(self) -> bool:
        """ Determines if required system modules are active """
        return self.__S(self)['corestat']()

    def fw_active(self) -> bool:
        """ Returns frameworks run status """
        return self.__S(self)['runstat']()

    def new_service(self, call: str, cls: any, func: any, **kwargs):
        """ Add a function reference to the service provider """
        self.__S(self)['nsvc'](call, cls, func, **kwargs)
        return

    def pause_console(self):
        """ Pause the console queue output """
        self.__S(self)['pauseConsole']()
        return

    def resume_console(self):
        """ Resume the console queue output """
        self.__S(self)['resumeConsole']()
        return

    def files(self) -> list:
        """ Returns the list of file names in the registry """
        return self.__S(self)['fileHost']()

    def get_file(self, fn: str) -> str:
        """ Returns the contents of the
        requested file from the file host """
        return self.__S(self)['getFile'](fn)

    def read_file(self, fp: str) -> str:
        """ Read the updated contents of a file """
        return self.__S(self)['readFile'](fp)

    def load_file(self, fp: str, **kwargs):
        """ Add a file to the file registry """
        self.__S(self)['loadFile'](fp, **kwargs)
        return

    def remove_file(self, fn: str):
        """ Remove a file from the registry """
        self.__S(self)['removeFile'](fn)
        return

    def threads(self) -> list:
        """ Returns a list of stored thread handles """
        return self.__S(self)['threads']()

    def new_thread(self, handle: str, thread: Thread, **kwargs):
        """ Establish new thread in thread host """
        self.__S(self)['nthread'](handle, thread, **kwargs)
        return

    def delete_thread(self, handle: str):
        """ Delete requested thread """
        self.__S(self)['dthread'](handle)
        return

    def exc(self, cls: any, exc_o: any, exc_info: tuple, **kwargs):
        """ Handle system raised exceptions """
        self.__S(self)['exc'](cls, exc_o, exc_info, **kwargs)
        return

    def exe(self, service: str, **kwargs) -> any:
        """ Execute a specified service call """
        return self.__S(self)[service](**kwargs)


class TkWindowHost:
    def __init__(self, fw: any, svc_c: any):
        """ FLUX Tkinter library framework """
        self.__FW = fw
        self.__S = svc_c

        self.__exe('wcls', requestor=self, cls=TkWindow, clearance='m')
        self.__window_host: dict = {}
        return

    def start_process(self):
        """ Start window host processes """
        self.__out("Activating TkWindowHost...")
        ...
        return

    def new_window(self, identifier: str, **kwargs) -> TkWindow:
        """ Create a new application window """
        window: TkWindow = TkWindow(
            identifier=identifier,
            fw=self.__FW,
            svc_c=self.__S,
            **kwargs
        )
        self.add_to_window_host(window)
        return self.__window_host[list(self.__window_host.keys())[-1]]['window']

    def add_to_window_host(self, window: TkWindow):
        """ Add a TkWindow to the window host """
        self.__window_host[window.primary_identifier()] = {
            'window': window,
        }
        return

    def invoke_window(self, window: TkWindow or str):
        """ | """
        if type(window) is TkWindow:
            pass
        elif type(window) is str:
            self.__window_host[window]['window'].invoke()
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
