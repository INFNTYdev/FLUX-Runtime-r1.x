
"""
Framework Asset Chain Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
import inspect


#   EXTERNAL IMPORTS
pass


#   MODULE CLASS
class AssetChain(dict):
    def __init__(self) -> None:
        """ Framework module asset chain """
        super().__init__()

    def asset_classes(self) -> list[type]:
        """ Returns the list of asset chain
        module classes """
        return [_type for _type in self.keys()]

    def asset_func(self, asset: type, _func: str, **fargs) -> any:
        """ Execute the specified asset function """
        if inspect.isclass(asset):
            return getattr(self.get(asset), _func)(**fargs)
