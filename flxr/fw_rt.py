
""" Framework runtime clock module """


# MODULE IMPORTS
from flxr import *

# MODULE PACKAGE
__package__ = pkg_n()


# MODULE CLASSES
class FlxrRuntimeClock:
    def __init__(self, fw: any, svc: any):
        """
        Runtime-engine runtime clock

        :param fw: Hosting framework
        :param svc: Framework service call
        """

        self.__FW = fw_obj(fw)
        self.__S = svc
        self._handle: str = 'fw-rtc'

        self.__origin: dict = {
            'date': None,
            'time': None
        }
        self.__core_clock: int = None
        self._runtime: str = None
        self._run: bool = False
        self._inject_services()

    def start_module(self):
        """ Start framework module """
        self.__S(self)['nthr'](
            handle=self._handle,
            thread=Thread(target=self.__clock),
            start=True
        )

    def stop_module(self, force: bool = None):
        """ Stop framework module """
        self._run = False
        self.__S(self)['jthr'](handle=self._handle, stop=force)

    def current_runtime(self) -> str:
        """ Returns the current runtime """
        return self._runtime

    def _runnable(self) -> bool:
        """ Determines if the module
        has permission to execute """
        if self._run:
            return True
        self._status(False)
        return False

    def __clock(self):
        """ Runtime clock main loop """
        self._run = True
        self.__origin['date'] = self._current_date()
        self.__origin['time'] = self._current_time()
        self.__core_clock = 0
        self._status(True)
        while self._runnable():
            time.sleep(1)
            self.__core_clock += 1

    def _current_date(self) -> str:
        """ Returns the current date """
        return self.__S(self)['date']()

    def _current_time(self) -> str:
        """ Returns the current time """
        return self.__S(self)['time']()

    def _status(self, status: bool):
        """ Set the modules status """
        self.__S(self)['sstat'](
            module=FlxrRuntimeClock,
            active=status
        )

    def _inject_services(self):
        """ Inject runtime clock services into distributor """
        injectables: list = [
            ('runtime', FlxrRuntimeClock, self.current_runtime),
        ]
        for new in injectables:
            self.__S(self)['nsvc'](
                call=new[0],
                cls=new[1],
                func=new[2],
            )
