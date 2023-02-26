
""" FLUX Runtime-Engine Framework Custom Exceptions """


#   MODULE CLASSES
class ExcFailureError(Exception):
    def __init__(self, value=None):
        """ Framework exception manager failure """
        self.value: str = 'The runtime exception manager failed'
        self.notice: str = "\n\n\t[ FATAL RUNTIME ERROR ] : ExcModFailure"
        if value is not None:
            self.value += f': {value}'
        return
