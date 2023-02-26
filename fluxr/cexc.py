
""" FLUX Runtime-Engine Framework Custom Exceptions """


#   MODULE CLASSES
class ExcFailureError(Exception):
    def __init__(self, value=None):
        """ Framework exception manager failure """
        self.value: str = 'The runtime exception manager failed'
        self.notice: str = f"\n\n\t[ FATAL RUNTIME ERROR ] : {self.value}"
        if value is not None:
            self.value += f': {value}'
        return


class SvcFailureError(Exception):
    def __init__(self, value=None):
        """ Framework service provider failure """
        self.value: str = 'The runtime service provider failed'
        self.notice: str = f"\n\n\t[ FATAL RUNTIME ERROR ] : {self.value}"
        if value is not None:
            self.value += f': {value}'
        return
