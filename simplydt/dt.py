
""" Datetime Object """


# MODULE IMPORTS
from simplydt import *

# MODULE PACKAGE
__package__ = datetime_pkg_n()


# MODULE CLASSES
class DateTime:
    def __init__(self, **kwargs):
        """
        Datetime object

        :param kwargs: Auxiliary datetime input
        """

        if kwargs.get('aux') is not None:
            self._set(kwargs.get('aux'))
        else:
            self._date: Date = Date(
                m=kwargs.get('m'),
                d=kwargs.get('d'),
                y=kwargs.get('y')
            )
            self._time: Time = Time(
                hr=kwargs.get('hr'),
                min=kwargs.get('min'),
                sec=kwargs.get('sec')
            )

    def date_time(self, hformat: int = 12) -> str:
        """ Returns the datetime (MM-DD-YYYY HH:MM:SS p) """
        return f'{self._date.datetime_date()} {self._time.time(hformat=hformat)}'

    def raw_datetime(self, hformat: int = 24):
        """ Returns the raw datetime (YYYY-MM-DD HH:MM:SS) """
        return f'{self._date.raw_date()} {self._time.raw_time(hformat=hformat)}'

    def datetime_tuple(self, hformat: int = 12) -> tuple:
        """ Returns the datetime value as a tuple (month, day, year, hour, minute, second) """
        return tuple(
            (
                self._date.month(),
                self._date.day(),
                self._date.year(),
                self._time.hour(hformat=hformat),
                self._time.minute(),
                self._time.second()
            )
        )

    def date(self) -> str:
        """ Returns the date (MM/DD/YYYY) """
        return self._date.date()

    def raw_date(self) -> str:
        """ Returns the raw date (YYYY-MM-DD) """
        return self._date.raw_date()

    def approx_date(self) -> str:
        """ Returns the approximated date (MM/DD) """
        return self._date.approx_date()

    def date_tuple(self) -> tuple[int, int, int]:
        """ Returns the date value as a tuple (month, day, year) """
        return self._date.date_tuple()

    def month(self) -> int:
        """ Returns the month of the date """
        return self._date.month()

    def month_name(self) -> str:
        """ Returns the month name """
        return self._date.month_name()

    def get_month(self) -> Month:
        """ Returns the month instance of the date """
        return self._date.get_month()

    def day(self) -> int:
        """ Returns the day of the date """
        return self._date.day()

    def get_day(self) -> Day:
        """ Returns the day instance of the date """
        return self._date.get_day()

    def year(self) -> int:
        """ Returns the year of the date """
        return self._date.year()

    def get_year(self) -> Year:
        """ Returns the year instance of the date """
        return self._date.get_year()

    def get_date(self) -> Date:
        """ Returns the date instance of the datetime """
        return self._date

    def time(self, hformat: int = 12) -> str:
        """ Returns the time (HH:MM:SS p) """
        return self._time.time(hformat=hformat)

    def raw_time(self, hformat: int = 24) -> str:
        """ Returns the raw time (HH:MM:SS) """
        return self._time.raw_time(hformat=hformat)

    def approx_time(self, hformat: int = 12) -> str:
        """ Returns the approximated time (HH:MM p) """
        return self._time.approx_time(hformat=hformat)

    def time_tuple(self, hformat: int = 24) -> tuple[int, int, int]:
        """ Returns the time value as a tuple (hour, minute, second) """
        return self._time.time_tuple(hformat=hformat)

    def hour(self, hformat: int = 12) -> int:
        """ Returns the hour of the time """
        return self._time.hour(hformat=hformat)

    def get_hour(self) -> Hour:
        """ Returns the hour instance of the time """
        return self._time.get_hour()

    def minute(self) -> int:
        """ Returns the minute of the time """
        return self._time.minute()

    def get_minute(self) -> Minute:
        """ Returns the minute instance of the time """
        return self._time.get_minute()

    def second(self) -> int:
        """ Returns the second of the time """
        return self._time.second()

    def get_second(self) -> Second:
        """ Returns the second instance of the time """
        return self._time.get_second()

    def phase(self) -> str:
        """ Returns the phase of the time """
        return self._time.phase()

    def get_time(self) -> Time:
        """ Returns the time instance of the datetime """
        return self._time

    def until(self, value: any) -> tuple[int, int, int, int, int, int]:
        """
        Determines the total amount of time until another datetime value

        :param value: Another datetime value as datetime, DateTime or tuple (MM, DD, YYYY, HH, MM, SS) (24 hr only)
        :return: Total time remaining until value as (years, months, days, hours, minutes, seconds)
        """
        if type(value) is DateTime:
            years, months, days = self._date.until(value.get_date())
            hrs, mins, secs = self._time.until(value.get_time())
            return tuple((years, months, days, hrs, mins, secs))
        else:
            return self.until(DateTime(aux=value))

    def is_before(self, value: any) -> bool:
        """
        Determines if the current datetime is before another time object

        :param value: Another datetime or time object as datetime, DateTime, Date, Time or tuple: (MM, DD, YYYY, HH, MM, SS) (24 hr only)
        :return: True if value is after current datetime
        """
        if type(value) is DateTime:
            if value.date() != self.date():
                if value.get_date().is_after(self._date):
                    if value.get_time().is_after(self._time):
                        return True
                return False
            else:
                if value.get_time().is_after(self._time):
                    return True
                return False
        elif type(value) is datetime:
            return self.is_before(DateTime(aux=value))
        elif type(value) is Date:
            if value.is_after(self._date):
                return True
            return False
        elif type(value) is Time:
            if value.is_after(self._time):
                return True
            return False
        else:
            if self._is_date(value):
                return self.is_before(Date(aux=value))
            elif self._is_time(value):
                return self.is_before(Time(aux=value))

        if type(value) is tuple:
            return self.is_before(DateTime(aux=value))
        raise ValueError(
            f"Invalid datetime comparison value: '{value}'"
        )

    def is_after(self, value: any) -> bool:
        """
        Determines if the current datetime is after another

        :param value: Another datetime value as datetime, DateTime or tuple (MM, DD, YYYY, HH, MM, SS)
        :return: True if value is before current datetime
        """
        if type(value) is DateTime:
            if value.date() != self.date():
                if value.get_date().is_before(self._date):
                    if value.get_time().is_before(self._time):
                        return True
                return False
            else:
                if value.get_time().is_before(self._time):
                    return True
                return False
        elif type(value) is datetime:
            return self.is_after(DateTime(aux=value))
        elif type(value) is Date:
            if value.is_before(self._date):
                return True
            return False
        elif type(value) is Time:
            if value.is_before(self._time):
                return True
            return False
        else:
            if self._is_date(value):
                return self.is_after(Date(aux=value))
            elif self._is_time(value):
                return self.is_after(Time(aux=value))

        if type(value) is tuple:
            return self.is_after(DateTime(aux=value))
        raise ValueError(
            f"Invalid datetime comparison value: '{value}'"
        )

    def same_datetime(self, value: any) -> bool:
        """
        Determines if the current datetime value is equal to another

        :param value: Another datetime value as datetime, DateTime or tuple (MM, DD, YYYY, HH, MM, SS)
        :return: True if value is equal to current
        """
        if type(value) is DateTime:
            if not value.get_date().same_date(self._date):
                return False

            if not value.get_time().same_time(self._time):
                return False
            return True
        else:
            return self.same_datetime(DateTime(aux=value))

    @staticmethod
    def _is_date(value: any) -> bool:
        """ Determines if a value is a date """
        if type(value) is str:
            if value.__contains__('/'):
                d: list = value.split('/')
                if (len(d[2]) == 4) and (1 <= int(d[0]) <= 12):
                    return True
            elif value.__contains__('-'):
                d: list = value.split('-')
                if (len(d[2]) == 4) and (1 <= int(d[0]) <= 12):
                    return True

        if type(value) is tuple:
            if not len(value) == 3:
                return False

            if (len(str(value[2])) == 4) and (1 <= int(value[0]) <= 12):
                return True
        return False

    @staticmethod
    def _is_time(value: any) -> bool:
        """ Determines if a value is time """
        if type(value) is str:
            t: list = value.split(':')
            if 0 <= t[0] <= 23:
                if (0 <= t[1] <= 59) and (0 <= t[2] <= 59):
                    return True

        if type(value) is tuple:
            if not len(value) == 3:
                return False

            if 0 <= value[0] <= 23:
                if (0 <= value[1] <= 59) and (0 <= value[2] <= 59):
                    return True
        return False

    def _set(self, aux: any):
        """ Initialize the datetime object values via auxiliary """
        if type(aux) is DateTime:
            self._date = Date(aux=aux.get_date())
            self._time = Time(aux=aux.get_time())
            return
        else:
            if type(aux) is tuple:
                _m, _d, _y, _hr, _min, _sec = aux
                self._date = Date(aux=(_m, _d, _y))
                self._time = Time(aux=(_hr, _min, _sec))
                return

            if not type(aux) is datetime:
                if aux is datetime:
                    raise TypeError(
                        'Auxiliary datetime input must be provided as datetime.now()'
                    )
                raise TypeError(
                    'Invalid auxiliary datetime input, must be datetime, DateTime or tuple object'
                )

            self._date = Date(aux=aux)
            self._time = Time(aux=aux)
