
""" SimplyDatetime Date Object """


# MODULE IMPORTS
from simplydt import *

# MODULE PACKAGE
__package__ = datetime_pkg_n()


# MODULE CLASSES
class Date:
    def __init__(self, m: any = None, d: any = None, y: any = None, **kwargs):
        """
        Date object

        :param m: The dates month
        :param d: The dates day
        :param y: The dates year
        :param kwargs: Auxiliary date input (Takes precedence)
        """

        self._month: Month = None
        self._day: Day = None
        self._year: Year = None

        if kwargs.get('aux') is not None:
            self._set(kwargs.get('aux'))
        else:
            self._month = Month(value=m)
            self._day = Day(value=d)
            self._year = Year(value=y)

    def date(self) -> str:
        """ Returns the date (MM/DD/YYYY) """
        return f'{self._month.value()}/{self._day.value()}/{self._year.value()}'

    def raw_date(self) -> str:
        """ Returns the raw date (YYYY-MM-DD) """
        return f'{self._year.value()}-{self._month.value()}-{self._day.value()}'

    def approx_date(self) -> str:
        """ Returns the approximated date (MM/DD) """
        return f'{self._month.value()}/{self._day.value()}'

    def datetime_date(self) -> str:
        """ Returns the datetime date (MM-DD-YYYY) """
        return f'{self._month.value()}-{self._day.value()}-{self._year.value()}'

    def date_tuple(self) -> tuple[int, int, int]:
        """ Returns the date value as a tuple (month, day, year) """
        return tuple(
            (
                self._month.value_int(),
                self._day.value_int(),
                self._year.value_int()
            )
        )

    def month(self) -> int:
        """ Returns the month of the date """
        return self._month.value_int()

    def month_name(self) -> str:
        """ Returns the month name """
        return self._month.name()

    def get_month(self) -> Month:
        """ Returns the month instance of the date """
        return self._month

    def day(self) -> int:
        """ Returns the day of the date """
        return self._day.value_int()

    def get_day(self) -> Day:
        """ Returns the day instance of the date """
        return self._day

    def year(self) -> int:
        """ Returns the year of the date """
        return self._year.value_int()

    def get_year(self) -> Year:
        """ Returns the year instance of the date """
        return self._year

    def year_difference(self, value: any) -> int:
        """
        Determines the difference in years between two dates

        :param value: Another date value as datetime, Date, tuple or str (MM/DD/YYYY)
        :return: |(value year - current year)|
        """
        if type(value) is Date:
            return int(abs(value.year() - self.year()))
        else:
            return self.year_difference(Date(aux=value))

    def month_difference(self, value: any) -> int:
        """
        Determines the difference in months between two dates

        :param value: Another date value as datetime, Date, tuple or str (MM/DD/YYYY)
        :return: |(value month - current month)|
        """
        if type(value) is Date:
            return int(abs(value.month() - self.month()))
        else:
            return self.month_difference(Date(aux=value))

    def day_difference(self, value: any) -> int:
        """
        Determines the difference in days between two dates

        :param value: Another date value as datetime, Date, tuple or str (MM/DD/YYYY)
        :return: |(value day - current day)|
        """
        if type(value) is Date:
            return int(abs(value.day() - self.day()))
        else:
            return self.day_difference(Date(aux=value))

    def until(self, value: any) -> tuple[int, int, int]:
        """
        Determines the amount of time until another date value

        :param value: Another date value as datetime, Date, tuple or str (MM/DD/YYYY)
        :return: Time remaining until value as (years, months, days)
        """
        effect: int = 1
        if type(value) is Date:
            day_delta: int = (value.day() + (self._month_frame_max(self.month(), self.year()) - self.day()))
            if (value.month() == self.month()) and (value.year() == self.year()):
                day_delta = (value.day() - self.day())
            if self.is_after(value):
                effect = -1
                month_delta: int = self._months_between(
                    frame1=(value.month(), value.year()),
                    frame2=(self.month(), self.year())
                )
                day_delta *= -1
            else:
                month_delta: int = self._months_between(
                    frame1=(self.month(), self.year()),
                    frame2=(value.month(), value.year())
                )

            year_delta: int = int(month_delta/12)*effect
            month_delta = (month_delta - (year_delta*12))*effect
            return tuple((year_delta, month_delta, day_delta))
        else:
            return self.until(Date(aux=value))

    def days_until(self, value: any) -> int:
        """
        Determines the amount of days until another date value

        :param value: Another date value as datetime, Date, tuple or str (MM/DD/YYYY)
        :return: Days remaining until value
        """
        if type(value) is Date:
            delta_raw: int = self._time_frame_days(
                frame1=(self.month(), self.year()),
                frame2=(value.month(), value.year())
            )
            delta: int = int(delta_raw - self.day())
            delta += value.day()
            return delta
        else:
            return self.days_until(Date(aux=value))

    def is_before(self, value: any) -> bool:
        """
        Determines if the current date is before another

        :param value: Another date value as datetime, Date, tuple or str (MM/DD/YYYY)
        :return: True if value is after current date
        """
        if type(value) is Date:
            if value.year() > self.year():
                return True
            elif value.year() < self.year():
                return False

            if value.month() > self.month():
                return True
            elif value.month() < self.month():
                return False

            if value.day() > self.day():
                return True
            return False
        else:
            return self.is_before(Date(aux=value))

    def is_after(self, value: any) -> bool:
        """
        Determines if the current date is after another

        :param value: Another date value as datetime, Date, tuple or str (MM/DD/YYYY)
        :return: True if value is before current date
        """
        if type(value) is Date:
            if value.year() < self.year():
                return True
            elif value.year() > self.year():
                return False

            if value.month() < self.month():
                return True
            elif value.month() > self.month():
                return False

            if value.day() < self.day():
                return True
            return False
        else:
            return self.is_after(Date(aux=value))

    def same_date(self, value: any) -> bool:
        """
        Determines if the current date value is equal to another

        :param value: Another date value as datetime, Date, tuple or str (MM/DD/YYYY)
        :return: True if value is equal to current
        """
        if type(value) is Date:
            if not value.month() == self.month():
                return False

            if not value.day() == self.day():
                return False

            if not value.year() == self.year():
                return False
            return True
        else:
            return self.same_date(Date(aux=value))

    @staticmethod
    def _month_frame_max(m: int, y: int) -> int:
        """ Returns the maximum amount of days in a months time frame """
        return int(calendar.monthrange(y, m)[1])

    @staticmethod
    def _time_frame_days(frame1: tuple[int, int], frame2: tuple[int, int]) -> int:
        """ Calculates the total number of days in a time frame (month, year) """
        def same_frame(f1: tuple, f2: tuple):
            """ Determines if two time frames are the same """
            if (f1[0] == f2[0]) and (f1[1] == f2[1]):
                return True
            return False

        start_m, start_y = frame1
        end_m, end_y = frame2
        total: int = 0

        while not same_frame((start_m, start_y), (end_m, end_y)):
            total += calendar.monthrange(start_y, start_m)[1]
            if start_m == 12:
                start_m = 1
                start_y += 1
            else:
                start_m += 1
        return total

    @staticmethod
    def _months_between(frame1: tuple[int, int], frame2: tuple[int, int], effect: int = 1) -> int:
        """ Returns the number of whole months in a time frame """
        def same_frame(f1: tuple, f2: tuple):
            """ Determines if two time frames are the same """
            if (f1[0] == f2[0]) and (f1[1] == f2[1]):
                return True
            return False

        start_m, start_y = frame1
        end_m, end_y = frame2
        total: int = 0
        skip: bool = True

        while not same_frame((start_m, start_y), (end_m, end_y)):
            if start_m == 12:
                start_m = 1
                start_y += 1
                if skip:
                    skip = False
                else:
                    total += 1
            else:
                start_m += 1
                if skip:
                    skip = False
                else:
                    total += 1
        return total

    def _set(self, aux: any):
        """ Initialize the date object values via auxiliary """
        if type(aux) is Date:
            self._month = Month(value=aux.month())
            self._day = Day(value=aux.day())
            self._year = Year(value=aux.year())
            return
        else:
            if type(aux) is tuple:
                self._month = Month(value=aux[0])
                self._day = Day(value=aux[1])
                self._year = Year(value=aux[2])
                return

            if type(aux) is str:
                _date_set: list = []
                if aux.__contains__('-'):
                    _date_set = aux.split('-')
                elif aux.__contains__('/'):
                    _date_set = aux.split('/')
                self._month = Month(value=_date_set[0])
                self._day = Day(value=_date_set[1])
                self._year = Year(value=_date_set[2])
                return

            if not type(aux) is datetime:
                if aux is datetime:
                    raise TypeError(
                        'Auxiliary date input must be provided as datetime.now()'
                    )
                raise TypeError(
                    'Invalid auxiliary date input, must be datetime, Date, tuple or str object'
                )

            _date_set: list = aux.strftime('%m-%d-%Y').split('-')
            self._month = Month(value=_date_set[0])
            self._day = Day(value=_date_set[1])
            self._year = Year(value=_date_set[2])
