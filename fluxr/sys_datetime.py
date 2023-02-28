
""" FLUX Runtime-Engine Framework Datetime Manager """


#   MODULE IMPORTS
from fluxr import *


#   MODULE PACKAGE
__package__ = pkg_n()


#   MODULE CLASSES
class SystemDatetimeManager:
    def __init__(self, fw: any, svc_c: any):
        """ Framework datetime manager """
        self.__FW = fw_obj(fw)
        self.__S = svc_c

        self.__local_datetime: dict = {
            'sec': '',
            'min': '',
            'hr': '',
            'day': '',
            'month': '',
            'year': '',
            'phase': ''
        }
        self.__date: str = None
        self.__time: str = None
        self.RUN: bool = False
        self.__inject_services()
        return

    def start(self):
        """ Start datetime manager """
        self.__new_thread(
            handle='sys-datetime',
            thread=Thread(target=self.__datetime),
            start=True
        )
        return

    def current_date(self) -> str:
        """ Returns the current date """
        return

    def current_time(self) -> str:
        """ Returns the current time """
        return

    def __runnable(self) -> bool:
        """ Determines if the module
        has permission to execute """
        if self.RUN and self.__fw_active():
            return True
        else:
            return False

    def __datetime(self):
        """ Datetime manager main loop """
        self.RUN = True
        self.__out("Starting datetime module...")
        try:
            self.__update()
            self.__status(True)
            while self.__runnable():
                time.sleep(0.1)
                self.__update()
        except BaseException as Unknown:
            self.__status(False)
            self.__exc(self, Unknown, sys.exc_info(), unaccounted=True,
                       pointer='__datetime()')
            self.__out("An error occurred in the datetime main loop", error=True)
        finally:
            self.__status(False)
            self.__out("Datetime module stopped running")
            return

    def __update(self):
        """ Update datetime manager object """
        now: list = datetime.now().strftime('%S-%M-%I-%d-%m-%Y-%p').split('-')
        i: int = 0
        for point in self.__local_datetime:
            self.__local_datetime[point] = now[i]
            i += 1
        self.__date = str(
            f"{self.__get_point('month')}/{self.__get_point('day')}/{self.__get_point('year')}"
        )
        self.__time = str(
            f"{self.__get_point('hr')}:{self.__get_point('min')}:{self.__get_point('sec')} {self.__get_point('phase')}"
        )
        return

    def __get_point(self, point: str):
        """ Returns a point in time from local datetime object """
        return self.__local_datetime[point]

    @staticmethod
    def __convert_24_hr(hr: str):
        """ Convert 24-hr to 12-hr """
        return

    # FRAMEWORK SERVICE BOILER PLATE - lvl1
    def __inject_services(self):
        """ Add class functions to service provider """
        self.__new_service('date', self, self.current_date)
        self.__new_service('time', self, self.current_time)
        return

    def __out(self, text: str, **kwargs):
        """ Send text to the console """
        self.__S(self)['console'](text, **kwargs)
        return

    def __status(self, status: bool):
        """ Update the modules status """
        self.__S(self)['setstat'](self, status)
        return

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
