
""" Framework File Object """


#   MODULE IMPORTS
import os
import stat
from flxr import *


#   MODULE CONSTANTS
EXT_TYPES: dict = {
    'txt': 'Text Document',
    'py': 'Python File',
}


#   MODULE CLASSES
class FWFile:
    def __init__(self, fp: str, protected: bool = False) -> None:
        """
        FLUX framework file
        
        :param fp: File path
        :param protected: File protection status
        """

        self._path: str = None
        self._name: str = None
        self._type: str = None
        self._size: float = None
        self._contents: str = None
        self._last_modified: int = None
        self._last_accessed: DateTime = None
        self._protected: bool = protected
        self._construct(fp)
    
    def name(self) -> str:
        """ Returns the file name """
        return self._name
    
    def ftype(self) -> str:
        """ Returns the file type """
        return self._type
    
    def size(self) -> float:
        """ Returns the file size in KB """
        return self._size
    
    def protected(self) -> bool:
        """ Returns the file protection status """
        return self._protected
    
    def contents(self, **kwargs) -> str:
        """ Returns the file contents """
        if not self._protected:
            if self._contents is None:
                self._contents = self._retrieve_contents()
            return self._contents

        pass

    def mute(self) -> None:
        """ Clears the file contents from memory """
        self._contents = None

    def muted(self) -> bool:
        """ Returns the file mute status """
        if self._contents is None:
            return True
        return False

    def out_of_date(self) -> bool:
        """ Determines if the files information is out-of-date """
        if self._retrieve_last_modified() != self._last_modified:
            return True
        return False

    def update(self) -> None:
        """ Update the file information """
        if self.out_of_date():
            self._size = self._retrieve_size()
            self._last_modified = self._retrieve_last_modified()
            if self._contents is not None:
                self._contents = self._retrieve_contents()

    def last_accessed(self) -> DateTime:
        """ Returns the last access datetime stamp """
        return self._last_accessed
    
    def _retrieve_size(self) -> float:
        """ Returns the updated file size in KB """
        return float(os.path.getsize(self._path)/1024)
    
    def _retrieve_contents(self) -> str:
        """ Returns the updated contents of the file """
        with open(self._path) as readable:
            _contents: str = readable.read()
            readable.close()
        self._last_accessed = simplydatetime.now()
        return _contents
    
    def _retrieve_last_modified(self) -> int:
        """ Returns the files updated last modified stamp """
        return os.stat(self._path)[stat.ST_MTIME]

    def _construct(self, fp: str) -> None:
        """ Construct the framework file object """
        if not os.path.exists(fp):
            raise ValueError(
                f"Invalid file path: '{fp}'"
            )
        
        self._path = os.path.abspath(fp)
        self._name = os.path.basename(self._path)
        self._type = EXT_TYPES[self._name.split('.')[-1]]
        self._size = self._retrieve_size()
        self._last_modified = self._retrieve_last_modified()
        self._last_accessed = simplydatetime.now()
