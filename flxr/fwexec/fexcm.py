
""" FLUX Runtime-Engine Exception Manager """


#   MODULE IMPORTS
from flxr import *


#   MODULE CLASSES
class FlxrExceptionManager:
    def __init__(self, hfw: any, svc: any) -> None:
        """
        Framework exception manager
        
        :param hfw: The hosting framework
        :param svc: Hosting framework base services
        """

        self.__hfw = fw_obj(hfw)
        self.__S = svc
        self._exception_log: list = []
        self.__index: int = 0
    
    def exception(self, _from: type, excinfo: tuple, **kwargs) -> None:
        """
        Handles framework exceptions
        
        :param _from: The class in which the exception was raised
        :param excinfo: The exception data tuple
        :param kwargs: Additional args such as critical status and exception pointer
        """
        self._log_exception(
            author=_from,
            exc_type=excinfo[0],
            cause=str(excinfo[1]),
            critical=kwargs.get('critical', False),
            pointer=kwargs.get('pointer')
        )
        self.__S['console'](msg=f"EXCEPTION @ {class_of(_from).__name__}", error=True)
        self.__S['console'](
            msg=f"{class_of(_from).__name__}.{kwargs.get('pointer', '#N/A')} - {excinfo[0].__name__}",
            error=True
        )
        self.__S['console'](msg=f"{str(excinfo[1])}", error=True)
        self._handle_exception()

    def _log_exception(self, **kwargs) -> None:
        """ Log exception """
        self._exception_log.append(
            FWExceptionLogEntry(
                index=self.__index,
                datetime=simplydatetime.now(),
                timeline=None,
                critical=kwargs.get('critical', False),
                exc_type=kwargs.get('exc_type'),
                cause=kwargs.get('cause'),
                pointer=kwargs.get('pointer'),
                author=kwargs.get('author')
            )
        )

    def _handle_exception(self) -> None:
        """ Handle exception """
        self.__index += 1
