""" Runtime-Engine Framework Constants """

#   CONSTANTS
RFW_FAIL_NOTICE: str = str(
    f'\n\t[ RUNTIME FRAMEWORK FAILED ]'
    f'\n\n\tUnable to start due to resource failure, press enter to exit...'
    f'\n\t'
)

APP_FAIL_NOTICE: str = str(
    f'\n\t[ APPLICATION FAILED ]'
    f'\n\n\tUnable to start due to application failure, press enter to exit...'
    f'\n\t'
)

MISSING_APP_ARGS: str = str(
    "Applications __init__ method missing required 'fw' and 'svc_c' parameters"
)
...
