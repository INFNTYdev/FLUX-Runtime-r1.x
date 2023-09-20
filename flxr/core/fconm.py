
"""
Framework Console Manager Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
pass


#   EXTERNAL IMPORTS
from flxr.common.core import ThreadedFwm
from flxr.constant import SvcVars
from flxr.model import ConsoleEntry


#   MODULE CLASS
class FlxrConsoleManager(ThreadedFwm):
    def __init__(self, hfw) -> None:
        """ Framework console manager """
        super().__init__(hfw=hfw, cls=FlxrConsoleManager, handle='fwconsole')
        self.__index: int = 0
        self.__pause: bool = False
        self.__queue: list[ConsoleEntry] = []
        self.__local_log: dict[ConsoleEntry] = {}
        self.set_mainloop(func=self.__mainloop)
        self.set_poll(requestor=self, poll=0.15)
        self.to_service_injector(
            load=[
                ('pauseConsole', self.pause, SvcVars.MED),
                ('resumeConsole', self.resume, SvcVars.MED),
                ('consoleIndex', self.current_index, SvcVars.MED)
            ]
        )
        self.inject_services()

    def current_index(self) -> int:
        """ Returns current console log index """
        return self.__index

    def paused(self) -> bool:
        """ Returns true if
        console log is paused """
        return self.__pause is True

    def datetime(self) -> any:
        """ Returns the instantaneous datetime object """
        return self.hfw_service(svc='getDatetime')

    def runtime(self) -> str:
        """ Returns the instantaneous runtime """
        return f'{self.hfw_service(svc="runtimeStamp")}-{self.__index}'

    def __get_next_queued(self) -> ConsoleEntry:
        """ Returns next entry queued """
        _next: ConsoleEntry = self.__queue[0]
        del self.__queue[0]
        return _next

    def queue_output(self, **output) -> None:
        """ Queue text for console output """
        _record: ConsoleEntry = ConsoleEntry(
            index=self.__index,
            datetime=self.datetime(),
            timeline=self.runtime(),
            **output
        )
        self.__index += 1
        self.__local_log[self.runtime()] = _record
        if self.hfw().developer_mode():
            self.__queue.append(_record)

    def pause(self) -> None:
        """ Pause console output stream """
        self.__pause = True

    def resume(self) -> None:
        """ Resume console output stream """
        self.__pause = False

    def __disregard_next_queued(self) -> None:
        """ Disregard the next entry queued """
        if len(self.__queue) > 0:
            del self.__queue[0]

    def __mainloop(self) -> None:
        """ Console manager module update """
        if (len(self.__queue) > 0) and (not self.__pause):
            _len_snapshot: int = len(self.__queue)
            while _len_snapshot > 0:
                if self.hfw().developer_mode():
                    self.__get_next_queued().print_entry()
                else:
                    self.__disregard_next_queued()
                _len_snapshot -= 1
            self.acknowledge_update()
