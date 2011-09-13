from abjad.tools.durationtools.lilypond_duration_string_to_rational import lilypond_duration_string_to_rational


def lilypond_duration_string_to_rational_list(duration_string):
    '''.. versionadded:: 2.0

    Change LilyPond `duration_string` to rational list::

        abjad> from abjad.tools import durationtools

    ::

        abjad> durationtools.lilypond_duration_string_to_rational_list('8.. 32 8.. 32')
        [Fraction(7, 32), Fraction(1, 32), Fraction(7, 32), Fraction(1, 32)]

    Return list of fractions.
    '''

    if not isinstance(duration_string, str):
        raise TypeError('duration string must be string.')

    rationals = []
    duration_strings = duration_string.split()
    for duration_string in duration_strings:
        rational = lilypond_duration_string_to_rational(duration_string)
        rationals.append(rational)

    return rationals
