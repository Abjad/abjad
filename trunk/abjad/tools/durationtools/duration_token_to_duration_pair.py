from abjad.tools.durationtools.lilypond_duration_string_to_rational import lilypond_duration_string_to_rational
from fractions import Fraction


def duration_token_to_duration_pair(duration_token):
    '''.. versionadded:: 1.1

    Change `duration_token` to duration pair::

        abjad> from abjad.tools import durationtools

    ::

        abjad> durationtools.duration_token_to_duration_pair(Fraction(2, 4))
        (1, 2)

    .. versionadded:: 2.0
        Change LilyPond duration string to duration pair:

    ::

        abjad> durationtools.duration_token_to_duration_pair('8.')
        (3, 16)

    Return pair.

    .. versionchanged:: 2.0
        renamed ``durationtools.token_unpack()`` to
        ``durationtools.duration_token_to_duration_pair()``.
    '''

    if isinstance(duration_token, (tuple, list)):
        if len(duration_token) == 1:
            numerator = duration_token[0]
            denominator = 1
        elif len(duration_token) == 2:
            numerator, denominator = duration_token
        else:
            raise ValueError('duration tuple must be of length 1 or 2.')
    elif isinstance(duration_token, int):
        numerator = duration_token
        denominator = 1
    elif isinstance(duration_token, Fraction):
        numerator, denominator = duration_token.numerator, duration_token.denominator
    elif isinstance(duration_token, str):
        rational = lilypond_duration_string_to_rational(duration_token)
        numerator, denominator = rational.numerator, rational.denominator
    else:
        raise TypeError('token must be of tuple, list, int or Fraction.')

    return numerator, denominator
