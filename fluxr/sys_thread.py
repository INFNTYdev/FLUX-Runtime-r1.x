
""" FLUX Runtime-Engine Framework Thread Manager """


#   MODULE IMPORTS
from fluxr import *


#   MODULE PACKAGE
__package__ = pkg_n()


#   MODULE CLASSES
class SystemThread:
    def __init__(self, handle: str, thread: Thread):
        """ Framework thread """
        self.__handle: str = handle
        self.__thread: Thread = thread
        self.__active: bool = False
        return

    def handle(self) -> str:
        """ Returns the threads handle """
        return self.__handle

    def set(self, status: bool):
        """ Set the activity state of the thread """
        self.__active = status
        return

    def start(self):
        """ Start thread """
        self.__thread.start()
        return

    def join(self, **kwargs):
        """ Join thread """
        self.__thread.join(**kwargs)
        return

    def is_active(self) -> bool:
        """ Determines if the thread is currently active """
        return self.__active

    def get_thread(self) -> Thread:
        """ Returns the core thread """
        return self.__thread


class SystemThreadManager:
    def __init__(self, fw: any, svc_c: any):
        """ Framework thread manager """
        self.__FW = fw_obj(fw)
        self.__S = svc_c

        self.__thread_host: dict = {}
        self.__inject_services()
        return

    def threads(self) -> list:
        """ Returns a list of stored thread handles """
        return [x for x in self.__thread_host.keys()]

    def thread_exist(self, handle: str) -> bool:
        """ Determines if a thread exist in the host """
        return bool(handle in list(self.__thread_host.keys()))

    def thread_active(self, handle: str) -> bool:
        """ Determines if a thread is currently running """
        if self.thread_exist(handle):
            return self.__thread_host[handle].is_active()
        return

    def new(self, handle: str, thread: Thread, **kwargs):
        """ Establish new thread in thread host """
        if not self.thread_exist(handle):
            try:
                self.__thread_host[handle] = SystemThread(
                    handle=handle,
                    thread=thread
                )
                if kwargs.get('start', False):
                    self.start(handle)
            except BaseException as Unknown:
                self.__exc(self, Unknown, sys.exc_info(), unaccounted=True,
                           pointer='new()')
                self.__out(f"An error occurred establishing '{handle}' thread", error=True)
        return

    def start(self, handle: str):
        """ Start requested thread """
        if (self.thread_exist(handle)) and (not self.thread_active(handle)):
            try:
                self.__out(f"Starting '{handle}' thread...")
                self.__thread_host[handle].start()
                self.__thread_host[handle].set(True)
            except BaseException as Unknown:
                self.__exc(self, Unknown, sys.exc_info(), unaccounted=True,
                           pointer='start()')
                self.__out(f"Failed to start '{handle}' thread", error=True)
        return

    def join(self, handle: str, **kwargs):
        """ Join requested thread with main thread """
        if (self.thread_exist(handle)) and (self.thread_active(handle)):
            try:
                self.__out(f"Joining '{handle}' thread to main...")
                self.__thread_host[handle].join(**kwargs)
                self.__thread_host[handle].set(False)
                self.__out(f"Successfully closed '{handle}' thread")
            except BaseException as Unknown:
                self.__exc(self, Unknown, sys.exc_info(), unaccounted=True,
                           pointer='join()')
                self.__out(f"Failed to join '{handle}' thread", error=True)
        return

    def delete(self, handle: str):
        """ Delete requested thread """
        if (self.thread_exist(handle)) and (not self.thread_active(handle)):
            try:
                del self.__thread_host[handle]
                self.__out(f"Successfully deleted '{handle}' thread")
            except BaseException as Unknown:
                self.__exc(self, Unknown, sys.exc_info(), unaccounted=True,
                           pointer='delete()')
                self.__out(f"An error occurred deleting '{handle}' thread", error=True)
        return

    def __inject_services(self):
        """ Add thread manager functions to service provider """
        self.__S(self)['nsvc']('threads', self, self.threads)
        self.__S(self)['nsvc']('nthread', self, self.new)
        self.__S(self)['nsvc']('sthread', self, self.start)
        self.__S(self)['nsvc']('jthread', self, self.join)
        self.__S(self)['nsvc']('dthread', self, self.delete)
        return

    def __out(self, text: str, **kwargs):
        """ Send text to the console """
        self.__S(self)['console'](text, **kwargs)
        return

    def __exc(self, cls: any, exc_o: any, exc_info: tuple, **kwargs):
        """ Handle system raised exceptions """
        self.__S(self)['exc'](cls, exc_o, exc_info, **kwargs)
        return
