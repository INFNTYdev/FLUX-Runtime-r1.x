
"""
Framework File I/O Manager Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
import os


#   EXTERNAL IMPORTS
from flxr.common.core import ThreadedFwm
from flxr.constant import SvcVars
from flxr.model import FlxrFileRef


#   MODULE CLASS
class FlxrFileIOManager(ThreadedFwm):
    def __init__(self, hfw) -> None:
        """ Framework file I/O manager """
        super().__init__(hfw=hfw, cls=FlxrFileIOManager, handle='fwfileio')
        self.__pause: bool = False
        self.__references: dict[FlxrFileRef] = {}
        self.set_mainloop(func=None)
        self.set_poll(requestor=self, poll=1.3)
        self.to_service_injector(load=None)
        self.inject_services()

    pass
