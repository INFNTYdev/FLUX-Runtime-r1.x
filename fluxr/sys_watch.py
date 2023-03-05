
""" FLUX Runtime-Engine Framework Monitor """
import sys

#   MODULE IMPORTS
from fluxr import *


#   MODULE PACKAGE
__package__ = pkg_n()


#   MODULE CLASSES
class ModuleWrapper:
    def __init__(self, m_class: any, m: any):
        """ Framework monitor module wrapper """
        self.__class = m_class
        self.__class_o = m
        self.__class_n: str = m_class.__name__
        return

    def class_name(self) -> str:
        """ Returns the focused module class name """
        return self.__class_n

    def mod_class(self) -> any:
        """ Returns the focused module class """
        return self.__class


class SystemMonitor:
    def __init__(self, fw: any, svc_c: any):
        """ Framework monitor """
        self.__FW = fw_obj(fw)
        self.__S = svc_c

        self.__ref: dict = fw.bus_assetc(self)
        self.__assets: dict = self.__init_assets()
        self.__refresh: float = 0.3
        self.RUN: bool = False
        return

    def __init_assets(self) -> dict:
        """ Initialize module assets """
        __a: dict = {}
        for c in self.__ref:
            if c != type(self):
                __a[c.__name__] = ModuleWrapper(
                    m_class=c,
                    m=self.__ref[c]
                )
        return __a

    def start(self):
        """ Start system monitor """
        self.__new_thread(
            handle='sys-monitor',
            thread=Thread(target=self.__system_watch),
            start=True
        )
        return

    def stop(self):
        """ Stop system monitor """
        self.RUN = False
        return

    def __runnable(self) -> bool:
        """ Determines if the module
        has permission to execute """
        if self.RUN and self.__fw_active():
            return True
        else:
            return False

    def __system_watch(self):
        """ System monitor main loop """
        self.RUN = True
        self.__status(True)
        try:
            while self.__runnable():
                time.sleep(self.__refresh)
                self.__eval_assets()
        except BaseException as Unknown:
            self.__status(False)
            self.__exc(self, Unknown, sys.exc_info(), unaccounted=True,
                       pointer='__system_watch()')
            self.__out("An error occurred in the system monitor main loop", error=True)
        finally:
            self.__status(False)
            self.__out("System monitor stopped running")
            return

    def __eval_assets(self):
        """ Evaluate monitor assets """
        for cls in self.__assets.keys():
            if cls == 'FrameworkStatusManager':
                pass
            elif cls == 'FrameworkExceptionManager':
                pass
            elif cls == 'ServiceProvider':
                pass
            elif cls == 'SystemThreadManager':
                pass
            elif cls == 'SystemDatetimeManager':
                pass
            elif cls == 'SystemRuntimeClock':
                pass
            elif cls == 'SystemConsoleManager':
                pass
            elif cls == 'SystemFileIOManager':
                pass
            else:
                pass
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
        self.__S(self)['pauseConsole']()
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
