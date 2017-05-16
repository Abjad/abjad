# -*- coding: utf-8 -*-


def offset_happens_after_timespan_starts(
    timespan=None,
    offset=None,
    hold=False,
    ):
    r'''Makes time relation indicating that `offset` happens
    after `timespan` starts.
    ::

        >>> relation = timespantools.offset_happens_after_timespan_starts()
        >>> f(relation)
        abjad.OffsetTimespanTimeRelation(
            inequality=abjad.CompoundInequality(
                [
                    abjad.Inequality('timespan.start < offset'),
                    ],
                logical_operator='and',
                ),
            )

    Returns time relation or boolean.
    '''
    from abjad.tools import timespantools

    inequality = timespantools.CompoundInequality([
        'timespan.start < offset',
        ])

    time_relation = timespantools.OffsetTimespanTimeRelation(
        inequality,
        timespan=timespan,
        offset=offset,
        )

    if time_relation.is_fully_loaded and not hold:
        return time_relation()
    else:
        return time_relation
