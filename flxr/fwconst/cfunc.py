
""" Package Constant Functions """


#   MODULE IMPORTS
import inspect


#   CONSTANT FUNCTIONS
def fw_obj(fw: any) -> any:
    """
    Framework object parameter wrapper function (Ensures that the provided object is in-fact the FLUX runtime-engine)

    :param fw: The supposed framework object
    :return: The same object if valid runtime-engine
    """
    try:
        if fw.is_rfw():
            return fw
    except BaseException:
        raise ValueError(
            f'Invalid framework object parameter: {str(fw)}'
        )


def class_of(obj: any) -> type:
    """
    Returns the class of a given object
    
    :param obj: Any Python object
    :return: The class of obj
    """
    if 'object' in str(obj):
        return obj.__class__
    elif inspect.isclass(obj):
        return obj
