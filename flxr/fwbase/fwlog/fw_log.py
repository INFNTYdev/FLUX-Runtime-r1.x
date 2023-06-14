
""" Framework Console Log Entry """


#   MODULE IMPORTS
from flxr.fwbase.fwlog import *


#   MODULE CLASSES
class FWConsoleLogEntry(FrameworkLogger):

    _ERR_PREFIX: str = '[ ERROR ] : '
    __LINE: str = '{prefix} >  {date} {time} {divider}  {msg}'

    def __init__(self, **kwargs) -> None:
        """ Framework console log entry """
        super().__init__(
            index=kwargs.get('index'),
            datetime=kwargs.get('datetime'),
            timeline=kwargs.get('timeline'),
            log_type=FWConsoleLogEntry
        )
        self._is_error: bool = kwargs.get('error', False)
        self._print_config: dict = {
            'prefix': '',
            'divider': '|',
        }
        if kwargs.get('pconfig') is not None:
            self._print_config |= kwargs.get('pconfig')
        self._text: str = kwargs.get('msg')
    
    def error_msg(self) -> bool:
        """ Returns the console log error message status """
        return self._is_error
    
    def msg(self) -> str:
        """ Returns the console log message """
        return self._text

    def print_entry(self) -> None:
        """ Print the console log entry """
        if self._is_error:
            _local: str = f'{self._ERR_PREFIX}{self._text}'
        else:
            _local: str = self._text
        print(
            self.__LINE.format(
                prefix=self._print_config['prefix'],
                date=self.date(),
                time=self.time(),
                divider=self._print_config['divider'],
                msg=_local
            )
        )
