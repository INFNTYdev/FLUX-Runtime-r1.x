
"""
Console Log Entry Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
pass


#   EXTERNAL IMPORTS
from flxr.constant import ConsoleVars
from .fw_log import FlxrLogger


#   MODULE CLASS
class ConsoleEntry(FlxrLogger):
    def __init__(self, index, datetime, timeline, **print_config) -> None:
        """ Framework console log entry """
        super().__init__(
            index=index,
            datetime=datetime,
            timeline=timeline,
            type=ConsoleEntry
        )
        self._printed: bool = False
        self._print_config: dict = print_config

    def print_entry(self) -> str:
        """ Print the console log string """
        if self._printed:
            return

        _message: str = ''
        if self._print_config.get('error') is True:
            _message += ConsoleVars.ERROR_PREFIX
            self._print_config['prefix'] = '!'
        elif self._print_config.get('warning') is True:
            _message += ConsoleVars.WARNING_PREFIX
        elif self._print_config.get('notice') is True:
            _message += ConsoleVars.NOTICE_PREFIX
        _message += self._print_config['message']

        if self._print_config.get('skip') is True:
            self._print_config['prefix'] = f"\n{self._print_config['prefix']}"

        _pointer: str = '>'
        if self._print_config.get('pointer') is False:
            _pointer = ' '

        _date: str = ''
        if self._print_config.get('show_date') is False:
            _date = ' '*10
        else:
            _date = self.date()

        _time: str = ''
        if self._print_config.get('show_time') is False:
            _time = ' '*11
        else:
            _time = self.time()

        print(
            ConsoleVars.PRINT_LINE.format(
                prefix=self._print_config.get('prefix'),
                pointer=_pointer,
                date=_date,
                time=_time,
                divider=self._print_config.get('seperator'),
                message=f"{_message}{self._print_config.get('suffix')}"
            )
        )
        self._printed = True

    def released(self) -> bool:
        """ Returns true if the console log
        was printed to the console """
        return self._printed
