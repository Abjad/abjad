from abjad.tools import mathtools


def group_duration_tokens_by_implied_prolation(durations):
    '''.. versionadded:: 1.1

    Group `durations` by implied prolation::

        abjad> from abjad.tools import durationtools

    ::

        abjad> durationtools.group_duration_tokens_by_implied_prolation([(1, 4), (1, 8), (1, 3), (1, 6), (1, 4)])
        [[(1, 4), (1, 8)], [(1, 3), (1, 6)], [(1, 4)]]

    Return list of integer pair lists.

    .. versionchanged:: 2.0
        renamed ``durationtools.agglomerate_by_prolation()`` to
        ``durationtools.group_duration_tokens_by_implied_prolation()``.
    '''

    assert isinstance(durations, list)
    assert 0 < len(durations)

    group = [durations[0]]
    result = [group]
    for d in durations[1:]:
        d_f = set(mathtools.factors(d[1]))
        d_f.discard(2)
        gd_f = set(mathtools.factors(group[0][1]))
        gd_f.discard(2)
        if d_f == gd_f:
            group.append(d)
        else:
            group = [d]
            result.append(group)
    return result
