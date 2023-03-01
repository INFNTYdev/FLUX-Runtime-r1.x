
""" FLUX Runtime-Engine Framework File I/O Manager """


#   MODULE IMPORTS
from fluxr import *


#   MODULE PACKAGE
__package__ = pkg_n()


#   MODULE CLASSES
class RegistryFile:

    __EXT_DICT: dict = {
        'txt': 'Text Document',
        'py': 'Python File',
    }

    def __init__(self, fp: str, **kwargs):
        """ File registry file """
        self.__path: str = None
        self.__name: str = None
        self.__title: str = None
        self.__type: str = None
        self.__size: float = None
        self.__contents: str = None
        self.__last_modified = None
        self.__protected: bool = kwargs.get('protected', False)
        self.__eval_param(fp=fp, **kwargs)
        return

    def __eval_param(self, **kw):
        """ Evaluate object parameters """
        self.__path = os.path.abspath(kw.get('fp'))
        self.__name = os.path.basename(kw.get('fp'))
        self.__title = None
        self.__type = None
        self.__size = round(float(os.path.getsize(self.__path)/1024), 2)
        self.__last_modified = os.stat(self.__path)[stat.ST_MTIME]
        return

    def get_contents(self) -> str:
        """ Return the contents of the file """
        return self.__contents

    def update_contents(self, content: str, mode: str = 'overwrite' or 'append'):
        """ Update the contents of the file """
        opt: list = ['overwrite', 'append']
        if mode in opt:
            if mode == 'overwrite':
                self.__contents = content
            elif mode == 'append':
                self.__contents += content
        return

    def abs_path(self) -> str:
        """ Returns the absolute path of the file """
        return self.__path

    def name(self) -> str:
        """ Returns the name of the file """
        return self.__name

    def title(self) -> str:
        """ Returns the title of the file """
        return self.__title

    def type(self) -> str:
        """ Returns the type of file """
        return self.__type

    def extension(self) -> str:
        """ Returns the file extension """
        for x, n in self.__EXT_DICT:
            if n == self.type():
                return x
        return

    def size(self) -> float:
        """ Returns the file size in KB """
        return self.__size

    def last_modified(self) -> str:
        """ Returns the file last modified stamp """
        return str(self.__last_modified)

    def is_protected(self) -> bool:
        """ Determines if the file is protected """
        return self.__protected


class FileRegistry:
    def __init__(self, host: any):
        """ Framework file registry """
        self.__H = host

        self.__registry: dict = {}
        return

    def files(self) -> list:
        """ Returns the list of file names in the registry """
        return [x for x in self.__registry.keys()]

    def length(self) -> int:
        """ Returns the length of the file registry """
        return len(self.files())

    def file_exist(self, fn: str) -> bool:
        """ Determines if a file exist in the registry """
        return bool(fn in self.files())

    def read_file(self, file: RegistryFile or str) -> str:
        """ Get the updated contents of a file """
        __cont: str = ''
        try:
            if type(file) is RegistryFile:
                __cont = file.abs_path()
            else:
                __cont = file
            with open(__cont) as readable:
                __cont = readable.read()
                readable.close()
        except BaseException as Unknown:
            self.__H.d_call(self, 'exc', cls=self, exc_o=Unknown, exc_info=sys.exc_info(),
                            pointer='read_file()')
            if type(file) is RegistryFile:
                self.__H.d_call(self, 'console', text=f"Failed to read '{file.name()}'", error=True)
            else:
                self.__H.d_call(self, 'console', text=f"Failed to read '{file}'", error=True)
        finally:
            return __cont

    def load_file(self, fp: str, **kwargs):
        """ Add a file to the file registry """
        if os.path.exists(fp):
            file: RegistryFile = RegistryFile(
                fp=fp,
                **kwargs
            )
            file.update_contents(self.read_file(file), 'overwrite')
            self.__registry[file.name()] = file
        return

    def truncate_file(self, fn: str):
        """ Remove a file from the registry """
        if self.file_exist(fn):
            del self.__registry[fn]
        return


class SystemFileIOManager:
    def __init__(self, fw: any, svc_c: any):
        """ Framework file I/O manager """
        self.__FW = fw_obj(fw)
        self.__S = svc_c

        self.__file_host: FileRegistry = FileRegistry(self)
        self.__refresh: float = 2.2
        self.RUN: bool = False
        self.__inject_services()
        return

    def start(self):
        """ Start system file manager """
        self.__new_thread(
            handle='sys-io',
            thread=Thread(target=self.__file_io),
            start=True
        )
        return

    def stop(self):
        """ Stop system file manager """
        self.RUN = False
        return

    def d_call(self, requestor: any, call: any, **kwargs) -> any:
        """ Provide framework services to dependant object """
        if requestor is self.__file_host:
            return self.__S(self)[call](**kwargs)
        return

    def __runnable(self) -> bool:
        """ Determines if the module
        has permission to execute """
        if self.RUN and self.__fw_active():
            return True
        else:
            return False

    def __file_io(self):
        """ System file manager main loop """
        self.RUN = True
        self.__status(True)
        try:
            while self.__runnable():
                time.sleep(self.__refresh)
                self.__eval_registry()
        except BaseException as Unknown:
            self.__status(False)
            self.__exc(self, Unknown, sys.exc_info(), unaccounted=True,
                       pointer='__file_io()')
            self.__out("", error=True)
        finally:
            self.__status(False)
            self.__out("System file manager stopped")
            return

    def __eval_registry(self):
        """ Evaluate hosted files in the registry """
        return

    # FRAMEWORK SERVICE BOILER PLATE - lvl4
    def __inject_services(self):
        """ Add class functions to service provider """
        return

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
