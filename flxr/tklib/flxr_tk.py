
""" FLUX Runtime-Engine Framework """


# MODULE IMPORTS
from flxr.tklib import *
from flxr import fw_obj

# MODULE PACKAGE
__package__ = tkpkg_n()


# MODULE CLASSES
class FlxrTkinterLibrary:
    def __init__(self, fw: any, svc: any):
        """
        Runtime-engine file I/O manager

        :param fw: Hosting framework
        :param svc: Framework service call
        """

        self.__FW = fw_obj(fw)
        self.__S = svc
        self._handle: str = 'fw-tklib'

        ...
        # self._inject_services()

    def _inject_services(self):
        """ Inject datetime services into distributor """
        injectables: list = [
            (),
        ]
        for new in injectables:
            self.__S(self)['nsvc'](
                call=new[0],
                cls=new[1],
                func=new[2],
                clearance=new[3]
            )
