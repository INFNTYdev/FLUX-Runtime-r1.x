
""" SimplyDatetime Minute Object """


# MODULE IMPORTS
from simplydt.unitlib import *

# MODULE PACKAGE
__package__ = unitlib_pkg_n()


# MODULE CLASSES
class Minute:

    _MIN_SEQ: int = 0
    _MAX_SEQ: int = 60

    def __init__(self, value: any):
        """
        Minute object

        :param value: Value to initialize the minute with (Minute, int or str)
        """

        self._value: str = self._set(value=value)

    def value(self) -> str:
        """ Returns the value of the minute """
        return self._value

    def value_int(self) -> int:
        """ Returns the value of the minute as an integer """
        return int(self._value)

    def until_hour(self) -> int:
        """ Returns the amount of minutes until a complete hour """
        return int(self._MAX_SEQ - self.value_int())

    def until(self, value: any) -> int:
        """
        Determines the amount of minutes until another minute value

        :param value: Another minute value as a Minute, int or str
        :return: Minutes remaining until value
        """
        if type(value) is Minute:
            return int(value.value_int() - self.value_int())
        else:
            return int(Minute(value=value).value_int() - self.value_int())

    def in_seconds(self) -> int:
        """ Returns the minute value in seconds """
        return int(self.value_int()*60)

    def is_before(self, value: any) -> bool:
        """
        Determines if the current minute is before another

        :param value: Another minute value as a Minute, int or str
        :return: True if value is after current minute
        """
        if type(value) is Minute:
            if value.value_int() > self.value_int():
                return True
        else:
            if Minute(value=value).value_int() > self.value_int():
                return True
        return False

    def is_after(self, value: any) -> bool:
        """
        Determines if the current minute is after another

        :param value: Another minute value as a Minute, int or str
        :return: True if value is before current minute
        """
        if type(value) is Minute:
            if value.value_int() < self.value_int():
                return True
        else:
            if Minute(value=value).value_int() < self.value_int():
                return True
        return False

    def _set(self, value: any) -> str:
        """ Initialize the minute object value """
        if type(value) is Minute:
            return value.value()

        if not str(value).isdecimal():
            raise ValueError(
                f"Invalid value '{value}' for type {Minute.__name__}"
            )

        if not self._MIN_SEQ <= int(value) <= self._MAX_SEQ - 1:
            raise ValueError(
                f"Invalid minute value: {value}"
            )

        if len(str(value)) == 1:
            return f'0{value}'
        elif len(str(value)) == 2:
            return str(value)
