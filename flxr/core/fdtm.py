
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
        self._run: bool = False
        self._refresh: float = 0.2
        self.__datetime: DateTime = simplydatetime.now()
        self.to_service_injector(
            load=[
                ('date', self.current_date, SvcVars.ANY),
                ('time', self.current_time, SvcVars.ANY),
                ('datetime', self.current_datetime, SvcVars.ANY),
                ('getDate', self.get_date, SvcVars.ANY),
                ('getTime', self.get_time, SvcVars.ANY),
                ('getDatetime', self.get_datetime, SvcVars.ANY),
            ]
        )
        self.inject_services()

    def current_date(self) -> str:
        """ Returns the current date """
        return self.__datetime.date()

    def get_date(self) -> Date:
        """ Returns the current date object """
        return self.__datetime.get_date()

    def current_time(self, hformat: int = 12) -> str:
        """ Returns the current time """
        return self.__datetime.time(hformat=hformat)

    def get_time(self) -> Time:
        """ Returns the current time object """
        return self.__datetime.get_time()

    def current_datetime(self, hformat: int = 12) -> str:
        """ Returns the current datetime """
        return self.__datetime.date_time(hformat=hformat)

    def get_datetime(self) -> DateTime:
        """ Returns the current datetime object """
        return self.__datetime

    def _runnable(self) -> bool:
        """ Returns true if the framework
        module has clearance to run """
        if not self._run:
            return False
        if not self.framework().is_alive():
            return False
        if not self.fw_svc(svc='getstat', module=FlxrDatetimeManager):
            return False
        return True

    def _mainloop(self) -> None:
        """ Datetime manager main loop """
        self._run = True
        self.set_status(True)
        while self._runnable():
            self.wait(self._refresh)
            self._update()

    def _update(self) -> None:
        """ Update the datetime manager module """
        self.__datetime = simplydatetime.now()
