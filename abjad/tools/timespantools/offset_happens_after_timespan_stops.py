# -*- coding: utf-8 -*-


def offset_happens_after_timespan_stops(
    timespan=None,
    offset=None,
    hold=False,
    ):
    r'''Makes time relation indicating that `offset` happens
    after `timespan` stops.

    ::

        >>> import abjad

    ..  container:: example

        ::

            >>> relation = abjad.timespantools.offset_happens_after_timespan_stops()
            >>> f(relation)
            abjad.OffsetTimespanTimeRelation(
                inequality=abjad.CompoundInequality(
                    [
                        abjad.TimespanInequality('timespan.stop < offset'),
                        ],
                    logical_operator='and',
                    ),
                )

    Returns time relation or boolean.
    '''
    from abjad.tools import timespantools

    inequality = timespantools.CompoundInequality([
        'timespan.stop < offset',
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
