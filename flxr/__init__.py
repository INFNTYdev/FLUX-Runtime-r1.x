
""" INFINITY Systems LLC 2023; FLUX Runtime-Engine Framework """


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
__PACKAGE_DIRECTORY: str = str(__file__)[:-11]
__PACKAGE_VERSION: str = '1.2.2.3'
__PACKAGE_SERVICES: dict = None


#   PACKAGE METHODS
def pkg_n() -> str:
    """ Returns package name """
    return __PACKAGE_NAME


def pkg_v() -> str:
    """ Returns package version """
    return __PACKAGE_VERSION


def pkg_dir() -> str:
    """ Returns package directory """
    return __PACKAGE_DIRECTORY


def fwsvcs(**kwargs) -> any:
    """ Returns framework services call """
    if 'mode' in kwargs:
        pass


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
from .fwexc import *
from .fwsvcs import *
from .exitcde import *
from .fwfile import FWFile
from .fwchain import AssetChain
from .fwstat import StatusManager
from .fw_exclog import ExceptionLogManager
from .fw_thread import FlxrThreadManager
from .fw_dt import FlxrDatetime
from .fw_rt import FlxrRuntimeClock
from .fw_console import FlxrConsoleManager
from .fw_io import FlxrFileIOManager
...
from .fw_watch import FlxrRuntimeMonitor
from .rfw import Flxr


pass
