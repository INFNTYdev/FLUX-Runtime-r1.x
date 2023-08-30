
""" SimplyDatetime Day Object """


# MODULE IMPORTS
from simplydt.unitlib import *

# MODULE PACKAGE
__package__ = unitlib_pkg_n()


# MODULE CLASSES
class Day:

    _MIN_SEQ: int = 1
    _MAX_SEQ: int = 31

    def __init__(self, value: any):
        """
        Second object

        :param value: Value to initialize the day with (Day, int or str)
        """

        self._value: str = self._set(value=value)

    def value(self) -> str:
        """ Returns the value of the day """
        return self._value

    def value_int(self) -> int:
        """ Returns the value of the day as an integer """
        return int(self._value)

    def until(self, value: any) -> int:
        """
        Determines the amount of days until another day value

        :param value: Another day value as a Day, int or str
        :return: Days remaining until value
        """
        if type(value) is Day:
            return int(value.value_int() - self.value_int())
        else:
            return int(Day(value=value).value_int() - self.value_int())

    def in_hours(self) -> int:
        """ Returns the day value in hours """
        return int(self.value_int()*24)

    def in_minutes(self) -> int:
        """ Returns the day value in minutes """
        return int((self.value_int()*24)*60)

    def in_seconds(self) -> int:
        """ Returns the day value in seconds """
        return int((self.value_int()*24)*3600)

    def is_before(self, value: any) -> bool:
        """
        Determines if the current day is before another

        :param value: Another day value as a Day, int or str
        :return: True if value is after current day
        """
        if type(value) is Day:
            if value.value_int() > self.value_int():
                return True
        else:
            if Day(value=value).value_int() > self.value_int():
                return True
        return False

    def is_after(self, value: any) -> bool:
        """
        Determines if the current day is after another

        :param value: Another day value as a Day, int or str
        :return: True if value is before current day
        """
        if type(value) is Day:
            if value.value_int() < self.value_int():
                return True
        else:
            if Day(value=value).value_int() < self.value_int():
                return True
        return False

    def _set(self, value: any) -> str:
        """ Initialize the day object value """
        if type(value) is Day:
            return value.value()

        if not str(value).isdecimal():
            raise ValueError(
                f"Invalid value '{value}' for type {Day.__name__}"
            )

        if not self._MIN_SEQ <= int(value) <= self._MAX_SEQ:
            raise ValueError(
                f"Invalid day value: {value}"
            )

        if len(str(value)) == 1:
            return f'0{value}'
        elif len(str(value)) == 2:
            return str(value)
