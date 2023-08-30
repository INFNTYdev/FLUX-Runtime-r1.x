
"""
FLUX Runtime Framework File Reference Module
"""


#   THIRD-PARTY IMPORTS
pass


#   BUILT-IN IMPORTS
import os
import stat


#   EXTERNAL IMPORTS
from simplydt import simplydatetime, DateTime


#   MODULE CLASS
class FlxrFileRef:
    def __init__(self, path: str, protected: bool = False) -> None:
        """ Framework file reference object """
        self._path: str = None
        self._name: str = None
        self._type: str = None
        self._size: float = None
        self._contents: str = None
        self._last_modified: int = None
        self._last_accessed: DateTime = None
        self._protected: bool = protected
        self.__reference(path)

    def name(self) -> str:
        """ Returns the file name """
        return self._name

    def type(self) -> str:
        """ Returns the file extension """
        return self._type

    def size(self) -> float:
        """ Returns the file size in KB """
        return self._size

    def protected(self) -> bool:
        """ Returns true if the file has protection status """
        return self._protected

    def muted(self) -> bool:
        """ Returns true if the file contents are muted """
        return self._contents is None

    def out_of_date(self) -> bool:
        """ Returns true if the file metadata
        is out-of-date """
        return self._retrieve_last_modified() != self._last_modified

    def last_accessed(self) -> DateTime:
        """ Returns the last access datetime object """
        return self._last_accessed

    def contents(self, **kwargs) -> any:
        """ Returns the file contents """
        if not self._protected:
            if self._contents is None:
                self._contents = self._retrieve_contents()
            return self._contents

    def update(self) -> None:
        """ Update the file metadata """
        if self.out_of_date():
            self._size = self._retrieve_size()
            self._last_modified = self._retrieve_last_modified()
            if self._contents is not None:
                self._contents = self._retrieve_contents()

    def mute(self) -> None:
        """ Clears the file contents from memory """
        self._contents = None

    def _retrieve_size(self) -> float:
        """ Returns the updated file size in KB """
        return float(os.path.getsize(self._path)/1024)

    def _retrieve_contents(self) -> any:
        """ Returns the updated file contents """
        with open(self._path) as readable:
            _contents = readable.read()
            readable.close()
        self._last_accessed = simplydatetime.now()
        return _contents

    def _retrieve_last_modified(self) -> int:
        """ Returns the updated last modified stamp """
        return os.stat(self._path)[stat.ST_MTIME]

    def __reference(self, fp: str) -> None:
        """ Finalize the file reference attributes """
        if not os.path.exists(fp):
            raise ValueError(
                f"Invalid file reference path: '{fp}'"
            )
        self._path = os.path.abspath(fp)
        self._name = os.path.basename(self._path)
        self._type = self._name.split('.')[-1]
        self._size = self._retrieve_size()
        self._last_modified = self._retrieve_last_modified()
        self._last_accessed = simplydatetime.now()
