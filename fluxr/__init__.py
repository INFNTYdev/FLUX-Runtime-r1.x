
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
__PACKAGE_VERSION: str = '1.0.0.4'


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
    except BaseException as non_fw:
        del non_fw, fw
        return


#   MODULE IMPORTS
from .const import *
from .ext_cde import *
from .cexc import *
from .rt import RuntimeClock
from .sys_stat import FrameworkStatusManager
from .exc import FrameworkExceptionManager
from .svc import ServiceProvider
from .sys_thread import SystemThreadManager
from .sys_datetime import SystemDatetimeManager
from .sys_rt import SystemRuntimeClock
from .sys_console import SystemConsoleManager
from .sys_io import SystemFileIOManager
from .sys_watch import SystemMonitor
from .rfw import RuntimeFramework


pass
