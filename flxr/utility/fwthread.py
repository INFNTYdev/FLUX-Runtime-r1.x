
"""
Framework Thread Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
from threading import Thread


#   EXTERNAL IMPORTS
from flxr.constant import ErrMsgs, SvcVars


#   MODULE CLASS
class FlxrThread:
    def __init__(self, handle: str, thread: Thread) -> None:
        """ Framework thread object """
        self._handle: str = self._verify_handle(handle)
        self.__thread: Thread = self._verify_thread(thread)
        self.__run: bool = False

    def handle(self) -> str:
        """ Returns the thread handle """
        return self._handle

    def thread(self) -> Thread:
        """ Returns the thread instance """
        return self.__thread

    def running(self) -> bool:
        """ Returns true if the thread is running """
        return self.__run

    def start(self) -> None:
        """ Start the framework thread """
        self.__thread.start()

    @staticmethod
    def _verify_handle(handle: str) -> str:
        """ Verify and return thread handle """
        if type(handle) is not str:
            raise ValueError(
                f"Invalid thread handle '{handle}'"
            )
        return handle

    @staticmethod
    def _verify_thread(thread: Thread) -> Thread:
        """ Verify and return thread instance """
        if type(thread) is not Thread:
            raise ValueError(
                f"Invalid thread instance: {thread}"
            )
        return thread
