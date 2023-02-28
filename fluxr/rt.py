
""" Runtime Clock """


#   MODULE IMPORTS
from fluxr import *


#   MODULE PACKAGE
__package__ = pkg_n()


#   MODULE CLASSES
class RuntimeClock:
    def __init__(self):
        """ Runtime clock """
        self.__runtime: dict = {
            's': 0,
            'm': 0,
            'h': 0,
            'd': 0,
        }
        self.__host: Thread = None
        self.__run: bool = False
        return

    def resume_from(self, origin: list):
        """ Set the runtime clock to an intial value """
        if (not self.__run) and (self.__empty()):
            i: int = 0
            for point in self.__runtime.keys():
                if len(origin) > i:
                    self.__runtime[point] = origin[i]
                else:
                    break
                i += 1
        return

    def start(self, **kwargs):
        """ Start runtime clock """
        if ('with' in kwargs) and (type(kwargs.get('with')) is list):
            self.resume_from(kwargs.get('with'))
        self.__host = Thread(target=self.__clock)
        self.__host.start()
        return

    def override_start(self, fw: any):
        """ Override runtime clock start sequence """
        if fw_obj(fw) is not None:
            self.__clock()

    def runtime(self) -> str:
        """ Returns the current runtime """
        if self.get_point('d') == 0:
            return str(
                f"{self.__format_integer(self.get_point('h'))}:"
                f"{self.__format_integer(self.get_point('m'))}:"
                f"{self.__format_integer(self.get_point('s'))}"
            )
        return str(
            f"{self.__format_integer(self.get_point('d'))}:"
            f"{self.__format_integer(self.get_point('h'))}:"
            f"{self.__format_integer(self.get_point('m'))}:"
            f"{self.__format_integer(self.get_point('s'))}"
        )

    def get_point(self, point: str) -> str:
        """ Returns a point in time from runtime clock """
        return self.__runtime[point]

    def stop(self):
        """ Stop runtime clock """
        self.__run = False
        return

    @staticmethod
    def __format_integer(integer: int) -> str:
        """ Format time integer value to string """
        if integer > 9:
            return str(integer)
        return f'0{str(integer)}'

    def __update(self):
        """ Update the runtime clock object """
        self.__runtime['s'] += 1
        if self.__runtime['s'] == 60:
            self.__runtime['m'] += 1
            self.__runtime['s'] = 0
        if self.__runtime['m'] == 60:
            self.__runtime['h'] += 1
            self.__runtime['m'] = 0
        if self.__runtime['h'] == 24:
            self.__runtime['d'] += 1
            self.__runtime['h'] = 0
        return

    def __clock(self):
        """ Runtime clock main loop """
        self.__run = True
        while self.__run:
            time.sleep(1)
            self.__update()
        return

    def __empty(self) -> bool:
        """ Determines if the runtime clock is at 0 """
        for point in self.__runtime.keys():
            if self.__runtime[point] != 0:
                return False
        return True
