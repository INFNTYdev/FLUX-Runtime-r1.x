
""" INFINITY(c) Systems 2023; FLUX Tkinter Application Framework """


#   EXTERNAL IMPORTS
from fluxr import *
import tkinter as tk
import customtkinter as ctk
from tkinter import ttk


#   PACKAGE META
__PACKAGE_NAME: str = str(__file__).split('\\')[-2]
__PACKAGE_VERSION: str = '1.0.0.0'


#   PACKAGE METHODS
def tkpkg_n() -> str:
    """ Returns package name """
    return __PACKAGE_NAME


def tkfw_v() -> str:
    """ Returns package version """
    return __PACKAGE_VERSION


#   MODULE IMPORTS
from .tkhost import TkWindow, TkWindowHost
from .tkfw import TkinterLibFramework


pass