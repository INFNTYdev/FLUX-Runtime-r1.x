
""" FLUX Runtime-Engine Framework Exception Classes """


#   MODULE CLASSES
class ExcFailureError(Exception):
    def __init__(self):
        self.value: str = 'The runtime exception manager failed'
        return
