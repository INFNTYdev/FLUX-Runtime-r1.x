
"""
Framework Datetime Manager Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
pass


#   EXTERNAL IMPORTS
from flxr.constant import SvcVars
from simplydt import simplydatetime, DateTime, Date, Time
from .fwmod import FrameworkModule


#   MODULE CLASS
class FlxrDatetimeManager(FrameworkModule):
    def __init__(self, hfw) -> None:
        """ Framework datetime manager """
        super().__init__(hfw=hfw, cls=FlxrDatetimeManager)
        self.to_service_injector(
            load=[
                ('date', self.current_date, SvcVars.ANY),
                ('time', self.current_time, SvcVars.ANY),
                ('datetime', self.current_datetime, SvcVars.ANY),
                ('getDate', self.get_date, SvcVars.ANY),
                ('getTime', self.get_time, SvcVars.ANY),
                ('getDatetime', self.datetime, SvcVars.ANY),
            ]
        )
        self.inject_services()

    def current_date(self) -> str:
        """ Returns the current date """
        return self.datetime().date()

    def get_date(self) -> Date:
        """ Returns the current date object """
        return self.datetime().get_date()

    def current_time(self, hformat: int = 12) -> str:
        """ Returns the current time """
        return self.datetime().time(hformat=hformat)

    def get_time(self) -> Time:
        """ Returns the current time object """
        return self.datetime().get_time()

    def current_datetime(self, hformat: int = 12) -> str:
        """ Returns the current datetime """
        return self.datetime().date_time(hformat=hformat)

    @staticmethod
    def datetime() -> DateTime:
        """ Returns the current datetime object """
        return simplydatetime.now()
