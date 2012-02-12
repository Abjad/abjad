from fractions import Fraction
import re


def lilypond_duration_string_to_rational(duration_string):
    '''.. versionadded:: 2.0

    Change LilyPond `duration_string` to rational::

        abjad> from abjad.tools import durationtools

    ::

        abjad> durationtools.lilypond_duration_string_to_rational('8.')
        Fraction(3, 16)

    Return fraction.
    '''

    if not isinstance(duration_string, str):
        raise TypeError('duration string must be string.')

    numeric_body_strings = [str(2 ** n) for n in range(8)]
    other_body_strings = [r'\\breve', r'\\longa', r'\\maxima']
    body_strings = numeric_body_strings + other_body_strings
    body_strings = '|'.join(body_strings)
    pattern = r'^(%s)(\.*)$' % body_strings

    match = re.match(pattern, duration_string)
    if match is None:
        raise DurationError('incorrect duration string format: %s.' %
            duration_string)
    body_string, dots_string = match.groups()

    try:
        body_denominator = int(body_string)
        body_duration = Fraction(1, body_denominator)
    except ValueError:
        if body_string == r'\breve':
            body_duration = Fraction(2)
        elif body_string == r'\longa':
            body_duration = Fraction(4)
        elif body_string == r'\maxima':
            body_duration = Fraction(8)
        else:
            raise ValueError('unknown body string %s.' % body_string)

    rational = body_duration
    for n in range(len(dots_string)):
        exponent = n + 1
        denominator = 2 ** exponent
        multiplier = Fraction(1, denominator)
        addend = multiplier * body_duration
        rational += addend

    return rational
