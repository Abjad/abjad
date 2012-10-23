def is_duration_token(expr):
    '''.. versionadded:: 2.0

    True when `expr` can initialize an Abjad duration object:

        >>> durationtools.is_duration_token('8.')
        True

    Otherwise false::

        >>> durationtools.is_duration_token('foo')
        False

    Return boolean.
    '''
    from abjad.tools import durationtools

    try:
        durationtools.Duration(expr)
        return True
    except:
        return False 
