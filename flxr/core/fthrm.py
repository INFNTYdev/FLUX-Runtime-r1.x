
"""
Framework Thread Manager Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
from threading import Thread


#   EXTERNAL IMPORTS
from flxr.utility import FlxrThread
from flxr.constant import SvcVars
from .fwmod import FrameworkModule


#   MODULE CLASS
class FlxrThreadManager(FrameworkModule):
    def __init__(self, hfw) -> None:
        """ Framework thread manager """
        super().__init__(hfw=hfw, cls=FlxrThreadManager)
        self.__threads: dict[FlxrThread] = {}
        self.to_service_injector(
            load=[
                ('thrs', self.threads, SvcVars.LOW),
                ('nthr', self.new, SvcVars.MED),
                ('sthr', self.start, SvcVars.MED),
                ('jthr', self.join, SvcVars.MED),
                ('dthr', self.delete, SvcVars.MED),
                ('thrr', self.thread_running, SvcVars.MED),
            ]
        )
        self.inject_services()

    def threads(self) -> list[str]:
        """ Returns the list of managed thread handles """
        return [handle for handle in self.__threads.keys()]

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

    def start(self, handle: str) -> None:
        """ Start the specified managed thread """
        if not self.existing_handle(handle):
            return

        if self.thread_running(handle):
            return

        self.console(msg=f"Starting '{handle}' thread...")
        self.__threads[handle].start()

    def join(self, handle: str, force: bool = False, **kwargs) -> None:
        """ Join the specified managed thread """
        pass

    def join_all(self, force: bool = False, **kwargs) -> None:
        """ Join all managed threads with main """
        pass

    def delete(self, handle: str) -> None:
        """ Delete the specified managed thread """
        pass

    def existing_handle(self, handle: str) -> bool:
        """ Returns true if provided handle exists """
        return handle in self.__threads.keys()

    def thread_running(self, handle: str) -> bool:
        """ Returns true if the provided thread
        handle is running """
        if not self.existing_handle(handle):
            return False
        return self.__threads[handle].running()
