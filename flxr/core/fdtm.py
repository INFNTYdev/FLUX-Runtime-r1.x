
"""
Framework Datetime Manager Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
pass


#   EXTERNAL IMPORTS
from .fwmod import FrameworkModule


#   MODULE CLASS
class FlxrDatetimeManager(FrameworkModule):
    def __init__(self, hfw) -> None:
        """ Framework datetime manager """
        super().__init__(hfw=hfw, cls=FlxrDatetimeManager)
        pass
