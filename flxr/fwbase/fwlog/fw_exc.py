
""" Framework Exception Log Entry """


#   MODULE IMPORTS
from flxr.fwbase.fwlog import *


#   MODULE CLASSES
class FWExceptionLogEntry(FrameworkLogger):
    def __init__(self, **kwargs) -> None:
        """ Framework exception log entry """
        super().__init__(
            index=kwargs.get('index'),
            datetime=kwargs.get('datetime'),
            timeline=kwargs.get('timeline'),
            log_type=FWExceptionLogEntry
        )
        self._critical: bool = kwargs.get('critical')
        self._exception_type: type = kwargs.get('exc_type')
        self._exception_cause: str = kwargs.get('cause')
        self._exception_pointer: str = kwargs.get('pointer')
        self._exception_author: type = kwargs.get('author')
    
    def breaks_runtime(self) -> bool:
        """ Returns the log critical status """
        return self._critical
    
    def exception_type(self) -> type:
        """ Returns the log exception type """
        return self._exception_type
    
    def cause(self) -> str:
        """ Returns the cause of the exception log """
        return self._exception_cause
    
    def pointer(self) -> str:
        """ Returns the pointer of the exception log """
        return self._exception_pointer
    
    def author(self) -> type:
        """ Returns the author of the exception log """
        return self._exception_author
