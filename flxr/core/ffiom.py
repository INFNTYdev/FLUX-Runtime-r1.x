
"""
Framework File I/O Manager Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
pass


#   EXTERNAL IMPORTS
from .fwmod import FrameworkModule


#   MODULE CLASS
class FlxrFileIOManager(FrameworkModule):
    def __init__(self, hfw) -> None:
        """ Framework file I/O manager """
        super().__init__(hfw=hfw, cls=FlxrFileIOManager)
        pass
