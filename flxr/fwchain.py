
""" Framework asset chain object """


# MODULE IMPORTS
from flxr import *

# MODULE PACKAGE
__package__ = pkg_n()


# MODULE CLASSES
class AssetChain(dict):
    def __init__(self):
        dict.__init__(self)

    def func(self, asset: type, func: str, **kwargs) -> any:
        """ Execute the function of a chained asset """
        if inspect.isclass(asset):
            return getattr(self.get(asset), func)(**kwargs)
