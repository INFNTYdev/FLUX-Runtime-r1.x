
""" Framework exception log """


# MODULE IMPORTS
from flxr import *

# MODULE PACKAGE
__package__ = pkg_n()


# MODULE CLASSES
class ExceptionEntry:
    def __init__(self, **kwargs):
        """ Exception log entry """
        self._exception_runtime: str = None
        self._exception_index: int = kwargs.get('index')
        self._exception_date: str = kwargs.get('date')
        self._exception_time: str = kwargs.get('time')
        self._expected_encounter: bool = kwargs.get('known')
        self._exception_type: str = kwargs.get('type')
        self._exception_status: str = kwargs.get('status')
        self._exception_cause: str = kwargs.get('cause')
        self._exception_pointer: str = kwargs.get('pointer')
        self._author: str = kwargs.get('author')


class ExceptionLog:
    def __init__(self):
        """ Exception log """
        self.__log: list = []

    def log(self, _from: type, exc: Exception, excinfo: tuple, **kwargs):
        """ Log a system raised exception """
        self.__log.append(
            ExceptionEntry(
                index=len(self.__log),
                date=None,
                time=None,
                known=kwargs.get('known', True),
                type=str(exc.__class__.__name__),
                status=kwargs.get('status'),
                cause=(str(excinfo[1]) or None),
                pointer=kwargs.get('pointer'),
                author=str(_from.__class__.__name__)
            )
        )

    def get(self, index: int) -> ExceptionEntry:
        """ Retrieve an exception log by index """
        return self.__log[index]

    def get_last(self) -> ExceptionEntry:
        """ Retrieve the las submitted exception log """
        return self.__log[-1]


class ExceptionLogManager:
    def __init__(self, svc: any):
        """
        Framework exception log manager

        :param svc: Framework service call
        """

        self._svc: dict = svc
        self._exc_log: ExceptionLog = ExceptionLog()

    def exception(self, cls: type, exc: Exception, excinfo: tuple, **kwargs):
        """ Handle system raised exceptions """
        self._exc_log.log(
            _from=cls,
            exc=exc,
            excinfo=excinfo,
            known=kwargs.get('known'),
            pointer=kwargs.get('pointer'),
            status=kwargs.get('status')
        )
        self._svc['console'](f"EXCEPTION @ {cls.__class__.__name__}", error=True)
        self._svc['console'](f"{cls.__class__.__name__}.{kwargs.get('pointer', '#N/A')} "
                             f"- {excinfo[0].__name__}", error=True)
        self._svc['console'](f"{(exc or 'No cause provided')}", error=True)
