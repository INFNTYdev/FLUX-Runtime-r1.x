
"""
Framework Runtime Clock Module
"""


#   EXTERNAL IMPORTS
from flxr.common.core import DeployableFwm
from flxr.constant import SvcVars
from simplydt import simplydatetime, DateTime, Date, Time


#   MODULE CLASS
class FlxrRuntimeClock(DeployableFwm):
    def __init__(self, hfw, core: bool) -> None:
        """ Framework thread manager """
        super().__init__(hfw=hfw, cls=FlxrRuntimeClock, core=core)
        self.__origin: DateTime = simplydatetime.now()
        self.load_injector(
            load=[
                ('runtime', self.runtime_string, SvcVars.ANY),
                ('runtimeStamp', self.runtime_stamp, SvcVars.ANY),
                ('runtimeString', self.runtime_string, SvcVars.ANY),
                ('runtimeOrigin', self.runtime_origin, SvcVars.ANY),
                ('originDate', self.origin_date, SvcVars.ANY),
                ('originTime', self.origin_time, SvcVars.ANY),
            ]
        )
        self.inject_services()

    def runtime_origin(self) -> DateTime:
        """ Returns framework runtime
        clock origin datetime """
        return self.__origin

    def origin_date(self) -> Date:
        """ Returns framework runtime
        clock origin date """
        return self.runtime_origin().get_date()

    def origin_time(self) -> Time:
        """ Returns framework runtime
        clock origin time """
        return self.runtime_origin().get_time()

    def runtime(self) -> tuple[int, int, int, int, int, int]:
        """ Returns current framework runtime """
        return self.runtime_origin().until(simplydatetime.now())

    def runtime_stamp(self) -> str:
        """ Returns current
        framework runtime stamp """
        _rt: str = ''
        for index, _value in enumerate(self.runtime()[1:]):
            if index+1 != 5:
                _rt += f'{_value}:'
            else:
                _rt += f'{_value}'
        return _rt

    def runtime_string(self) -> str:
        """ Returns current
        framework runtime string """
        _rt: str = ''
        label: list = ['Months', 'Days', 'Hours', 'Minutes', 'Seconds']
        for index, _value in enumerate(self.runtime()[1:]):
            if index+1 != len(label):
                _rt += f'{_value} {label[index]}, '
            else:
                _rt += f'{_value} {label[index]}'
        return _rt
