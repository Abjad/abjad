# -*- encoding: utf-8 -*-


def new(expr, *args, **kwargs):
    r'''Makes new `expr` with optionally new `args` and ``kwargs``.

    Returns new object with the same type as `expr`.
    '''

    if not hasattr(expr, '__makenew__'):
        message = 'does not implement the make-new protocol: {!r}.'
        message = message.format(expr)
        raise TypeError(message)

    new = expr.__makenew__(*args, **kwargs)
    return new
