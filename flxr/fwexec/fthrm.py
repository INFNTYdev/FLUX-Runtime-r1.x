
""" FLUX Runtime-Engine Thread Manager """


#   MODULE IMPORTS
from flxr import *


#   MODULE CLASSES
class FlxrThreadManager:
    def __init__(self, hfw: any, svc: any) -> None:
        """
        Framework thread manager
        
        :param hfw: Hosting framework
        :param svc: Hosting framework services
        """

        self.__hfw = fw_obj(hfw)
        self.__S = svc

        self.__threads: dict = {}
        self._inject_services()

    def threads(self) -> list:
        """ Returns the list of stored threads """
        return [handle for handle in self.__threads.keys()]
    
    def new(self, handle: str, thread: Thread, **kwargs) -> None:
        """ Establish new thread """
        if self._handle_exist(handle):
            return
        
        self.__threads[handle] = FWThread(
            handle=handle,
            thread=thread
        )
        self.__S(self)['console'](msg=f"Created '{handle}' thread")
        if kwargs.get('start', False):
            self.start(handle)

    def start(self, handle: str) -> None:
        """ Start a specified thread """
        if not self._handle_exist(handle):
            return
        
        if self._thread_running(handle):
            return
        
        self.__S(self)['console'](msg=f"Starting '{handle}' thread...")
        self.__threads[handle].start()

    def join(self, handle: str, force: bool = False, **kwargs) -> None:
        """ Join a specified thread with the main """
        if not self._handle_exist(handle):
            return
        
        if not self._thread_running(handle):
            return
        
        self.__S(self)['console'](msg=f"Closing '{handle}' thread...")
        self.__threads[handle].join(force=force, timeout=kwargs.get('timeout'))
        self.__S(self)['console'](msg=f"Successfully joined '{handle}' thread")
        self.delete(handle)
    
    def delete(self, handle: str) -> None:
        """ Delete a specified thread """
        if not self._handle_exist(handle):
            return
        
        if self._thread_running(handle):
            self.__S(self)['console'](msg=f"Cannot delete '{handle}' thread while running", error=True)
            return
        
        del self.__threads[handle]
        self.__S(self)['console'](msg=f"Successfully deleted '{handle}' thread")

    def join_all(self, force: bool = False) -> None:
        """ Join all threads with main """
        for _handle in self.__threads.keys():
            self.join(handle=_handle, force=force)

    def _handle_exist(self, handle: str) -> bool:
        """ Determines if a thread handle already exists """
        return handle in self.__threads.keys()
    
    def _thread_running(self, handle: str) -> bool:
        """ Determines if a stored thread is running """
        if not self._handle_exist(handle):
            return False
        
        return self.__threads[handle].running()

    def _inject_services(self) -> None:
        """ Inject the modules services """
        _injectables: list = [
            ('thrs', self.threads, MED),
            ('nthr', self.new, MED),
            ('sthr', self.start, MED),
            ('jthr', self.join, MED),
            ('dthr', self.delete, MED),
            ('thrr', self._thread_running, HIGH),
        ]
        for _new in _injectables:
            self.__S(self)['nsvc'](
                call=_new[0],
                cls=self,
                func=_new[1],
                clearance=_new[2]
            )
