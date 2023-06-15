
""" FLUX Runtime-Engine Console Manager """


#   MODULE IMPORTS
from flxr import *


#   MODULE CLASSES
class FlxrConsoleManager:

    _HANDLE: str = 'fw-console'

    def __init__(self, hfw: any, svc: any) -> None:
        """
        Framework console manager

        :param hfw: Hosting framework
        :param svc: Hosting framework services
        """

        self.__hfw = fw_obj(hfw)
        self.__S = svc

        self.__console_log: FWConsoleDatabase = FWConsoleDatabase()

        self._refresh: float = 0.15
        self._index: int = 0
        self._run: bool = False
        self._pause: bool = False
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
            while (len(self.__console_log) > 0) and (self.__hfw.dev()):
                pass
            self._run = False
            self.__S(self)['jthr'](handle=self._HANDLE, stop=force)

    def pause(self) -> None:
        """ Pause the console output """
        self._pause = True

    def resume(self) -> None:
        """ Resume the console output """
        self._pause = False

    def queue_output(self, msg: str, pconfig: dict[str, any] = None, error: bool = False) -> None:
        """ Queue text for console output """
        self.__console_log.append(
            FWConsoleLogEntry(
                index=self._index,
                datetime=self.__S(self)['getDatetime'](),
                timeline=self.__S(self)['runtimeStr'](),
                error=error,
                pconfig=pconfig,
                msg=msg
            )
        )
        self._index += 1

    def _runnable(self) -> bool:
        """ Determines if the module
        has permission to execute """
        if self._run:
            return True
        self._status(False)
        return False

    def _mainloop(self) -> None:
        """ Console manager main loop """
        self._run = True
        self._update()
        self._status(True)
        while self._runnable():
            time.sleep(self._refresh)
            self._update()

    def _update(self) -> None:
        """ Update framework console """
        if (len(self.__console_log) > 0) and (not self._pause):
            len_snapshot: int = len(self.__console_log)

            while len_snapshot > 0:
                if self.__hfw.dev():
                    self.__console_log.get_next().print_entry()
                else:
                    self.__console_log.get_next()
                len_snapshot -= 1

    def _status(self, status: bool) -> None:
        """ Set the framework module status """
        self.__S(self)['sstat'](
            module=FlxrConsoleManager,
            status=status
        )

    def _inject_services(self) -> None:
        """ Inject the modules services """
        _injectables: list = [
            ('pauseConsole', self.pause, MED),
            ('resumeConsole', self.resume, ANY),
        ]
        for _new in _injectables:
            self.__S(self)['nsvc'](
                call=_new[0],
                cls=self,
                func=_new[1],
                clearance=_new[2]
            )
