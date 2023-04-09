
""" Framework file I/O module """


# MODULE IMPORTS
from flxr import *

# MODULE PACKAGE
__package__ = pkg_n()


# MODULE CLASSES
class FlxrRuntimeMonitor:
    def __init__(self, fw: any, svc: any):
        """
        Runtime-engine file I/O manager

        :param fw: Hosting framework
        :param svc: Framework service call
        """

        self.__FW = fw_obj(fw)
        self.__S = svc
        self._handle: str = 'fw-monitor'

        self._refresh: float = 0.1
        self._run: bool = False

    def start_module(self):
        """ Start framework module """
        self.__S(self)['nthr'](
            handle=self._handle,
            thread=Thread(target=self.__system_watch),
            start=True
        )

    def stop_module(self, force: bool = None):
        """ Stop framework module """
        self._run = False
        self.__S(self)['jthr'](handle=self._handle, stop=force)

    def _runnable(self) -> bool:
        """ Determines if the module
        has permission to execute """
        if self._run:
            return True
        self._status(False)
        return False

    def __system_watch(self):
        """ System monitor main loop """
        self._run = True
        self._status(True)
        while self._runnable():
            time.sleep(self._refresh)
            pass

    def _status(self, status: bool):
        """ Set the modules status """
        self.__S(self)['sstat'](
            module=FlxrRuntimeMonitor,
            active=status
        )
