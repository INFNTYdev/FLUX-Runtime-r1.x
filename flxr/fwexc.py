
""" Framework defined exceptions """


# EXCEPTION MESSAGES
VEx001: str = str(
    f'The provided asset was not a valid class'
)


# RUNTIME EXCEPTIONS
class ExcFailureError(Exception):
    def __init__(self, value: any = None):
        """ Framework exception manager failure """
        Exception.__init__(self)
        self._value: str = 'Framework exception manager failed'
        if value is not None:
            self._value += f': {value}'
        self.notice: str = f'\n\n\t[ FATAL RUNTIME ERROR ] : {self._value}'
