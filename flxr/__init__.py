
""" INFINITY Systems, LLC. 2023 - FLUX Runtime-Engine Framework """


#   BUILT-IN IMPORTS
import os
import sys
import time
from threading import Thread


#   INFINITY IMPORTS
from simplydt import simplydatetime, DateTime, Date, Time


#   PACKAGE META
__FRAMEWORK_PACKAGE: str = __file__.split('\\')[-2]
__FRAMEWORK_VERSION: str = '1.5.0.2'


#   PACKAGE METHODS
def flxr_pkg_n() -> str:
    """ Returns package name """
    return __FRAMEWORK_PACKAGE


def flxr_pkg_v() -> str:
    """ Returns package version """
    return __FRAMEWORK_VERSION


#   MODULE IMPORTS
...
from flxr.fwconst import *
from .fwsvc import *
from .fwbase import *
from .fwexec import *
...
from .fwlib import *
from .rfw import Flxr
