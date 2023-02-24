
""" INFINITY(c) Systems 2023; FLUX Runtime-Engine Framework """


#   EXTERNAL IMPORTS
from datetime import datetime
from threading import Thread
import inspect
import random
import time
import stat
import ast
import sys
import os


#   PACKAGE META
__PACKAGE_NAME: str = str(__file__).split('\\')[-2]
__PACKAGE_VERSION: str = '1.0.0.0'


#   PACKAGE METHODS
def pkg_n() -> str:
    """ Returns package name """
    return __PACKAGE_NAME


def pkg_v() -> str:
    """ Returns the package version """
    return __PACKAGE_VERSION


#   MODULE IMPORTS
from .const import *
from .ext_cde import *
from .fw import RuntimeFramework
...


pass
