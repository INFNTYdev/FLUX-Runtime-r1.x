
""" SimplyDatetime Time Object """


# MODULE IMPORTS
from simplydt import *

# MODULE PACKAGE
__package__ = datetime_pkg_n()


# MODULE CLASSES
class Time:
    def __init__(self, hr: any = None, min: any = None, sec: any = None, **kwargs):
        """
        Time object

        :param hr: The times hour
        :param min: The times minute
        :param sec: The times second
        :param kwargs: Auxiliary time input (Takes precedence)
        """

        self._hour: Hour = None
        self._minute: Minute = None
        self._second: Second = None

        if kwargs.get('aux') is not None:
            self._set(kwargs.get('aux'))
        else:
            self._hour = Hour(value=hr)
            self._minute = Minute(value=min)
            self._second = Second(value=sec)

    def time(self, hformat: int = 12) -> str:
        """ Returns the time (HH:MM:SS p) """
        return f'{self._hour.value(hformat)}:{self._minute.value()}:{self._second.value()} {self._hour.phase()}'

    def raw_time(self, hformat: int = 24) -> str:
        """ Returns the raw time (HH:MM:SS) """
        return f'{self._hour.value(hformat)}:{self._minute.value()}:{self._second.value()}'

    def approx_time(self, hformat: int = 12) -> str:
        """ Returns the approximated time (HH:MM p) """
        return f'{self._hour.value(hformat)}:{self._minute.value()} {self._hour.phase()}'

    def time_tuple(self, hformat: int = 24) -> tuple[int, int, int]:
        """ Returns the time value as a tuple (hour, minute, second) """
        return tuple(
            (
                self._hour.value_int(hformat=hformat),
                self._minute.value_int(),
                self._second.value_int()
            )
        )

    def hour(self, hformat: int = 12) -> int:
        """ Returns the hour of the time """
        return self._hour.value_int(hformat=hformat)

    def get_hour(self) -> Hour:
        """ Returns the hour instance of the time """
        return self._hour

    def minute(self) -> int:
        """ Returns the minute of the time """
        return self._minute.value_int()

    def get_minute(self) -> Minute:
        """ Returns the minute instance of the time """
        return self._minute

    def second(self) -> int:
        """ Returns the second of the time """
        return self._second.value_int()

    def get_second(self) -> Second:
        """ Returns the second instance of the time """
        return self._second

    def phase(self) -> str:
        """ Returns the phase of the time """
        return self._hour.phase()

    def until(self, value: any) -> tuple[int, int, int]:
        """
        Determines the amount of time until another time value

        :param value: Another time value as datetime, Time, tuple or str (HH:MM:SS) (24 hr only)
        :return: Time remaining until value as (hrs, mins, secs)
        """
        if type(value) is Time:
            tdiff: int = (value.in_seconds() - self.in_seconds())
            hours: int = int(tdiff/3600)
            minutes: int = int((tdiff-(hours*3600))/60)
            seconds: int = int((tdiff-(hours*3600))-(minutes*60))
            return tuple((hours, minutes, seconds))
        else:
            return self.until(Time(aux=value))

    def in_seconds(self) -> int:
        """ Returns the time value in seconds """
        h, m, s = self.time_tuple()
        return int(s + ((h*3600)+(m*60)))

    def is_before(self, value: any) -> bool:
        """
        Determines if the current time is before another

        :param value: Another time value as datetime, Time, tuple or str (HH:MM:SS) (24 hr only)
        :return: True if value is after current time
        """
        if type(value) is Time:
            if value.in_seconds() > self.in_seconds():
                return True
            return False
        else:
            return self.is_before(Time(aux=value))

    def is_after(self, value: any) -> bool:
        """
        Determines if the current time is after another

        :param value: Another time value as datetime, Time, tuple or str (HH:MM:SS) (24 hr only)
        :return: True if value is before current time
        """
        if type(value) is Time:
            if value.in_seconds() < self.in_seconds():
                return True
            return False
        else:
            return self.is_after(Time(aux=value))

    def same_time(self, value: any) -> bool:
        """
        Determines if the current time value is equal to another

        :param value: Another time value as datetime, Time, tuple or str (HH:MM:SS) (24 hr only)
        :return: True if value is equal to current
        """
        if type(value) is Time:
            if not value.hour(hformat=24) == self.hour(hformat=24):
                return False

            if not value.minute() == self.minute():
                return False

            if not value.second() == self.second():
                return False
            return True
        else:
            self.same_time(Time(aux=value))

    def _set(self, aux: any):
        """ Initialize the time object values via auxiliary """
        if type(aux) is Time:
            self._hour = Hour(value=aux.hour(hformat=24))
            self._minute = Minute(value=aux.minute())
            self._second = Second(value=aux.second())
            return
        else:
            if type(aux) is tuple:
                self._hour = Hour(value=aux[0])
                self._minute = Minute(value=aux[1])
                self._second = Second(value=aux[2])
                return

            if type(aux) is str:
                _time_set: list = aux.split(':')
                self._hour = Hour(value=_time_set[0])
                self._minute = Minute(value=_time_set[1])
                self._second = Second(value=_time_set[2])
                return

            if not type(aux) is datetime:
                if aux is datetime:
                    raise TypeError(
                        'Auxiliary time input must be provided as datetime.now()'
                    )
                raise TypeError(
                    'Invalid auxiliary time input, must be datetime, Time, tuple or str object'
                )

            _time_set: list = aux.strftime('%H-%M-%S').split('-')
            self._hour = Hour(value=_time_set[0])
            self._minute = Minute(value=_time_set[1])
            self._second = Second(value=_time_set[2])
