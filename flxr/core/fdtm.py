
"""
Framework Datetime Manager Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
pass


#   EXTERNAL IMPORTS
from simplydt import simplydatetime, DateTime, Date, Time
from .fwmod import FrameworkModule


#   MODULE CLASS
class FlxrDatetimeManager(FrameworkModule):
    def __init__(self, hfw) -> None:
        """ Framework datetime manager """
        super().__init__(hfw=hfw, cls=FlxrDatetimeManager)
        self._run: bool = False
        self._refresh: float = 0.2
