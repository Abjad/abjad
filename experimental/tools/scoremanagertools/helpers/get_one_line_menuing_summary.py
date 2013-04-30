import abc
import types


def get_one_line_menuing_summary(expr):
    '''Get one-line menuing summary of `expr`.

    Return string.
    '''
    if isinstance(expr, (types.ClassType, abc.ABCMeta)):
        return expr.__name__
    elif getattr(expr, 'one_line_menuing_summary', None):
        return expr.one_line_menuing_summary
    elif getattr(expr, '_one_line_menuing_summary', None):
        return expr._one_line_menuing_summary
    elif isinstance(expr, type(type)):
        return expr.__name__
    elif isinstance(expr, str):
        return expr
    else:
        return repr(expr)
