
"""
Deployable FLUX Framework Dependant Module
"""


#   EXTERNAL IMPORTS
from .fwm import Fwm
from flxr.common.protocols import Flux


#   MODULE CLASS
class DeployableFwm(Fwm):
    def __init__(self, hfw: Flux, cls: type, core: bool) -> None:
        """ Base deployable FLUX
        runtime framework module """
        super().__init__(hfw=hfw, cls=cls)
        self.__core_module: bool = bool(core)

    def core_module(self) -> bool:
        """ Returns true if deployable
        module is required by framework """
        return self.__core_module

    def status(self) -> bool:
        """ Returns deployable module run status """
        return self.hfw_service(svc='getstat', module=self.fwm_class())

    def set_status(self, status: bool) -> None:
        """ Set deployable module status """
        self.hfw_service(svc='setstat', module=self.fwm_class(), status=status)
