
"""
Framework Thread Manager Module
"""


#   BUILT-IN IMPORTS
from threading import Thread


#   EXTERNAL IMPORTS
from flxr.common.core import DeployableFwm
from flxr.utility import FlxrThread
from flxr.constant import SvcVars


#   MODULE CLASS
class FlxrThreadManager(DeployableFwm):
    def __init__(self, hfw, core: bool) -> None:
        """ Framework thread manager """
        super().__init__(hfw=hfw, cls=FlxrThreadManager, core=core)
        self.__threads: dict[FlxrThread] = {}
        self.load_injector(
            load=[
                ('thrs', self.handles, SvcVars.LOW),
                ('nthr', self.new, SvcVars.MED),
                ('sthr', self.start, SvcVars.MED),
                ('jthr', self.join, SvcVars.MED),
                ('dthr', self.delete, SvcVars.MED),
                ('thrr', self.thread_running, SvcVars.MED),
            ]
        )
        self.inject_services()

    def handles(self) -> list[str]:
        """ Returns list of managed thread handles """
        return [handle for handle in self.__threads.keys()]

    def existing_handle(self, handle: str) -> bool:
        """ Returns true if provided handle exists """
        return handle in self.handles()

    def thread_running(self, handle: str) -> bool:
        """ Returns true if provided
        thread is running """
        if not self.existing_handle(handle):
            return False
        return self.__threads[handle].running()

    def start(self, handle: str) -> None:
        """ Start specified managed thread """
        if not self.existing_handle(handle):
            return
        if self.thread_running(handle):
            return
        self.console(msg=f"Starting '{handle}' thread...")
        self.__threads[handle].start()

    def new(self, handle: str, thread: Thread, **kwargs) -> None:
        """ Establish new managed thread """
        if self.existing_handle(handle):
            return
        self.console(msg=f"Creating '{handle}' thread...")
        self.__threads[handle] = FlxrThread(
            handle=handle,
            thread=thread
        )
        if kwargs.get('start', False) is True:
            self.start(handle)

    def delete(self, handle: str) -> None:
        """ Delete specified managed thread """
        # TODO: Setup thread manager delete behavior

    def join(self, handle: str, force: bool = False, **kwargs) -> None:
        """ Join the specified managed thread """
        # TODO: Setup thread manager join behavior

    def join_all(self, force: bool = False, **kwargs) -> None:
        """ Join all managed threads with main """
        # TODO: Setup thread manager join all behavior
