
""" Framework Standalone Service Module """


#   MODULE IMPORTS
from flxr.fwsvc import *


#   MODULE CLASSES
class FWService:
    def __init__(self, cls: type, func: any, clearance: int = ANY) -> None:
        """
        Framework standalone service object
        
        :param cls: The class in which the services function comes from
        :param func: The function in which the service executes
        :param clearance: The services security clearance
        """

        self.__clearance: int = int(clearance)
        self.__type: type = class_of(cls)
        self.__func = self.__finalize(func)

    def service_class(self) -> type:
        """ Returns the class of the service """
        return self.__type

    def execute(self, **fargs) -> any:
        """
        Execute the function of the service
        
        :param fargs: Arguments to provide the service function with
        :return: Function return value if any
        """
        return self.__func(**fargs)

    def clearance(self) -> int:
        """ Returns the security clearance of the service """
        return self.__clearance
    
    def __finalize(self, func: any) -> any:
        """ Finalize the intialization of the standalone service """
        if not callable(func):
            raise ValueError(
                f"Invalid service function parameter: {str(func)}"
            )
        return func
