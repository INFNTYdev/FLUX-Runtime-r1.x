
""" INFINITY Systems, LLC. 2023 - SimplyDatetime Library """


# EXTERNAL IMPORTS
from datetime import datetime
import calendar


# PACKAGE META
__PKG_N: str = str(__file__).split('\\')[-2]
__PKG_V: str = '1.1.0.2'


# PACKAGE METHODS
def datetime_pkg_n() -> str:
    """ Returns the package name """
    return __PKG_N


def datetime_pkg_v() -> str:
    """ Returns the package version """
    return __PKG_V


# MODULE IMPORTS
from simplydt.unitlib import *
from .dt_time import Time
from .dt_date import Date
from .dt import DateTime
import simplydt.simplydatetime
