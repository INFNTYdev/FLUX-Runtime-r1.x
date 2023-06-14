
""" Framework Thread Object """

#   MODULE IMPORTS
from flxr import *


#   MODULE CLASSES
class FWThread:
    def __init__(self, handle: str, thread: Thread) -> None:
        """ Framework thread object """
        self._handle: str = handle
        self.__thread: Thread = thread
        self.__run: bool = False
    
    def handle(self) -> str:
        """ Returns the thread handle """
        return self._handle
    
    def start(self) -> None:
        """ Start thread """
        if not self.__run:
            self.__thread.start()
            self.__run = True
    
    def join(self, force: bool = False, timeout: int = None) -> None:
        """ Join thread with main """
        if not self.__run:
            return
        
        if force is True:
            self.__thread.join(timeout=0)
        else:
            self.__thread.join(timeout=timeout)
        self.__run = False
    
    def running(self) -> bool:
        """ Returns the thread run status """
        return self.__run
