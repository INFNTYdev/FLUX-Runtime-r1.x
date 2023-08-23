
"""
Framework Process Proxy Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
from multiprocessing import Process


#   EXTERNAL IMPORTS
from flxr.constant import ErrMsgs


#   MODULE CLASS
class ProcessProxy:
    def __init__(self) -> None:
        """ Framework process proxy """
        self.__proxy: dict = {}

    def append_process(self, process) -> None:
        """ Add an external process to proxy """
        if (type(process) is tuple) and (len(process) == 2):
            _name, __process = process
            if (issubclass(type(__process), Process)) and (type(_name) is str):
                self.__proxy[_name] = __process
                return
        self._invalid_process_arg(process)

    @staticmethod
    def _invalid_process_arg(process_arg) -> None:
        """ Raises value error on invalid process arg """
        raise ValueError(
            ErrMsgs.ERRM_F_001.format(process_arg=process_arg)
        )
