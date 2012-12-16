import fractions
from abjad.tools import mathtools


def group_nonreduced_fractions_by_implied_prolation(durations):
    '''.. versionadded:: 1.1

    Group `durations` by implied prolation::

        >>> durations = [(1, 4), (1, 8), (1, 3), (1, 6), (1, 4)]

    ::

        >>> for group in durationtools.group_nonreduced_fractions_by_implied_prolation(durations):
        ...     group
        [NonreducedFraction(1, 4), NonreducedFraction(1, 8)]
        [NonreducedFraction(1, 3), NonreducedFraction(1, 6)]
        [NonreducedFraction(1, 4)]

    Return list of duration lists.
    '''
    from abjad.tools import durationtools

    durations = [mathtools.NonreducedFraction(duration) for duration in durations]
    assert 0 < len(durations)

    group = [durations[0]]
    result = [group]
    for d in durations[1:]:
        d_f = set(mathtools.factors(d.denominator))
        d_f.discard(2)
        gd_f = set(mathtools.factors(group[0].denominator))
        gd_f.discard(2)
        if d_f == gd_f:
            group.append(d)
        else:
            group = [d]
            result.append(group)
    return result
