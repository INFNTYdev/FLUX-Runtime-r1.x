
"""
Framework Standalone Service Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
pass


#   EXTERNAL IMPORTS
from flxr.constant import ErrMsgs, SvcVars


#   MODULE CLASS
class FlxrService:
    def __init__(self, cls: type, func, clearance: int = SvcVars.ANY) -> None:
        """ Framework standalone service """
        self.__clearance: int = clearance
        self.__type: type = cls
        self.__func = self.__finalize(func)

    def service_class(self) -> type:
        """ Returns the service originating class """
        return self.__type

    def clearance(self) -> int:
        """ Returns the security clearance of the service """
        return self.__clearance

    def execute(self, **fargs) -> any:
        """ Execute the service function """
        return self.__func(**fargs)

    @staticmethod
    def __finalize(func) -> any:
        """ Finalize the service initialization """
        if not callable(func):
            raise ValueError(ErrMsgs.ERRM_F_003.format(func=str(func)))
        return func
