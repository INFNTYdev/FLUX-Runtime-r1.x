
"""
FLUX-Tkinter View Property Manager Module
"""


#   EXTERNAL IMPORTS
from flxr.common.protocols import FwV
from .fwvpm import FwvPropertyManager


#   MODULE CLASS
class ViewPropertyManager(FwvPropertyManager):
    def __init__(self, ftk: FwV, master, **kwargs) -> None:
        """ Framework view property manager """
        super().__init__(ftk=ftk, master=master, **kwargs)
