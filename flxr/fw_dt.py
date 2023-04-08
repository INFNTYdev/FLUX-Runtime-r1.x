
""" Framework datetime module """


# MODULE IMPORTS
from flxr import *

# MODULE PACKAGE
__package__ = pkg_n()


# MODULE CLASSES
class FlxrDatetime:
    def __init__(self, fw: any, svc: any):
        """
        Runtime-Engine datetime

        :param fw: Hosting framework
        :param svc: Framework service call
        """

        self.__FW = fw_obj(fw)
        self.__S = svc
        self._handle: str = 'fw-datetime'

        self.__local_datetime: dict = {
            'sec': None,
            'min': None,
            'hr': None,
            'day': None,
            'month': None,
            'year': None,
            'phase': None
        }
        self._date: str = None
        self._time: str = None
        self._last: list = None
        self._run: bool = False
        self._inject_services()

    def start_module(self):
        """ Start framework module """
        self.__S(self)['nthr'](
            handle=self._handle,
            thread=Thread(target=self.__datetime),
            start=True
        )

    def stop_module(self, force: bool = None):
        """ Stop framework module """
        self._run = False
        self.__S(self)['jthr'](handle=self._handle, stop=force)

    def current_date(self) -> str:
        """ Returns the current date """
        return self._date

    def current_time(self) -> str:
        """ Returns the current time """
        return self._time

    def _runnable(self) -> bool:
        """ Determines if the module
        has permission to execute """
        if self._run:
            return True
        self._status(False)
        return False

    def __datetime(self):
        """ Datetime module main loop """
        self._run = True
        self.__update()
        self._status(True)
        while self._runnable():
            time.sleep(0.1)
            self.__update()

    def __update(self):
        """ Update datetime module """
        now: list = self._now()
        if now != self._last:
            if self._consistent(now):
                self._last = []
                for point in self.__local_datetime.keys():
                    self.__local_datetime[point] = now[len(self._last)]
                    self._last.append(now[len(self._last)])
                self._date = str(
                    f"{self._point('month')}/{self._point('day')}/{self._point('year')}"
                )
                self._time = str(
                    f"{self._point('hr')}:{self._point('min')}:{self._point('sec')} {self._point('phase')}"
                )
            else:
                pass

    def _point(self, point: str) -> str:
        """ Returns a point in time from local datetime """
        return self.__local_datetime[point]

    def _consistent(self, now: list) -> bool:
        """ Determines if the updated time pattern is consistent """
        consistent: bool = True
        index_map: dict = {
            'sec': 0,
            'min': 1,
            'hr': 2,
            'day': 3,
            'month': 4
        }
        for segment, _value in self.__local_datetime.items():
            if segment != 'year':
                if self.__local_datetime[segment] != now[index_map[segment]]:
                    if self.__local_datetime[segment] is None:
                        return True
                    if (int(self.__local_datetime[segment]) == 59) and (int(now[index_map[segment]]) == 0):
                        pass
                    elif int(self.__local_datetime[segment])+1 == int(now[index_map[segment]]):
                        pass
                    else:
                        return False
            else:
                break
        return consistent

    def _inject_services(self):
        """ Inject datetime services into distributor """
        injectables: list = [
            ('date', FlxrDatetime, self.current_date),
            ('time', FlxrDatetime, self.current_time),
        ]
        for new in injectables:
            self.__S(self)['nsvc'](
                call=new[0],
                cls=new[1],
                func=new[2],
            )

    @staticmethod
    def _now() -> list:
        """ Retrieves the systems current datetime """
        return datetime.now().strftime('%S-%M-%I-%d-%m-%Y-%p').split('-')

    @staticmethod
    def _system_date() -> list:
        """ Retrieves the systems current date """
        return datetime.now().strftime('%d-%m-%Y').split('-')

    @staticmethod
    def _system_time() -> list:
        """ Retrieves the systems current time """
        return datetime.now().strftime('%S-%M-%I-%p').split('-')

    def _status(self, status: bool):
        """ Set the modules status """
        self.__S(self)['sstat'](
            module=FlxrDatetime,
            active=status
        )
