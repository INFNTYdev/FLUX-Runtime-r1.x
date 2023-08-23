
"""
Framework Thread Manager Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
pass


#   EXTERNAL IMPORTS
from .fwmod import FrameworkModule


#   MODULE CLASS
class FlxrThreadManager(FrameworkModule):
    def __init__(self, hfw) -> None:
        """ Framework thread manager """
        super().__init__(hfw=hfw, cls=FlxrThreadManager)
        pass
