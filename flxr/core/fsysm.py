
"""
Framework System Manager Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
pass


#   EXTERNAL IMPORTS
from flxr.core import FlxrConsoleManager
from .fwmod import FrameworkModule


#   MODULE CLASS
class FlxrSystemManager(FrameworkModule):
    def __init__(self, hfw) -> None:
        """ Framework system manager """
        super().__init__(hfw=hfw, cls=FlxrSystemManager)
        self._run: bool = False
        self._refresh: float = 0.5

    def _runnable(self) -> bool:
        """ Returns true if the framework
        module has clearance to run """
        if not self._run:
            self.set_status(False)
            return False
        if not self.framework().is_alive():
            self.set_status(False)
            return False
        if not self.fw_svc(svc='getstat', module=FlxrSystemManager):
            return False
        return True

    def _mainloop(self) -> None:
        """ Framework manager main loop """
        self._run = True
        self.set_status(True)
        while self._runnable():
            self.wait(self._refresh)
            self._update()

    def _update(self) -> None:
        """ Update the framework manager module """
        for _type, __module in self.framework().asset_bus(self).items():
            self._conduct_module_analysis(_type, __module)
        self.last_update_made(self.fw_svc(svc='getDatetime'))

    def _conduct_module_analysis(self, module_type: type, _module: FrameworkModule) -> None:
        """ Conduct analysis on the provided
        framework module """
        if _module.threaded_module():
            self._conduct_thread_analysis(module_type, _module)
        pass

    def _conduct_thread_analysis(self, module_type: type, _module: FrameworkModule) -> None:
        """ Conduct analysis on threaded framework modules """
        #   WASTEFUL MONOPOLIZATION MITIGATION
        _update_drag: tuple = _module.last_updated().until(self.fw_svc(svc='getDatetime'))[-2:]
        if (_update_drag[1] >= 30) and (_module.polling_rate() < 2):
            if module_type != FlxrConsoleManager:
                self.console(msg=f"Adjusting {module_type.__name__} poll rate...")
                _module.set_poll(requestor=self, rate=3.0)
        elif ((_update_drag[1] <= 2) and (_update_drag[0] == 0)) and (_module.polling_rate() > 2):
            _module.reset_poll()
