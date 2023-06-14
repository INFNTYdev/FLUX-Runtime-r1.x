
""" FLUX Runtime-Engine File I/O Manager """


#   MODULE IMPORTS
from flxr import *


#   MODULE CLASSES
class FlxrFileIOManager:

    _HANDLE: str = 'fw-fileio'
    _DRAG_MINUTE_MAX: int = 1
    _DRAG_SECOND_MAX: int = 0

    def __init__(self, hfw: any, svc: any) -> None:
        """
        Framework file I/O manager

        :param hfw: Hosting framework
        :param svc: Hosting framework services
        """

        self.__hfw = fw_obj(hfw)
        self.__S = svc

        self._refresh: float = 0.5
        self._run: bool = False
        self._pause: bool = False
        self.__files: dict = {}
        self._inject_services()

    def start_module(self) -> None:
        """ Start framework module """
        if not self._run:
            self.__S(self)['nthr'](
                handle=self._HANDLE,
                thread=Thread(target=self._mainloop),
                start=True
            )

    def stop_module(self, force: bool = False) -> None:
        """ Stop framework module """
        if self._run:
            self._run = False
            self.__S(self)['jthr'](handle=self._HANDLE, stop=force)

    def pause(self) -> None:
        """ Pause the file I/O stream """
        self._pause = True

    def resume(self) -> None:
        """ Resume the file I/O stream """
        self._pause = False

    def files(self) -> list:
        """ Returns the list of files linked to the database """
        return self.__files.keys()

    def link(self, filepath: str, protected: bool = False) -> None:
        """ Link an existing file to the database """
        if not self.valid_file_path(filepath):
            self._invalid_file_path(fp=filepath, msg="Could not link requested file")
            return

        if not self.existing_file(filepath):
            self.__S(self)['console'](msg=f"No existing file at '{filepath}'", error=True)
            return

        _f: FWFile = FWFile(fp=filepath, protected=protected)
        self.__files[_f.name()] = _f
        self.__S(self)['console'](msg=f"Successfully linked '{filepath}'")

    def unlink(self, filename: str) -> bool:
        """ Unlink a file from the database """
        if filename not in self.files():
            self._invalid_file_name(fn=filename, msg=f"No such '{filename}' to unlink")
            return

        if self.__files[filename].protected():
            self.__S(self)['console'](msg=f"Cannot unlink protected file '{filename}'", error=True)
            return

        del self.__files[filename]
        self.__S(self)['console'](msg=f"Successfully unlinked '{filename}'")

    def get(self, filename: str) -> str:
        """ Returns the contents of linked file """
        if filename not in self.files():
            self._invalid_file_name(fn=filename, msg=f"No such file '{filename}' to retrieve")
            return

        return self.__files[filename].contents()

    def read(self, filepath: str) -> str:
        """ Returns the contents of a system file """
        if not self.valid_file_path(filepath):
            self._invalid_file_path(fp=filepath, msg="Could not read requested file")
            return

        if not self.existing_file(filepath):
            self.__S(self)['console'](msg=f"No existing file at '{filepath}'", error=True)
            return

        with open(file=self.abs_path(filepath), mode='r') as readable:
            _contents: str = readable.read()
            readable.close()
        return _contents

    def update(self, filename: str, contents: str, overwrite: bool = True) -> None:
        """ Write to the contents of a linked file """
        if filename not in self.files():
            self._invalid_file_name(fn=filename, msg=f"No such '{filename}' to update")
            return

        if self.__files[filename].protected():
            self.__S(self)['console'](msg=f"Cannot update protected file '{filename}'", error=True)
            return

        self.write(filepath=self.__files[filename].name(), contents=contents, overwrite=overwrite)

    def write(self, filepath: str, contents: str, overwrite: bool = True) -> None:
        """ Create or write to the contents of a system file """
        _contents: str = contents
        if self.existing_file(filepath) and not overwrite:
            _contents = f'{self.read(filepath)}\n{_contents}'

        with open(file=self.abs_path(filepath), mode='w+') as writable:
            writable.write(_contents)
            writable.close()

    @staticmethod
    def valid_file_path(fp: str) -> bool:
        """ Determines if a file path is valid """
        return os.path.exists(fp)

    @staticmethod
    def existing_file(fp: str) -> bool:
        """ Determines if a file exist """
        return os.path.isfile(fp)

    @staticmethod
    def abs_path(fp: str) -> str:
        """ Returns the absolute file path """
        return os.path.abspath(fp)

    def _runnable(self) -> bool:
        """ Determines if the module
        has permission to execute """
        if self._run and self.__hfw.running():
            return True
        self._status(False)
        return False

    def _mainloop(self) -> None:
        """ File I/O manager main loop """
        self._run = True
        self._update()
        self._status(True)
        while self._runnable():
            time.sleep(self._refresh)
            self._update()

    def _update(self) -> None:
        """ Update file database """
        if self._pause:
            return

        for _fn, __file in self.__files.items():
            if not __file.muted():
                _drag_time: tuple = __file.last_accessed().until(simplydatetime.now())
                if (_drag_time[4] >= self._DRAG_MINUTE_MAX) and (_drag_time[5] >= self._DRAG_SECOND_MAX):
                    self.__S(self)['console'](msg=f"Preserving '{_fn}' resource")
                    __file.mute()

            if __file.out_of_date():
                __file.update()
                self.__S(self)['console'](msg=f"Updated '{_fn}'")

    def _status(self, status: bool) -> None:
        """ Set the framework module status """
        self.__S(self)['sstat'](
            module=FlxrFileIOManager,
            status=status
        )

    def _invalid_file_path(self, fp: str, msg: str = None) -> None:
        """ Handle invalid file path """
        self.__S(self)['console'](msg=f"Invalid file path '{fp}'", error=True)
        if msg is not None:
            self.__S(self)['console'](msg=msg, error=True)

    def _invalid_file_name(self, fn: str, msg: str = None) -> None:
        """ Handle invalid file name """
        self.__S(self)['console'](msg=f"Invalid file name '{fn}'", error=True)
        if msg is not None:
            self.__S(self)['console'](msg=msg, error=True)

    def _inject_services(self) -> None:
        """ Inject the modules services """
        _injectables: list = [
            ('pauseIO', self.pause, MED),
            ('resumeIO', self.resume, ANY),
            ('files', self.files, LOW),
            ('linkFile', self.link, LOW),
            ('unlinkFile', self.unlink, MED),
            ('getFile', self.get, LOW),
            ('readFile', self.read, ANY),
            ('updateFile', self.update, LOW),
            ('writeFile', self.write, ANY),
        ]
        for _new in _injectables:
            self.__S(self)['nsvc'](
                call=_new[0],
                cls=self,
                func=_new[1],
                clearance=_new[2]
            )
