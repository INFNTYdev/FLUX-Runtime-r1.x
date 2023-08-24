
"""
Framework Service Manager Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
pass


#   EXTERNAL IMPORTS
from flxr.constant import SvcVars, GlobalFuncs
from flxr.utility import FlxrService
from .fwmod import FrameworkModule


#   MODULE CLASS
class FlxrServiceManager(FrameworkModule):

    __whitelist: dict = {}
    __admin: list = []

    def __init__(self, hfw) -> None:
        """ Framework service manager """
        super().__init__(hfw=hfw, cls=FlxrServiceManager)
        self.__services: dict = {}

    def calls(self) -> list[str]:
        """ Returns the list of all framework service calls """
        return [name for name in self.__services.keys()]

    def new(self, call: str, cls, func, **kwargs) -> None:
        """ Add new service to framework services """
        pass

    def remove(self, call: str) -> None:
        """ Remove specified service from framework services """
        pass

    def whitelist(self, requestor: type, cls, **kwargs) -> None:
        """ Add class to services whitelist group """
        pass

    def authorize(self, requestor: type, cls) -> None:
        """ Add class to services administration group """
        pass

    def override(self, requestor: type, call: str, using: type, func, **kwargs) -> None:
        """ Override an existing framework service with new """
        pass

    def serve(self, requestor: type) -> dict[FlxrService]:
        """ Returns appropriate framework services
        to requestor """
        pass

    def _existing_call(self, call: str) -> bool:
        """ Returns true if the provided call exist
        in the services """
        return call in self.__services.keys()

    def _whitelisted(self, requestor: type) -> bool:
        """ Returns true if the provided requestor
        is whitelisted """
        pass

    def _authorized(self, requestor: type) -> bool:
        """ Returns true if the provided requestor
         has administrative privilege """
        return GlobalFuncs.class_of(requestor) in self.__admin

    def _has_permission(self, requestor, svc: FlxrService) -> bool:
        """ Returns true if the provided requestor has
        permission to use the service """
        pass
