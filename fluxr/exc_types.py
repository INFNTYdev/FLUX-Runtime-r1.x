
""" FLUX Runtime-Engine Framework Exception Classes """


#   MODULE CLASSES
class ExcFailureError(Exception):
    def __init__(self, value):
        self.value: str = 'The runtime exception manager failed'
        if len(str(value)) > 0:
            self.value += f': {value}'
        return
