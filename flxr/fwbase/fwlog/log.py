
""" Framework Log Object """


#   MODULE IMPORTS
from flxr.fwbase.fwlog import *


class FrameworkLogger:
    def __init__(self, **kwargs) -> None:
        """ Framework log entry object """
        self._index: int = int(kwargs.get('index'))
        self._datetime: DateTime = kwargs.get('datetime')
        self._timeline: str = kwargs.get('timeline')
        self._type: str = kwargs.get('log_type').__name__
    
    def index(self) -> int:
        """ Returns the index of the log """
        return self._index
    
    def date(self) -> str:
        """ Returns the date of the log """
        return self._datetime.date()
    
    def time(self, hformat: int = 12) -> str:
        """
        Returns the time of the log
        
        :param hformat: Time format (12 or 24 hr)
        """
        return self._datetime.time(hformat=hformat)
    
    def log_datetime(self) -> DateTime:
        """ Returns the log datetime object """
        return self._datetime
    
    def timeline(self) -> str:
        """ Returns the log runtime plot """
        return self._timeline

    def log_type(self) -> str:
        """ Returns the log type """
        return self._type
