
""" FLUX Runtime-Engine Datetime Manager """


#   MODULE IMPORTS
from flxr import *


#   MODULE CLASSES
class FlxrDatetimeManager:

    _HANDLE: str = 'fw-datetime'

    def __init__(self, hfw: any, svc: any) -> None:
        """
        Framework datetime manager
        
        :param hfw: Hosting framework
        :param svc: Hosting framework services
        """

        self.__hfw = fw_obj(hfw)
        self.__S = svc

        self._refresh: float = 0.2
        self._run: bool = False
        self.__datetime: DateTime = None
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

    def current_date(self) -> str:
        """ Returns the current date """
        return self.__datetime.date()

    def current_time(self, hformat: int = 12) -> str:
        """ Returns the current time """
        return self.__datetime.time(hformat=hformat)

    def get_date(self) -> Date:
        """ Returns the instantaneous date object """
        return self.__datetime.get_date()

    def get_time(self) -> Time:
        """ Returns the instantaneous time object """
        return self.__datetime.get_time()

    def get_datetime(self) -> DateTime:
        """ Returns the instantaneous datetime object """
        return self.__datetime

    def _runnable(self) -> bool:
        """ Determines if the module
        has permission to execute """
        if self._run and self.__hfw.running():
            return True
        self._status(False)
        return False

    def _mainloop(self) -> None:
        """ Datetime manager main loop """
        self._run = True
        self._update()
        self._status(True)
        while self._runnable():
            time.sleep(self._refresh)
            self._update()

    def _update(self) -> None:
        """ Update datetime """
        self.__datetime = simplydatetime.now()

    def _status(self, status: bool) -> None:
        """ Set the framework module status """
        self.__S(self)['sstat'](
            module=FlxrDatetimeManager,
            status=status
        )

    def _inject_services(self) -> None:
        """ Inject the modules services """
        _injectables: list = [
            ('date', self.current_date, ANY),
            ('time', self.current_time, ANY),
            ('getDate', self.get_date, ANY),
            ('getTime', self.get_time, ANY),
            ('getDatetime', self.get_datetime, ANY),
        ]
        for _new in _injectables:
            self.__S(self)['nsvc'](
                call=_new[0],
                cls=self,
                func=_new[1],
                clearance=_new[2]
            )
