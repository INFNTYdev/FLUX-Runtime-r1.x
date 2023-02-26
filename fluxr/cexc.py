
""" FLUX Runtime-Engine Framework Custom Exceptions """


#   MODULE CLASSES
class ExcFailureError(Exception):
    def __init__(self, value=None):
        """ Framework exception manager failure """
        self.value: str = 'The runtime exception manager failed'
        if value is not None:
            self.value += f': {value}'
        self.notice: str = f"\n\n\t[ FATAL RUNTIME ERROR ] : {self.value}"
        return


class SvcFailureError(Exception):
    def __init__(self, value=None):
        """ Framework service provider failure """
        self.value: str = 'The runtime service provider failed'
        if value is not None:
            self.value += f': {value}'
        self.notice: str = f"\n\n\t[ FATAL RUNTIME ERROR ] : {self.value}"
        return
