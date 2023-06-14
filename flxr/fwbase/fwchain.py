
""" Framework Asset Chain """


#   MODULE IMPORTS
from flxr.fwbase import inspect


#   MODULE CLASSES
class AssetChain(dict):
    def __init__(self):
        """ Framework asset chain """
        dict.__init__(self)
    
    def asset_func(self, asset: type, func: str, **fargs) -> any:
        """
        Execute the function of a chained asset

        :param asset: Asset class in which to invoke the function call
        :param func: Asset function name
        :param fargs: Function arguments
        :return: Functions return value if any
        """
        if inspect.isclass(asset):
            return getattr(self.get(asset), func)(**fargs)
