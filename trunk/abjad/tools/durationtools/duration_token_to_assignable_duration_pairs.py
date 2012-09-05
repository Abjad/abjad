from abjad.tools import mathtools


def duration_token_to_assignable_duration_pairs(duration_token):
    '''.. versionadded:: 1.1

    Change `duration_token` to big-endian tuple of assignable duration pairs::

        >>> from abjad.tools import durationtools

    ::

        >>> duration_tokens = [(n, 16) for n in range(10, 20)]
        >>> for duration_token in duration_tokens:
        ...     pairs = durationtools.duration_token_to_assignable_duration_pairs(
        ...         duration_token)
        ...     print duration_token, pairs
        ...
        (10, 16) ((8, 16), (2, 16))
        (11, 16) ((8, 16), (3, 16))
        (12, 16) ((12, 16),)
        (13, 16) ((12, 16), (1, 16))
        (14, 16) ((14, 16),)
        (15, 16) ((15, 16),)
        (16, 16) ((16, 16),)
        (17, 16) ((16, 16), (1, 16))
        (18, 16) ((16, 16), (2, 16))
        (19, 16) ((16, 16), (3, 16))

    Return tuple of integer pairs.

    .. versionchanged:: 2.0
        renamed ``durationtools.token_decompose()`` to
        ``durationtools.duration_token_to_assignable_duration_pairs()``.
    '''
    from abjad.tools import durationtools

    numerator, denominator = durationtools.duration_token_to_duration_pair(duration_token)
    result = [(n, denominator)
        for n in mathtools.partition_integer_into_canonic_parts(numerator)]
    return tuple(result)
