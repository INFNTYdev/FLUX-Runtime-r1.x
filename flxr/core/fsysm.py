
"""
Framework System Manager Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
pass


#   EXTERNAL IMPORTS
from flxr.common.core import ThreadedFwm
from flxr.core import FlxrConsoleManager


#   MODULE CLASS
class FlxrSystemManager(ThreadedFwm):
    def __init__(self, hfw) -> None:
        """ Framework system manager """
        super().__init__(hfw=hfw, cls=FlxrSystemManager, handle='fwmonitor')
        self.set_mainloop(func=None)
        self.set_poll(requestor=self, poll=0.5)
