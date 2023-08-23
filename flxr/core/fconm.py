
"""
Framework Console Manager Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
pass


#   EXTERNAL IMPORTS
from .fwmod import FrameworkModule


#   MODULE CLASS
class FlxrConsoleManager(FrameworkModule):
    def __init__(self, hfw) -> None:
        """ Framework console manager """
        super().__init__(hfw=hfw, cls=FlxrConsoleManager)
        pass
