
""" SimplyDatetime Unit Library """


# PACKAGE IMPORTS
from simplydt import *


# PACKAGE META
__PKG_N: str = str(__file__).split('\\')[-2]


# PACKAGE METHODS
def unitlib_pkg_n() -> str:
    """ Returns the package name """
    return __PKG_N


# MODULE IMPORTS
from .sec import Second
from .min import Minute
from .hr import Hour
from .day import Day
from .month import Month
from .year import Year
