
""" SimplyDatetime Second Object """


# MODULE IMPORTS
from simplydt.unitlib import *

# MODULE PACKAGE
__package__ = unitlib_pkg_n()


# MODULE CLASSES
class Second:

    _MIN_SEQ: int = 0
    _MAX_SEQ: int = 60

    def __init__(self, value: any):
        """
        Second object

        :param value: Value to initialize the second with (Second, int or str)
        """

        self._value: str = self._set(value=value)

    def value(self) -> str:
        """ Returns the value of the second """
        return self._value

    def value_int(self) -> int:
        """ Returns the value of the second as an integer """
        return int(self._value)

    def until_minute(self) -> int:
        """ Returns the amount of seconds until a complete minute """
        return int(self._MAX_SEQ - self.value_int())

    def until(self, value: any) -> int:
        """
        Determines the amount of seconds until another second value

        :param value: Another second value as a Second, int or str
        :return: Seconds remaining until value
        """
        if type(value) is Second:
            return int(value.value_int() - self.value_int())
        else:
            return int(Second(value=value).value_int() - self.value_int())

    def is_before(self, value: any) -> bool:
        """
        Determines if the current second is before another

        :param value: Another second value as a Second, int or str
        :return: True if value is after current second
        """
        if type(value) is Second:
            if value.value_int() > self.value_int():
                return True
        else:
            if Second(value=value).value_int() > self.value_int():
                return True
        return False

    def is_after(self, value: any) -> bool:
        """
        Determines if the current second is after another

        :param value: Another second value as a Second, int or str
        :return: True if value is before current second
        """
        if type(value) is Second:
            if value.value_int() < self.value_int():
                return True
        else:
            if Second(value=value).value_int() < self.value_int():
                return True
        return False

    def _set(self, value: any) -> str:
        """ Initialize the second object value """
        if type(value) is Second:
            return value.value()

        if not str(value).isdecimal():
            raise ValueError(
                f"Invalid value '{value}' for type {Second.__name__}"
            )

        if not self._MIN_SEQ <= int(value) <= self._MAX_SEQ - 1:
            raise ValueError(
                f"Invalid second value: {value}"
            )

        if len(str(value)) == 1:
            return f'0{value}'
        elif len(str(value)) == 2:
            return str(value)
