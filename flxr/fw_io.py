
""" Framework file I/O module """


# MODULE IMPORTS
from flxr import *

# MODULE PACKAGE
__package__ = pkg_n()


# MODULE CLASSES
class FileDatabase(dict):
    def __init__(self, host: any, console: any):
        """ File manager database """
        self.__H = host
        self.__console = console
        dict.__init__(self)
        self.__size: float = 0.

    def files(self, **kwargs) -> list:
        """ Return the list of file names in the registry """
        file_view: list = []
        for _filename, __file in self.items():
            if __file.protected():
                if kwargs.get('requestor') is self.__H:
                    file_view.append(_filename)
                else:
                    pass
            else:
                file_view.append(_filename)
        return file_view

    def file_count(self) -> int:
        """ Returns the amount of files currently stored """
        return len(self)

    def size(self) -> float:
        """ Return the current size of the database in KB """
        return self.__size

    def retrieve(self, filename: str, **kwargs) -> FWFile:
        """ Retrieve a file from the database by name """
        if self._existing_file(filename):
            if self[filename].protected():
                if kwargs.get('requestor') is self.__H:
                    return self[filename]
                else:
                    pass
            else:
                return self[filename]

    def read(self, filepath: str, protected: bool = False):
        """ Read a specified file into the database """
        if not self._existing_file_path(filepath):
            file: FWFile = FWFile(
                filepath=filepath,
                protected=protected
            )
            self[file.name()] = file
            self.__size += file.size()
            self.__console(text=f"Successfully linked '{file.name()}'")

    def drop(self, filename: str, **kwargs):
        """ Remove a file from the database """
        if self._existing_file(filename):
            if self[filename].protected():
                if kwargs.get('requestor') is self.__H:
                    return self[filename]
                else:
                    pass
            else:
                self.__size -= self[filename].size()
                self.__console(text=f"Dropping '{self[filename].name()}'...")
                del self[filename]

    def review(self, filepath: str) -> str:
        """ Return the contents of a file not stored """
        if not self._existing_file(filepath):
            with open(file=filepath) as readable:
                __contents: str = readable.read()
                readable.close()
            return __contents
        return 'Invalid Access'

    def _existing_file(self, filename: str) -> bool:
        """ Determines if a file exists in the database """
        return filename in self.keys()

    def _existing_file_path(self, filepath: str) -> bool:
        """ Determines if a file path exists in the database """
        for _filename, __file in self.items():
            if __file.is_path(filepath):
                return True
        return False


class FlxrFileIOManager:
    def __init__(self, fw: any, svc: any):
        """
        Runtime-engine file I/O manager

        :param fw: Hosting framework
        :param svc: Framework service call
        """

        self.__FW = fw_obj(fw)
        self.__S = svc
        self._handle: str = 'fw-io'

        self.__file_database: FileDatabase = FileDatabase(
            host=self,
            console=self.__S(self)['console']
        )
        self._refresh: float = 1.5
        self._run: bool = False
        self._secure_framework_files()
        self._inject_services()

    def start_module(self):
        """ Start framework module """
        self.__S(self)['nthr'](
            handle=self._handle,
            thread=Thread(target=self.__file_io),
            start=True
        )

    def stop_module(self, force: bool = None):
        """ Stop framework module """
        self._run = False
        self.__S(self)['jthr'](handle=self._handle, stop=force)

    def files(self, **kwargs) -> list:
        """ Return the list of file names in the registry """
        return self.__file_database.files(**kwargs)

    def retrieve(self, filename: str, **kwargs) -> FWFile:
        """ Retrieve a file from the database by name """
        return self.__file_database.retrieve(
            filename=filename,
            **kwargs
        )

    def read(self, filepath: str, protected: bool = False):
        """ Read a specified file into the database """
        self.__file_database.read(
            filepath=filepath,
            protected=protected
        )

    def drop(self, filename: str, **kwargs):
        """ Remove a file from the database """
        self.__file_database.drop(
            filename=filename,
            **kwargs
        )

    def review(self, filepath: str) -> str:
        """ Return the contents of a file not stored """
        return self.__file_database.review(filepath)

    def _runnable(self) -> bool:
        """ Determines if the module
        has permission to execute """
        if self._run:
            return True
        self._status(False)
        return False

    def __file_io(self):
        """ System file manager main loop """
        self._run = True
        self._status(True)
        while self._runnable():
            time.sleep(self._refresh)
            self.__evaluate_files()

    def __evaluate_files(self):
        """ Evaluate the databse files """
        for _filename, __file in self.__file_database.items():
            if __file.out_of_date() is True:
                __file.update()
                self.__S(self)['console'](text=f"Updated '{_filename}'")

    @staticmethod
    def get_abs_file_paths(directory_path: str):
        file_paths = []
        for root, dirs, files in os.walk(directory_path):
            dirs[:] = [d for d in dirs if d != '__pycache__']
            for file in files:
                file_path = os.path.join(root, file)
                file_paths.append(file_path)
        return file_paths

    def _secure_framework_files(self):
        """ Secure the framework system files """
        for __p in self.get_abs_file_paths(pkg_dir()):
            self.read(
                filepath=__p,
                protected=True
            )

    def _inject_services(self):
        """ Inject file I/O services into distributor """
        injectables: list = [
            ('files', FileDatabase, self.files, LOW),
            ('getFile', FileDatabase, self.retrieve, MED),
            ('newFile', FileDatabase, self.read, LOW),
            ('dropFile', FileDatabase, self.drop, MED),
            ('readFile', FileDatabase, self.review, LOW),
        ]
        for new in injectables:
            self.__S(self)['nsvc'](
                call=new[0],
                cls=new[1],
                func=new[2],
                clearance=new[3]
            )

    def _status(self, status: bool):
        """ Set the modules status """
        self.__S(self)['sstat'](
            module=FlxrFileIOManager,
            active=status
        )
