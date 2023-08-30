
""" SimplyDatetime Hour Object """


# MODULE IMPORTS
from simplydt.unitlib import *

# MODULE PACKAGE
__package__ = unitlib_pkg_n()


# MODULE CLASSES
class Hour:

    _MIN_SEQ: int = 0
    _MAX_SEQ: int = 24

    def __init__(self, value: any):
        """
        Hour object

        :param value: Value to initialize the hour with (Hour, int or str)
        """

        self._value: str = self._set(value=value)
        if self._MIN_SEQ <= self.value_int(hformat=24) <= 11:
            self._phase: str = 'AM'
        elif 12 <= self.value_int(hformat=24) <= self._MAX_SEQ:
            self._phase: str = 'PM'

    def value(self, hformat: int = 12) -> str:
        """ Returns the value of the hour """
        if not self._valid_hour_format(hformat):
            self._invalid_format_error(hformat)

        if hformat == 12:
            return self._12_hr_format(hour=self._value)
        elif hformat == 24:
            return self._value

    def value_int(self, hformat: int = 12) -> int:
        """ Returns the value of the hour as an integer """
        if not self._valid_hour_format(hformat):
            self._invalid_format_error(hformat)

        if hformat == 12:
            return int(self._12_hr_format(hour=self._value))
        elif hformat == 24:
            return int(self._value)

    def phase(self) -> str:
        """ Returns the phase of the hour """
        return self._phase

    def until_day(self) -> int:
        """ Returns the amount of hours until a complete day """
        return int(self._MAX_SEQ - self.value_int(hformat=24))

    def until(self, value: any) -> int:
        """
        Determines the amount of hours until another hour value

        :param value: Another hour value as an Hour, int or str (24 hr only)
        :return: Hours remaining until value
        """
        if type(value) is Hour:
            return int(value.value_int(hformat=24) - self.value_int(hformat=24))
        else:
            return int(Hour(value=value).value_int(hformat=24) - self.value_int(hformat=24))

    def in_minutes(self) -> int:
        """ Returns the hour value in minutes """
        return int(self.value_int()*60)

    def in_seconds(self) -> int:
        """ Returns the hour value in seconds """
        return int(self.value_int()*3600)

    def is_before(self, value: any) -> bool:
        """
        Determines if the current hour is before another

        :param value: Another hour value as an Hour, int or str (24 hr only)
        :return: True if value is after current hour
        """
        if type(value) is Hour:
            if value.value_int(hformat=24) > self.value_int(hformat=24):
                return True
        else:
            if Hour(value=value).value_int(hformat=24) > self.value_int(hformat=24):
                return True
        return False

    def is_after(self, value: any) -> bool:
        """
        Determines if the current hour is after another

        :param value: Another hour value as an Hour, int or str (24 hr only)
        :return: True if value is before current second
        """
        if type(value) is Hour:
            if value.value_int(hformat=24) < self.value_int(hformat=24):
                return True
        else:
            if Hour(value=value).value_int(hformat=24) < self.value_int(hformat=24):
                return True
        return False

    def _set(self, value: any) -> str:
        """ Initialize the hour object value """
        if type(value) is Hour:
            return value.value(hformat=24)

        if not str(value).isdecimal():
            raise ValueError(
                f"Invalid value '{value}' for type {Hour.__name__}"
            )

        if not self._MIN_SEQ <= int(value) <= self._MAX_SEQ - 1:
            raise ValueError(
                f"Invalid hour value: {value}"
            )

        if len(str(value)) == 1:
            return f'0{value}'
        elif len(str(value)) == 2:
            return str(value)

    @staticmethod
    def _12_hr_format(hour: str) -> str:
        """ Format 24-hour to 12-hour """
        if int(hour) == 0:
            return '12'
        elif 0 <= int(hour) <= 12:
            if len(str(hour)) == 1:
                return f'0{hour}'
            elif len(str(hour)) == 2:
                return str(hour)
        else:
            if len(str(int(hour)-12)) == 1:
                return f'0{int(hour)-12}'
            elif len(str(int(hour)-12)) == 2:
                return str(int(hour)-12)

    @staticmethod
    def _valid_hour_format(value: int) -> bool:
        """ Determines if a provided hour format is valid """
        if (value == 12) or (value == 24):
            return True
        return False

    @staticmethod
    def _invalid_format_error(hformat: int) -> None:
        """ Raises value error on invalid hour formats """
        raise ValueError(
            f"Invalid hour format '{hformat}' must be 12 or 24"
        )
