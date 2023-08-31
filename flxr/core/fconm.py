
"""
Framework Console Manager Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
pass


#   EXTERNAL IMPORTS
from flxr.constant import SvcVars
from flxr.model import ConsoleEntry
from .fwmod import FrameworkModule


#   MODULE CLASS
class FlxrConsoleManager(FrameworkModule):
    def __init__(self, hfw) -> None:
        """ Framework console manager """
        super().__init__(hfw=hfw, cls=FlxrConsoleManager)
        self._run: bool = False
        self._refresh: float = 0.15
        self._index: int = 0
        self._pause: bool = False
        self._queue: list[ConsoleEntry] = []
        self._local_log: dict[ConsoleEntry] = {}
        self.to_service_injector(
            load=[
                ('pauseConsole', self.pause, SvcVars.MED),
                ('resumeConsole', self.resume, SvcVars.MED),
                ('consoleIndex', self.current_index, SvcVars.MED)
            ]
        )
        self.inject_services()

    def queue_output(self, **output) -> None:
        """ Queue text for console output """
        _record: ConsoleEntry = ConsoleEntry(
            index=self._index,
            datetime=self._datetime(),
            timeline=self._runtime(),
            **output
        )
        self._index += 1
        self._local_log[self._runtime()] = _record
        if self.framework().dev_mode():
            self._queue.append(_record)

    def pause(self) -> None:
        """ Pause the console output stream """
        self._pause = True

    def resume(self) -> None:
        """ Resume the console output stream """
        self._pause = False

    def current_index(self) -> int:
        """ Returns the current console log index """
        return self._index

    def _datetime(self) -> any:
        """ Returns the instantaneous datetime object """
        return self.fw_svc(svc='getDatetime')

    def _runtime(self) -> str:
        """ Returns the instantaneous runtime """
        return f'-{self._index}'

    def _get_next_queued(self) -> ConsoleEntry:
        """ Returns the next entry queued """
        _next: ConsoleEntry = self._queue[0]
        del self._queue[0]
        return _next

    def _disregard_next_queued(self) -> None:
        """ Disregard the next entry queued """
        if len(self._queue) > 0:
            del self._queue[0]

    def _runnable(self) -> bool:
        """ Returns true if the framework
        module has clearance to run """
        if not self._run:
            self.set_status(False)
            return False
        if not self.framework().is_alive():
            self.set_status(False)
            return False
        if not self.fw_svc(svc='getstat', module=FlxrConsoleManager):
            return False
        return True

    def _mainloop(self) -> None:
        """ Console manager main loop """
        self._run = True
        self.set_status(True)
        while self._runnable():
            self.wait(self._refresh)
            self._update()

    def _update(self) -> None:
        """ Update the console manager module """
        if (len(self._queue) > 0) and (not self._pause):
            _len_snapshot: int = len(self._queue)
            while _len_snapshot > 0:
                if self.framework().dev_mode():
                    self._get_next_queued().print_entry()
                else:
                    self._disregard_next_queued()
                _len_snapshot -= 1
            self.last_update_made(self.fw_svc(svc='getDatetime'))
