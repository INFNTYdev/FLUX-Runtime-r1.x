
"""
Framework Client Manager Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
import ctypes
import platform


#   EXTERNAL IMPORTS
pass


#   MODULE CLASS
class ClientManager:
    def __init__(self) -> None:
        """ Framework user client manager """
        pass

    @staticmethod
    def operating_system() -> str:
        """ Returns client operating system """
        return platform.system()

    @staticmethod
    def os_version() -> str:
        """ Returns client operating
        system version """
        return platform.version()

    @staticmethod
    def display_width() -> int:
        """ Returns client
        display width in pixels """
        return ctypes.windll.user32.GetSystemMetrics(0)

    @staticmethod
    def display_height() -> int:
        """ Returns client
        display height in pixels """
        return ctypes.windll.user32.GetSystemMetrics(1)
