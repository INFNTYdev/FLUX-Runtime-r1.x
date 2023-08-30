
""" SimplyDatetime: Return Module """


# MODULE IMPORTS
from simplydt import *

# MODULE PACKAGE
__package__ = datetime_pkg_n()


# MODULE METHODS
def _now_datetime() -> DateTime:
    return DateTime(aux=datetime.now())


now = _now_datetime
