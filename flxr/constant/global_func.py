
"""
Framework Global Function Module
"""


#   BUILT-IN IMPORTS
import inspect


def class_of(obj) -> type:
    """ Returns the class type of the
    specified object """
    if 'object' in str(obj):
        return obj.__class__
    elif inspect.isclass(obj):
        return obj
