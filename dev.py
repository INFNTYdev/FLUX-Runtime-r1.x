
print('Importing framework...')
from flxr import *

try:
    print(f'{pkg_n()} {pkg_v()}\n')
    test: Flxr = Flxr(dev=True, main=None)
    print('\nSuccessful')
except Exception as Failure:
    print(f'\nFailed:\n{Failure}\n{sys.exc_info()}')
    pass
except KeyboardInterrupt as ForcedStop:
    print(f'\nApplication was forced to stop')
finally:
    print('\nDone.')
