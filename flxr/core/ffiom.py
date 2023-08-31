
"""
Framework File I/O Manager Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
import os


#   EXTERNAL IMPORTS
from flxr.constant import SvcVars
from flxr.model import FlxrFileRef
from .fwmod import FrameworkModule


#   MODULE CLASS
class FlxrFileIOManager(FrameworkModule):
    def __init__(self, hfw) -> None:
        """ Framework file I/O manager """
        super().__init__(hfw=hfw, cls=FlxrFileIOManager)
        self._run: bool = False
        self._refresh: float = 1.3
        self._pause: bool = False
        self.__references: dict[FlxrFileRef] = {}
        self.to_service_injector(
            load=[
                ('pauseIO', self.pause, SvcVars.HIGH),
                ('resumeIO', self.resume, SvcVars.HIGH),
                ('files', self.files, SvcVars.LOW),
                ('linkFile', self.link, SvcVars.MED),
                ('unlinkFile', self.unlink, SvcVars.MED),
                ('getFile', self.get_file, SvcVars.MED),
                ('fileContents', self.get_contents, SvcVars.MED),
                ('read', self.read, SvcVars.LOW),
            ]
        )
        self.inject_services()

    def files(self) -> list[str]:
        """ Returns the list of referenced file names """
        return [_name for _name in self.__references.keys()]

    def existing_file(self, name: str) -> bool:
        """ Returns true if a file name exists
        in the file references """
        return name in [_name for _name in self.__references.keys()]

    def get_file(self, name: str) -> FlxrFileRef:
        """ Returns the specified fraamework file
        reference object """
        if not self.existing_file(name):
            self._invalid_file_name(fn=name, msg=f"No such file '{name}' linked to framework")
        if self.__references[name].protected():
            pass

        return self.__references[name]

    def get_contents(self, name: str) -> any:
        """ Returns the specified framework
        file contents """
        if not self.existing_file(name):
            self._invalid_file_name(fn=name, msg=f"No such file '{name}' linked to framework")
        if self.__references[name].protected():
            pass

        return self.__references[name].contents()

    def read(self) -> any:
        """ Returns the contents of the file
        at the specified path """
        pass

    def link(self, path: str, **kwargs) -> None:
        """ Link a file to the file I/O manager """
        if not self.valid_path(path):
            self._invalid_file_path(fp=path, msg="Could not locate path")
            return
        if not self.existing_system_file(path):
            self._invalid_file_path(fp=path, msg="Could not link requested file")
            return

        _file_ref: FlxrFileRef = FlxrFileRef(
            path=path,
            protected=kwargs.get('protect', False)
        )
        self.__references[_file_ref.name()] = _file_ref
        self.console(msg=f"Successfully linked '{_file_ref.name()}' - {round(_file_ref.size(), 2)}KB")

    def unlink(self, name: str, **kwargs) -> None:
        """ Unlink a file from the file I/O manager """
        if not self.existing_file(name):
            return
        if self.__references[name].protected():
            pass

        del self.__references[name]
        self.console(msg=f"Successfully unlinked '{name}' file")

    def pause(self) -> None:
        """ Pause the file I/O stream """
        self._pause = True

    def resume(self) -> None:
        """ Resume the file I/O stream """
        self._pause = False

    @staticmethod
    def valid_path(fp: str) -> bool:
        """ Return true if a path is valid """
        return os.path.exists(fp)

    @staticmethod
    def existing_system_file(fp: str) -> bool:
        """ Returns true if a system file exist """
        return os.path.isfile(fp)

    @staticmethod
    def abs_path(fp: str) -> str:
        """ Returns the absolute file path """
        return os.path.abspath(fp)

    def _invalid_file_path(self, fp: str, msg: str = None) -> None:
        """ Handle invalid file path """
        self.console(msg=f"Invalid file path '{fp}'", error=True)
        if msg is not None:
            self.console(msg=msg, error=True)

    def _invalid_file_name(self, fn: str, msg: str = None) -> None:
        """ Handle invalid file name """
        self.console(msg=f"Invalid file name '{fn}'", error=True)
        if msg is not None:
            self.console(msg=msg, error=True)

    def _runnable(self) -> bool:
        """ Returns true if the framework
        module has clearance to run """
        if not self._run:
            self.set_status(False)
            return False
        if not self.framework().is_alive():
            self.set_status(False)
            return False
        if not self.fw_svc(svc='getstat', module=FlxrFileIOManager):
            return False
        return True

    def _mainloop(self) -> None:
        """ File I/O manager main loop """
        self._run = True
        self.set_status(True)
        while self._runnable():
            self.wait(self._refresh)
            self._update()

    def _update(self) -> None:
        """ Update the file I/O manager module """
        if self._pause is True:
            return

        for _name, _file in self.__references.items():
            _file: FlxrFileRef
            if not _file.muted():
                _drag_time: tuple = _file.last_accessed().until(self.fw_svc('getDatetime'))
                if _drag_time[-2] >= 1:
                    _file.mute()
                    self.console(msg=f"Muted '{_name}'")

            if _file.out_of_date():
                self.console(msg=f"Updated '{_name}' file")
                _file.update()
                self.last_update_made(self.fw_svc(svc='getDatetime'))
