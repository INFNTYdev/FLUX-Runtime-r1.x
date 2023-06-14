
""" Framework Runtime Clock Module """

#   MODULE IMPORTS
from flxr import *


#   MODULE CLASSES
class FlxrRuntimeClock:

    _HANDLE: str = 'fw-rtclock'

    def __init__(self, hfw: any, svc: any) -> None:
        """
        Framework runtime clock

        :param hfw: Hosting framework
        :param svc: Hosting framework services
        """

        self.__hfw = fw_obj(hfw)
        self.__S = svc

        self._refresh: float = 0.1
        self._run: bool = False
        self.__origin: DateTime = simplydatetime.now()
        self.__runtime: tuple = None
        self._inject_services()

    def start_module(self) -> None:
        """ Start framework module """
        if not self._run:
            self.__S(self)['nthr'](
                handle=self._HANDLE,
                thread=Thread(target=self._mainloop),
                start=True
            )

    def stop_module(self, force: bool = False) -> None:
        """ Stop framework module """
        if self._run:
            self._run = False
            self.__S(self)['jthr'](handle=self._HANDLE, stop=force)

    def runtime(self) -> tuple[int, int, int, int, int]:
        """ Returns the runtime clock tuple (Ms, Ds, hrs, mins, secs) """
        return self.__runtime[1:]

    def runtime_str(self) -> str:
        """ Returns the runtime string """
        _rt: tuple = self.runtime()
        return f'{_rt[0]} Months, {_rt[1]} Days, {_rt[2]} Hours, {_rt[3]} Minutes, {_rt[4]} Seconds'

    def _runnable(self) -> bool:
        """ Determines if the module
        has permission to execute """
        if self._run and self.__hfw.running():
            return True
        self._status(False)
        return False

    def _mainloop(self) -> None:
        """ Runtime clock main loop """
        self._run = True
        self._update()
        self._status(True)
        while self._runnable():
            time.sleep(self._refresh)
            self._update()

    def _datetime(self) -> DateTime:
        """ Returns the current datetime """
        return self.__S(self)['getDatetime']()

    def _update(self) -> None:
        """ Update runtime """
        self.__runtime = self.__origin.until(self._datetime())

    def _status(self, status: bool) -> None:
        """ Set the framework module status """
        self.__S(self)['sstat'](
            module=FlxrRuntimeClock,
            status=status
        )

    def _inject_services(self) -> None:
        """ Inject the modules services """
        _injectables: list = [
            ('runtime', self.runtime, ANY),
            ('runtimeStr', self.runtime_str, ANY),
        ]
        for _new in _injectables:
            self.__S(self)['nsvc'](
                call=_new[0],
                cls=self,
                func=_new[1],
                clearance=_new[2]
            )
