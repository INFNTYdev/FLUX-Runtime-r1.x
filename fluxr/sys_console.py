
""" FLUX Runtime-Engine Framework Console Manager """


#   MODULE IMPORTS
from fluxr import *


#   MODULE PACKAGE
__package__ = pkg_n()


#   MODULE CLASSES
class ConsoleQueueEntry:
    def __init__(self, **kwargs):
        """ Console queue entry """
        self.__index: int = kwargs.get('index')
        self.__text: str = kwargs.get('text')
        self.__print_config: dict = kwargs.get('p_config')
        return

    def queue_text(self) -> str:
        """ Returns the queued items text """
        return self.__text

    def get_index(self) -> int:
        """ Returns the index of the queued item """
        return self.__index

    def get_config(self) -> dict:
        """ Returns the queued items print configuration """
        return self.__print_config


class ConsoleLogEntry:
    def __init__(self, **kwargs):
        """ Console log entry """
        self.__index: int = kwargs.get('index')
        self.__date: str = kwargs.get('date')
        self.__time: str = kwargs.get('time')
        self.__runtime: str = kwargs.get('rt')
        self.__is_error: bool = kwargs.get('is_error')
        self.__text: str = kwargs.get('text')
        return

    def get_index(self) -> int:
        """ Returns the index of the logged item """
        return self.__index

    def log_date(self) -> str:
        """ Returns the logged items date """
        return self.__date

    def log_time(self) -> str:
        """ Returns the logged items time """
        return self.__time

    def log_rt(self) -> str:
        """ Returns the logged items runtime """
        return self.__runtime

    def error_log(self) -> bool:
        """ Determines if the logged item is an error """
        return self.__is_error

    def log_text(self) -> str:
        """ Returns the logged items text """
        return self.__text


class ConsoleLog:
    def __init__(self, host: any):
        """ Framework console log """
        self.__H = host
        self.__console_log: dict = {}
        self.__console_queue: dict = {}
        self.__index: int = 0
        return

    def log(self, text: str, p_config: dict):
        """ Log console output to console log and queue """
        self.__console_log[self.__index] = ConsoleLogEntry(
            index=self.__index,
            date=self.__H.d_call(self, 'date'),
            time=self.__H.d_call(self, 'time'),
            rt=self.__H.d_call(self, 'rt'),
            is_error=p_config.get('is_error'),
            text=text
        )
        if self.__H.do_print():
            self.__console_queue[self.__index] = ConsoleQueueEntry(
                text=text,
                p_config=p_config
            )
        self.__index += 1
        return

    def queue_length(self) -> int:
        """ Returns the queues current length """
        return len(self.__console_queue)

    def log_length(self) -> int:
        """ Returns the current length of the log """
        return len(self.__console_log.keys())

    def log_index(self) -> int:
        """ Returns the logs current index """
        return self.__index

    def log_at(self, index: int) -> ConsoleLogEntry:
        """ Returns a logged item at the given index """
        return self.__console_log[index]

    def get_head(self) -> ConsoleQueueEntry:
        """ Returns the current queued item in line """
        return self.__console_queue[list(self.__console_queue.keys())[0]]

    def delete_head(self):
        """ Deletes the current queued item in line """
        del self.__console_queue[list(self.__console_queue.keys())[0]]
        return


class SystemConsoleManager:
    def __init__(self, fw: any, svc_c: any):
        """ Framework console manager """
        self.__FW = fw_obj(fw)
        self.__S = svc_c

        self.__console: ConsoleLog = ConsoleLog(self)
        self.__force_root: bool = False
        self.__refresh: float = 0.25
        self.__pause: bool = False
        self.RUN: bool = False
        self.__inject_services()
        return

    def start(self):
        """ Start framework console manager """
        self.__new_thread(
            handle='sys_console',
            thread=Thread(target=self.__queue),
            start=True
        )
        return

    def console_out(self, **kwargs):
        """ Send text to the console manager log for output """
        p_config: dict = {
            'is_error': kwargs.get('error', False),
            'skip_line': kwargs.get('skip', bool(self.__console.log_index() == 0)),
            'prefix': kwargs.get('prefix', ''),
            'seperator': kwargs.get('sepr', '|'),
            'show_date': kwargs.get('c_date', True),
            'show_time': kwargs.get('c_time', True)
        }
        self.__console.log(text=kwargs.get('text'), p_config=p_config)
        return

    def d_call(self, requestor: any, call: any, **kwargs) -> any:
        """ Provide framework services to dependant object """
        if requestor is self.__console:
            return self.__S(self)[call](**kwargs)
        return

    def do_print(self) -> bool:
        """ Determines if text should be sent to console """
        return self.__FW.dev

    def __runnable(self) -> bool:
        """ Determines if the module
        has permission to execute """
        if self.RUN and self.__fw_active():
            return True
        else:
            return False

    def __queue(self):
        """ Console queue main loop """
        self.RUN = True
        self.__status(True)
        try:
            while self.__runnable():
                time.sleep(self.__refresh)
                if (not self.__pause) and (self.do_print()):
                    self.__process_queue()
        except BaseException as Unknown:
            self.__status(False)
            self.__exc(self, Unknown, sys.exc_info(), unaccounted=True,
                       pointer='__queue()')
            self.__root_out("An error occurred in the console manager queue main loop", error=True)
        finally:
            self.__status(False)
            self.__root_out("Console manager queue has stopped running")
            return

    def __process_queue(self):
        """ Process and empty console queue """
        if (self.__console.queue_length() > 0) and (not self.__force_root):
            len_snapshot: int = self.__console.queue_length()
            for i in range(0, len_snapshot):
                self.__master_out(self.__console.get_head())
                self.__console.delete_head()
        elif self.__force_root:
            len_snapshot: int = self.__console.queue_length()
            for i in range(0, len_snapshot):
                self.__master_root_out(self.__console.get_head())
                self.__console.delete_head()
        return

    def __master_out(self, e: ConsoleQueueEntry):
        """ Master console output """
        conf: dict = e.get_config()
        __print_str: str = f"{conf['prefix']} >  "
        if conf['show_date']:
            __print_str += f"{self.__console.log_at(e.get_index()).log_date()} "
        else:
            __print_str += (' '*11)
        if conf['show_time']:
            __print_str += f"{self.__console.log_at(e.get_index()).log_time()} "
        else:
            __print_str += (' '*12)
        __print_str += conf['seperator']+'  '
        if conf['is_error']:
            __print_str += '[ ERROR ] : '
        __print_str += e.queue_text()
        if conf['skip_line']:
            __print_str = '\n'+__print_str
        print(__print_str)
        return

    def __master_root_out(self, e: ConsoleQueueEntry):
        """ Master root console output """
        self.__root_out(
            text=e.queue_text(),
            skip=e.get_config()['skip_line'],
            error=e.get_config()['is_error']
        )
        return

    # FRAMEWORK SERVICE BOILER PLATE - lvl3
    def __inject_services(self):
        """ Add class functions to service provider """
        pass

    def __root_out(self, text: str, **kwargs):
        """ Send text to the console """
        self.__S(self)['console'](text, root=True, **kwargs)
        return

    def __status(self, status: bool):
        """ Update the modules status """
        self.__S(self)['setstat'](self, status)
        return

    def __date(self) -> str:
        """ Returns the current date """
        return self.__S(self)['date']()

    def __time(self) -> str:
        """ Returns the current time """
        return self.__S(self)['time']()

    def __runtime(self) -> str:
        """ Returns the current runtime """
        return self.__S(self)['rt']()

    def __fw_stable(self) -> bool:
        """ Determines if required system modules are active """
        return self.__S(self)['corestat']()

    def __fw_active(self) -> bool:
        """ Returns frameworks run status """
        return self.__S(self)['runstat']()

    def __new_service(self, call: str, cls: any, func: any, **kwargs):
        """ Add a function reference to the service provider """
        self.__S(self)['nsvc'](call, cls, func, **kwargs)
        return

    def __threads(self) -> list:
        """ Returns a list of stored thread handles """
        return self.__S(self)['threads']()

    def __new_thread(self, handle: str, thread: Thread, **kwargs):
        """ Establish new thread in thread host """
        self.__S(self)['nthread'](handle, thread, **kwargs)
        return

    def __delete_thread(self, handle: str):
        """ Delete requested thread """
        self.__S(self)['dthread'](handle)
        return

    def __exc(self, cls: any, exc_o: any, exc_info: tuple, **kwargs):
        """ Handle system raised exceptions """
        self.__S(self)['exc'](cls, exc_o, exc_info, **kwargs)
        return
