
"""
Deployable FLUX Framework Dependant Module
"""


#   BUILT-IN IMPORTS
from threading import Thread
from typing import Callable
import time


#   EXTERNAL IMPORTS
from .dfwm import DeployableFwm
from flxr.common.protocols import Flux
from simplydt import simplydatetime, DateTime


#   MODULE CLASS
class ThreadedFwm(DeployableFwm):
    def __init__(self, hfw: Flux, cls: type, handle: str, core: bool) -> None:
        """ Base threaded deployable
        FLUX runtime framework module """
        super().__init__(hfw=hfw, cls=cls, core=core)
        self.__run: bool = False
        self.__handle: str = str(handle)
        self.__refresh: list[float] = []
        self.__mainloop: Callable = None
        self.__last_update: DateTime = None

    @staticmethod
    def threaded() -> bool: return True

    def is_alive(self) -> bool:
        """ Returns true if module
        thread is running """
        return self.__run

    def has_mainloop(self) -> bool:
        """ Returns true if a mainloop
        has been set by module """
        return self.__mainloop is not None

    def get_mainloop(self) -> Callable:
        """ Returns threaded module
        loop function """
        return self.__mainloop

    def runnable(self) -> bool:
        """ Returns true if framework
        module is runnable """
        if not self.__run:
            self.set_status(False)
            return False
        elif self.hfw.active() is not True:
            self.set_status(False)
            return False
        elif self.status() is not True:
            return False
        return True

    def poll_rate(self) -> float:
        """ Returns module threading poll rate """
        return self.__refresh[-1]

    def last_update(self) -> DateTime:
        """ Returns module thread last
        update datetime object """
        return self.__last_update

    def set_mainloop(self, func) -> None:
        """ Set threaded module main loop """
        if not callable(func):
            return
        self.__mainloop = func

    def set_poll(self, requestor, poll: float) -> None:
        """ Set threaded module polling rate """
        if requestor is self:
            self.__refresh.append(float(poll))

    def reset_poll(self) -> None:
        """ Reset threaded module poll rate """
        self.__refresh = [self.__refresh[0]]

    def start_module(self) -> None:
        """ Start framework module thread """
        if not self.has_mainloop():
            return
        if self.is_alive():
            return
        self.hfw_service(
            svc='nthr',
            handle=self.__handle,
            thread=Thread(target=self.__execute_loop),
            start=True
        )

    def stop_module(self) -> None:
        """ Stop framework module thread """
        if not self.is_alive():
            return
        self.console(msg=f"Stopping {self.fwm_name()} module...")
        self.__run = False

    def acknowledge_update(self) -> None:
        """ Update module 'last updated' datetime """
        self.__last_update = simplydatetime.now()

    @staticmethod
    def wait(secs: float) -> None: time.sleep(secs)

    def __execute_loop(self) -> None:
        """ Threaded module host loop """
        self.__run = True
        self.acknowledge_update()
        self.set_status(True)
        while self.runnable():
            self.__mainloop()
            self.wait(self.poll_rate())
