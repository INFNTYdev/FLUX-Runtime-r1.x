
""" Framework file object """


# MODULE IMPORTS
from flxr import *

# MODULE PACKAGE
__package__ = pkg_n()


# MODULE CLASSES
class FWFile:

    __EXT_DICT: dict = {
        'txt': 'Text Document',
        'py': 'Python File',
        'pyc': 'Compiled Python File',
    }

    def __init__(self, filepath: str, **kwargs):
        """ Framework file """
        self.__path: str = None
        self.__name: str = None
        self.__title: str = None
        self.__type: str = None
        self.__size: float = None
        self.__contents: str = None
        self.__last_modified = None
        self.__protected: bool = kwargs.get('protected', False)
        self.__construct(fp=filepath, **kwargs)

    def name(self) -> str:
        """ Returns the file name """
        return self.__name

    def ftype(self) -> str:
        """ Returns the file type """
        return self.__type

    def size(self) -> float:
        """ Returns the file size in KB """
        return self.__size

    def protected(self) -> bool:
        """ Returns the files protection status """
        return self.__protected

    def contents(self, **kwargs) -> str:
        """ Returns the contents of the file """
        if self.__protected:
            pass
        else:
            return self.__contents

    def out_of_date(self) -> bool:
        """ Determines if the file is out of date """
        if self.__retrieve_last_modified() != self.__last_modified:
            return True
        return False

    def update(self):
        """ Update the files contents """
        if self.out_of_date():
            self.__read_size()
            self.__contents = self.__read_self()
            self.__last_modified = self.__retrieve_last_modified()

    def is_path(self, path: str) -> bool:
        """ Determines if a string is the files path """
        if path == self.__path:
            return True
        return False

    def __read_title(self) -> str:
        """ Derive the file title """
        for index in range(1, len(self.__name)):
            if self.__name[-index] == '.':
                return self.__name[:-index]

    def __read_size(self) -> float:
        """ Returns the updated file size """
        return round(float(os.path.getsize(self.__path)/1024), 2)

    def __read_self(self) -> str:
        """ Returns the updated file contents """
        with open(file=self.__path) as readable:
            __contents: str = readable.read()
            readable.close()
        return __contents

    def __retrieve_last_modified(self) -> any:
        """ Returns the files last modified stamp """
        return os.stat(self.__path)[stat.ST_MTIME]

    def __construct(self, **args):
        """ Construct the framework file """
        self.__path = os.path.abspath(args.get('fp'))
        self.__name = os.path.basename(args.get('fp'))
        self.__title = self.__read_title()
        self.__type = self.__EXT_DICT[self.__name.split('.')[-1]]
        self.__size = self.__read_size()
        self.__contents = self.__read_self()
        self.__last_modified = self.__retrieve_last_modified()
