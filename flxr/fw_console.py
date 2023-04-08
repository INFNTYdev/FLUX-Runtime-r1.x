
""" Framework console module """


# MODULE IMPORTS
from flxr import *

# MODULE PACKAGE
__package__ = pkg_n()


# MODULE CLASSES
class QueueEntry:
    def __init__(self, complete: any, instructors: any, **kwargs):
        """ Console queue entry """
        self._complete = complete
        self._instructors: dict = instructors
        self._index: int = kwargs.get('index')
        self.__text: str = kwargs.get('text')
        self._print_config: dict = kwargs.get('pconfig')

    def index(self) -> int:
        """ Returns the index of the linked log """
        return self._index

    def printe(self):
        """ Print the queued entry """
        __print_str: str = f"{self._print_config['prefix']} >  "
        if self._print_config['show_date']:
            __print_str += f"{self._instructors['date']()} "
        else:
            __print_str += (' '*11)
        if self._print_config['show_time']:
            __print_str += f"{self._instructors['time']()} "
        else:
            __print_str += (' '*12)
        __print_str += self._print_config['seperator']+'  '
        if self._print_config['error_msg']:
            __print_str += '[ ERROR ] : '
        __print_str += self.__text
        if self._print_config['skip_line']:
            __print_str = '\n'+__print_str
        print(__print_str)
        self._complete(self._index)


class LogEntry:
    def __init__(self, **kwargs):
        """ Console log entry """
        self._index: int = kwargs.get('index')
        self._date: str = kwargs.get('date')
        self._time: str = kwargs.get('time')
        self._runtime: str = kwargs.get('runtime')
        self._is_error: bool = kwargs.get('error_msg')
        self.__text: str = kwargs.get('text')

    def index(self) -> int:
        """ Returns the log index """
        return self._index

    def date(self) -> str:
        """ Returns the log date """
        return self._date

    def time(self) -> str:
        """ Returns the log time """
        return self._time

    def runtime(self) -> str:
        """ Returns the log runtime """
        return self._runtime

    def error_msg(self) -> bool:
        """ Returns the log 'is error' status """
        return self._is_error

    def text(self) -> str:
        """ Returns the log text """
        return self.__text


class ConsoleLog:
    def __init__(self, instructors: dict):
        """ Console log """
        self._instructors: dict = instructors
        self.__console_log: dict = {}
        self.__print_queue: dict = {}
        self._index: int = 0

    def log(self, text: str, pconfig: dict):
        """ Log console output to console log """
        self.__console_log[self._index] = LogEntry(
            index=self._index,
            date=self._instructors['date'](),
            time=self._instructors['time'](),
            runtime=self._instructors['runtime'](),
            error_msg=pconfig['error_msg'],
            text=text
        )
        if self._instructors['print_enabled']() is True:
            self.__print_queue[self._index] = QueueEntry(
                complete=self._unqueue,
                instructors=self._instructors,
                index=self._index,
                text=text,
                pconfig=pconfig
            )
        self._index += 1

    def get_next(self) -> QueueEntry:
        """ Returns the next print entry in line """
        low: int = list(self.__print_queue.keys())[-1]
        for index, _entry in self.__print_queue.items():
            return _entry

    def queue_length(self) -> int:
        """ Returns the print queues current length """
        return len(self.__print_queue)

    def log_length(self) -> int:
        """ Returns the console logs current length """
        return len(self.__console_log)

    def log_index(self) -> int:
        """ Returns the console logs current index """
        return self._index

    def _unqueue(self, index: int):
        """ Remove a queued console entry """
        del self.__print_queue[index]


class FlxrConsoleManager:
    def __init__(self, fw: any, svc: any):
        """
        Runtime-engine runtime clock

        :param fw: Hosting framework
        :param svc: Framework service call
        """

        self.__FW = fw_obj(fw)
        self.__S = svc
        self._handle: str = 'fw-consl'

        self.__console_log: ConsoleLog = ConsoleLog(instructors=self._dependant_instructors())
        self._force_root: bool = False
        self._refresh: float = 0.25
        self._pause: bool = False
        self._run: bool = False
        self._inject_services()

    def start_module(self):
        """ Start framework module """
        self.__S(self)['nthr'](
            handle=self._handle,
            thread=Thread(target=self.__queue),
            start=True
        )

    def pause(self):
        """ Pause the console queue output """
        self._pause = True

    def resume(self):
        """ Resume the console queue output """
        self._pause = False

    def stop_module(self, force: bool = None):
        """ Stop framework module """
        self._run = False
        self.__S(self)['jthr'](handle=self._handle, stop=force)

    def console_out(self, text: str, **kwargs):
        """ Send text to the console """
        pconfig: dict = {
            'error_msg': kwargs.get('error', False),
            'skip_line': kwargs.get('skip', False),
            'prefix': kwargs.get('prefix', ''),
            'seperator': kwargs.get('seperator', '|'),
            'show_date': kwargs.get('show_date', True),
            'show_time': kwargs.get('show_time', True)
        }
        self.__console_log.log(text=text, pconfig=pconfig)

    def _runnable(self) -> bool:
        """ Determines if the module
        has permission to execute """
        if self._run:
            return True
        self._status(False)
        return False

    def __queue(self):
        """ Console queue main loop """
        self._run = True
        self._status(True)
        while self._runnable():
            time.sleep(self._refresh)
            if not self._pause:
                self.__process_queue()

    def __process_queue(self):
        """ Process and empty queue """
        if (self.__console_log.queue_length() > 0) and (not self._force_root):
            len_snapshot: int = self.__console_log.queue_length()
            for i in range(0, len_snapshot):
                self.__console_log.get_next().printe()
        elif (self.__console_log.queue_length() > 0) and self._force_root:
            pass

    def _do_print(self) -> bool:
        """ Determines if text should be printed to console """
        return self.__FW.dev_mode()

    def _dependant_instructors(self) -> dict:
        """ Returns the dependant instructors """
        instructor: dict = {
            'print_enabled': self._do_print,
            'date': self.__S(self)['date'],
            'time': self.__S(self)['time'],
            'runtime': self.__S(self)['runtime']
        }
        return instructor

    def _inject_services(self):
        """ Inject console services into distributor """
        injectables: list = [
            ('pauseConsole', FlxrConsoleManager, self.pause),
            ('resumeConsole', FlxrConsoleManager, self.resume),
        ]
        for new in injectables:
            self.__S(self)['nsvc'](
                call=new[0],
                cls=new[1],
                func=new[2],
            )

    def _status(self, status: bool):
        """ Set the modules status """
        self.__S(self)['sstat'](
            module=FlxrConsoleManager,
            active=status
        )
