import fractions


def assignable_rational_to_lilypond_duration_string(rational):
    '''.. versionadded:: 2.0

    Change assignable `rational` to LilyPond duration string::

        >>> from abjad.tools import durationtools

    ::

        >>> durationtools.assignable_rational_to_lilypond_duration_string(Fraction(3, 16))
        '8.'

    Raise assignability error when `rational` not assignable.

    Return string.
    '''
    from abjad.tools import durationtools

    if not durationtools.is_assignable_rational(rational):
        raise AssignabilityError

    undotted_rational = durationtools.rational_to_equal_or_lesser_binary_rational(rational)
    if undotted_rational <= 1:
        undotted_duration_string = str(undotted_rational.denominator)
    elif undotted_rational == fractions.Fraction(2, 1):
        undotted_duration_string = r'\breve'
    elif undotted_rational == fractions.Fraction(4, 1):
        undotted_duration_string = r'\longa'
    elif undotted_rational == fractions.Fraction(8, 1):
        undotted_duration_string = r'\maxima'
    else:
        raise ValueError('can not process undotted rational: %s' % undotted_rational)

    dot_count = durationtools.assignable_rational_to_dot_count(rational)
    dot_string = '.' * dot_count
    dotted_duration_string = undotted_duration_string + dot_string

    return dotted_duration_string
