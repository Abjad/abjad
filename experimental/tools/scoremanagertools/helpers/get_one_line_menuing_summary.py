import abc
import types


def get_one_line_menuing_summary(expr):
    '''Get one-line menuing summary of `expr`.

    Return string.
    '''
    if isinstance(expr, (types.ClassType, abc.ABCMeta, types.TypeType)):
        return expr.__name__
    elif getattr(expr, '_one_line_menuing_summary', None):
        return expr._one_line_menuing_summary
    elif isinstance(expr, str):
        return expr
    else:
        return repr(expr)
