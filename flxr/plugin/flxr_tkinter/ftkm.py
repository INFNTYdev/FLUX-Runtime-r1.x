
"""
FLUX Runtime Framework Tkinter Manager Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
pass


#   EXTERNAL IMPORTS
from flxr.core.fwmod import FrameworkModule


#   MODULE CLASS
class FlxrTkinterManager(FrameworkModule):
    def __init__(self, hfw) -> None:
        """ Framework tkinter manager """
        super().__init__(hfw=hfw, cls=FlxrTkinterManager)
