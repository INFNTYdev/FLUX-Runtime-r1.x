
""" SimplyDatetime Year Object """


# MODULE IMPORTS
from simplydt.unitlib import *

# MODULE PACKAGE
__package__ = unitlib_pkg_n()


# MODULE CLASSES
class Year:

    _MIN_SEQ: int = 1800

    def __init__(self, value: any):
        """
        Year object

        :param value: Value to initialize the year with (Year, int or str)
        """

        self._value: str = self._set(value=value)

    def value(self) -> str:
        """ Returns the value of the year """
        return self._value

    def value_int(self) -> int:
        """ Returns the value of the year as an integer """
        return int(self._value)

    def until(self, value: any) -> int:
        """
        Determines the amount of years until another year value

        :param value: Another year value as a Year, int or str
        :return: Years remaining until value
        """
        if type(value) is Year:
            return int(value.value_int() - self.value_int())
        else:
            return int(Year(value=value).value_int() - self.value_int())

    def _set(self, value: any) -> str:
        """ Initialize the year object value """
        if type(value) is Year:
            return value.value()

        if not str(value).isdecimal():
            raise ValueError(
                f"Invalid value '{value}' for type {Year.__name__}"
            )

        if not int(value) > self._MIN_SEQ:
            raise ValueError(
                f"Invalid year value: {value}"
            )

        return str(value)
