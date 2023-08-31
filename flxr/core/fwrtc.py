
"""
Framework Runtime Clock Module
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
class FlxrRuntimeClock(FrameworkModule):
    def __init__(self, hfw) -> None:
        """ Framework thread manager """
        super().__init__(hfw=hfw, cls=FlxrRuntimeClock)
        self.__origin: DateTime = simplydatetime.now()
        self.to_service_injector(
            load=[
                ('runtime', self.runtime_string, SvcVars.ANY),
                ('runtimeStamp', self.runtime_stamp, SvcVars.ANY),
                ('runtimeString', self.runtime_string, SvcVars.ANY),
                ('runtimeOrigin', self.runtime_origin, SvcVars.ANY),
                ('startDate', self.start_date, SvcVars.ANY),
                ('startTime', self.start_time, SvcVars.ANY)
            ]
        )
        self.inject_services()

    def runtime(self) -> tuple[int, int, int, int, int, int]:
        """ Returns the current framework runtime """
        return self.__origin.until(simplydatetime.now())

    def runtime_stamp(self) -> str:
        """ Returns the current framework runtime stamp """
        _rt: str = ''
        for index, _value in enumerate(self.runtime()[1:]):
            if index+1 != 5:
                _rt += f'{_value}:'
            else:
                _rt += f'{_value}'
        return _rt

    def runtime_string(self) -> str:
        """ Returns the current framework runtime string """
        _rt: str = ''
        label: list = ['Months', 'Days', 'Hours', 'Minutes', 'Seconds']
        for index, _value in enumerate(self.runtime()[1:]):
            if index+1 != len(label):
                _rt += f'{_value} {label[index]}, '
            else:
                _rt += f'{_value} {label[index]}'
        return _rt

    def runtime_origin(self) -> DateTime:
        """ Returns the framework runtime
        clock origin datetime """
        return self.__origin

    def start_date(self) -> Date:
        """ Returns the framework runtime
        clock origin date """
        return self.__origin.get_date()

    def start_time(self) -> Time:
        """ Returns the framework runtime
        clock origin time """
        return self.__origin.get_time()
