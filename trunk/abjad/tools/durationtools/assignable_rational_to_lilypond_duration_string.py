from abjad.tools.durationtools.assignable_rational_to_dot_count import assignable_rational_to_dot_count
from abjad.tools.durationtools.is_assignable_rational import is_assignable_rational
from abjad.tools.durationtools.rational_to_equal_or_lesser_binary_rational import rational_to_equal_or_lesser_binary_rational
from fractions import Fraction


def assignable_rational_to_lilypond_duration_string(rational):
    '''.. versionadded:: 2.0

    Change assignable `rational` to LilyPond duration string::

        abjad> from abjad.tools import durationtools

    ::

        abjad> durationtools.assignable_rational_to_lilypond_duration_string(Fraction(3, 16))
        '8.'

    Raise assignability error when `rational` not assignable.

    Return string.
    '''

    if not is_assignable_rational(rational):
        raise AssignabilityError

    undotted_rational = rational_to_equal_or_lesser_binary_rational(rational)
    if undotted_rational <= 1:
        undotted_duration_string = str(undotted_rational.denominator)
    elif undotted_rational == Fraction(2, 1):
        undotted_duration_string = r'\breve'
    elif undotted_rational == Fraction(4, 1):
        undotted_duration_string = r'\longa'
    elif undotted_rational == Fraction(8, 1):
        undotted_duration_string = r'\maxima'
    else:
        raise ValueError('can not process undotted rational: %s' % undotted_rational)

    dot_count = assignable_rational_to_dot_count(rational)
    dot_string = '.' * dot_count
    dotted_duration_string = undotted_duration_string + dot_string

    return dotted_duration_string
