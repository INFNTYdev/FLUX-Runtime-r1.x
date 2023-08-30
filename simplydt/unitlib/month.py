
""" SimplyDatetime Month Object """


# MODULE IMPORTS
from simplydt.unitlib import *

# MODULE PACKAGE
__package__ = unitlib_pkg_n()


# MODULE CLASSES
class Month:

    _MIN_SEQ: int = 1
    _MAX_SEQ: int = 12

    def __init__(self, value: any):
        """
        Month object

        :param value: Value to initialize the month with (Month, int or str)
        """

        self._value: str = self._set(value=value)

    def value(self) -> str:
        """ Returns the value of the month """
        return self._value

    def value_int(self) -> int:
        """ Returns the value of the month as an integer """
        return int(self._value)

    def name(self) -> str:
        """ Returns the month name """
        return self._month_list()[self.value_int()]

    def until(self, value: any) -> int:
        """
        Determines the amount of months until another month value

        :param value: Another month value as a Month, int or str
        :return: Months remaining until value
        """
        if type(value) is Month:
            return int(value.value_int() - self.value_int())
        else:
            return int(Month(value=value).value_int() - self.value_int())

    def _set(self, value: any) -> str:
        """ Initialize the month object value """
        if type(value) is Month:
            return value.value()

        if not str(value).isdecimal():
            if str(value).capitalize() in self._month_list():
                value: int = self._month_list().index(str(value).capitalize())
                if len(str(value)) == 1:
                    return f'0{value}'
                elif len(str(value)) == 2:
                    return str(value)
            else:
                raise ValueError(
                    f"Invalid value '{value}' for type {Month.__name__}"
                )

        if not self._MIN_SEQ <= int(value) <= self._MAX_SEQ:
            raise ValueError(
                f"Invalid month value: {value}"
            )

        if len(str(value)) == 1:
            return f'0{value}'
        elif len(str(value)) == 2:
            return str(value)

    @staticmethod
    def _month_list() -> list:
        """ Returns the list of month names """
        return list(calendar.month_name)
