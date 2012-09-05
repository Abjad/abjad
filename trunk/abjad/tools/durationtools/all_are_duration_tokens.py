def all_are_duration_tokens(expr):
    '''.. versionadded:: 2.6

    True when `expr` is a sequence of Abjad duration tokens::

        >>> from abjad.tools import durationtools

    ::

        >>> duration_tokens = ['8.', (3, 16), Fraction(3, 16), Duration(3, 16)]

    ::

        >>> durationtools.all_are_duration_tokens(duration_tokens)
        True

    True when `expr` is an empty sequence::

        >>> durationtools.all_are_duration_tokens([])
        True

    Otherwise false::

        >>> durationtools.all_are_durations('foo')
        False

    Return boolean.
    '''
    from abjad.tools import durationtools

    return all([durationtools.is_duration_token(x) for x in expr])
