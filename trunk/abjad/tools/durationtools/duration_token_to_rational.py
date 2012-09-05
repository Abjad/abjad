import fractions


def duration_token_to_rational(duration_token):
    '''.. versionadded:: 2.0

    Change `duration_token` to rational::

        >>> from abjad.tools import durationtools

    ::

        >>> durationtools.duration_token_to_rational((4, 16))
        Fraction(1, 4)

    ::

        >>> durationtools.duration_token_to_rational('4.')
        Fraction(3, 8)

    Return fraction.
    '''
    from abjad.tools import durationtools

    return fractions.Fraction(*durationtools.duration_token_to_duration_pair(duration_token))
