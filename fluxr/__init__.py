
""" INFINITY(c) Systems 2023; FLUX Runtime-Engine Framework """


#   EXTERNAL IMPORTS
from datetime import datetime
from threading import Thread
import importlib
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
    """ Returns package version """
    return __PACKAGE_VERSION


def fw_obj(fw: any) -> any:
    """ Confirm framework object """
    try:
        if fw.is_fw():
            return fw
        return None
    except BaseException as non_fw:
        del non_fw
        return None


#   MODULE IMPORTS
from .const import *
from .ext_cde import *
from .cexc import *
from .stat import FrameworkStatusManager
from .exc import FrameworkExceptionManager
from .svc import ServiceProvider
from .rfw import RuntimeFramework
...


pass
