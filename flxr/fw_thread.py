
""" Framework thread module """


# MODULE IMPORTS
from flxr import *

# MODULE PACKAGE
__package__ = pkg_n()


# MODULE CLASSES
class FwThread:
    def __init__(self, handle: str, thread: Thread):
        """ Framework thread """
        self._handle: str = handle
        self.__thread: Thread = thread
        self._running: bool = False

    def handle(self) -> str:
        """ Returns the threads unique handle """
        return self._handle

    def start(self):
        """ Start the thread """
        if not self._running:
            self.__thread.start()
            self._running = True

    def join(self, stop: bool = False, **kwargs):
        """ Join thread with main thread """
        if self._running:
            if stop:
                self.__thread.join(timeout=0)
            else:
                self.__thread.join(kwargs.get('timeout'))
            self._running = False

    def running(self) -> bool:
        """ Returns the thread run status """
        return self._running


class FlxrThreadManager:
    def __init__(self, fw: any, svc: any):
        """
        Runtime-Engine thread manager

        :param fw: Hosting framework
        :param svc: Framework service call
        """

        self.__FW = fw_obj(fw)
        self.__S = svc

        self.__thread_host: dict = {}
        self._inject_services()

    def threads(self) -> list:
        """ Returns a list of stored thread handles """
        return [handle for handle in self.__thread_host.keys()]

    def new(self, handle: str, thread: Thread, **kwargs):
        """ Establish new thread in thread host """
        if not self._thread_exists(handle):
            self.__thread_host[handle] = FwThread(
                handle=handle,
                thread=thread
            )
            self.__S(self)['console'](text=f"Created '{handle}' thread")
            if kwargs.get('start', False):
                self.start(handle)

    def start(self, handle: str):
        """ Start a hosted thread """
        if (self._thread_exists(handle)) and (not self._thread_running(handle)):
            self.__S(self)['console'](text=f"Starting '{handle}' thread...")
            self.__thread_host[handle].start()

    def join(self, handle: str, stop: bool = False, **kwargs):
        """ Join a hosted thread with main thread """
        if self._thread_exists(handle) and self._thread_running(handle):
            self.__S(self)['console'](text=f"Closing '{handle}' thread...")
            self.__thread_host[handle].join(
                stop=stop,
                timeout=kwargs.get('timeout')
            )
            self.__S(self)['console'](text=f"Successfully joined '{handle}' thread")

    def delete(self, handle: str):
        """ Delete a thread from the thread host """
        if (self._thread_exists(handle)) and (not self._thread_running(handle)):
            del self.__thread_host[handle]
            self.__S(self)['console'](text=f"Deleted '{handle}' thread")

    def _thread_exists(self, handle: str) -> bool:
        """ Determines if a thread exists in the host by handle """
        return handle in self.__thread_host.keys()

    def _thread_running(self, handle: str) -> bool:
        """ Determines if a hosted thread is running """
        if self._thread_exists(handle):
            return self.__thread_host[handle].running()

    def _inject_services(self):
        """ Inject threading services into service distrubutor """
        injectables: list = [
            ('thrs', self.threads, LOW),
            ('nthr', self.new, LOW),
            ('sthr', self.start, LOW),
            ('jthr', self.join, MED),
            ('dthr', self.delete, MED),
            ('thrr', self._thread_running, LOW)
        ]
        for new in injectables:
            self.__S(self)['nsvc'](
                call=new[0],
                cls=self,
                func=new[1],
                clearance=new[2]
            )
