
""" FLUX Runtime-Engine Tkinter Framework """


#   EXTERNAL IMPORTS
import tkinter as tk
from flxr import fw_obj
from tkinter import ttk
from flxr.const import *
import customtkinter as ctk
from threading import Thread


#   PACKAGE META
__PACKAGE_NAME: str = str(__file__).split('\\')[-2]
__PACKAGE_DIRECTORY: str = str(__file__)[:-11]
__PACKAGE_VERSION: str = '1.0.0.0'


#   PACKAGE METHODS
def tkpkg_n() -> str:
    """ Returns package name """
    return __PACKAGE_NAME


def tkpkg_v() -> str:
    """ Returns package version """
    return __PACKAGE_VERSION


def tkpkg_dir() -> str:
    """ Returns package directory """
    return __PACKAGE_DIRECTORY


#   MODULE IMPORTS
from .tkl_window import TkinterWindowDispatcher, TkinterWindow
from .flxr_tk import FlxrTkinterLibrary


pass
