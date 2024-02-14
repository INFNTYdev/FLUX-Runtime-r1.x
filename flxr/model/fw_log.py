
"""
FLUX Runtime Framework Base Logging Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
pass


#   EXTERNAL IMPORTS
from simplydt import DateTime, Date, Time


#   MODULE CLASS
class FlxrLogger:
    def __init__(self, **args) -> None:
        """ Framework logging object """
        self._index: int = args.get('index')
        self._datetime: DateTime = args.get('datetime')
        self._runtime: str = args.get('timeline')
        self._type: type = args.get('type')

    def index(self) -> int:
        """ Returns the log index """
        return self._index

    def date(self) -> str:
        """ Returns the log record date """
        return self._datetime.date()

    def get_date(self) -> Date:
        """ Returns the log date object """
        return self._datetime.get_date()

    def time(self, hformat: int = 12) -> str:
        """ Returns the log record time """
        return self._datetime.time(hformat=hformat)

    def get_time(self) -> Time:
        """ Returns the log time object """
        return self._datetime.get_time()

    def datetime(self, hformat: int = 12) -> str:
        """ Returns the log record datetime """
        return self._datetime.date_time(hformat=hformat)

    def get_datetime(self) -> DateTime:
        """ Returns the log datetime object """
        return self._datetime
