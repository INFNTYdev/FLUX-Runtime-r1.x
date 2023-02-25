
""" FLUX Runtime-Engine Framework Exception Classes """


#   MODULE CLASSES
class ExcFailureError(Exception):
    def __init__(self, value=None):
        """ Framework exception manager failure """
        self.value: str = 'The runtime exception manager failed'
        if value is not None:
            self.value += f': {value}'
        return
