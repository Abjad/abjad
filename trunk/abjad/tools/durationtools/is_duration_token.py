def is_duration_token(expr):
    '''.. versionadded:: 2.0

    True when `expr` has the form of an Abjad duration token::

        >>> from abjad.tools import durationtools

    ::

        >>> durationtools.is_duration_token('8.')
        True

    Otherwise false::

        >>> durationtools.is_duration_token('foo')
        False

    Return boolean.
    '''
    from abjad.tools import durationtools

    try:
        durationtools.duration_token_to_duration_pair(expr)
        return True
    except (TypeError, ValueError, DurationError):
        return False
