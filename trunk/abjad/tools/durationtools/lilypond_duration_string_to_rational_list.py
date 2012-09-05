def lilypond_duration_string_to_rational_list(duration_string):
    '''.. versionadded:: 2.0

    Change LilyPond `duration_string` to rational list::

        >>> from abjad.tools import durationtools

    ::

        >>> durationtools.lilypond_duration_string_to_rational_list('8.. 32 8.. 32')
        [Fraction(7, 32), Fraction(1, 32), Fraction(7, 32), Fraction(1, 32)]

    Return list of fractions.
    '''
    from abjad.tools import durationtools

    if not isinstance(duration_string, str):
        raise TypeError('duration string must be string.')

    rationals = []
    duration_strings = duration_string.split()
    for duration_string in duration_strings:
        rational = durationtools.lilypond_duration_string_to_rational(duration_string)
        rationals.append(rational)

    return rationals
