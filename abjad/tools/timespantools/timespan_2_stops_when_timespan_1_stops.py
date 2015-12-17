# -*- coding: utf-8 -*-


def timespan_2_stops_when_timespan_1_stops(
    timespan_1=None,
    timespan_2=None,
    hold=False,
    ):
    r'''Makes time relation indicating that `timespan_2` happens
    during `timespan_1`.

    ::

        >>> inequality = timespantools.timespan_2_stops_when_timespan_1_stops()
        >>> print(format(inequality))
        timespantools.TimespanTimespanTimeRelation(
            inequality=timespantools.CompoundInequality(
                [
                    timespantools.Inequality('timespan_2.stop_offset == timespan_1.stop_offset'),
                    ],
                logical_operator='and',
                ),
            )

    Returns time relation or boolean.
    '''
    from abjad.tools import timespantools

    inequality = timespantools.CompoundInequality([
        'timespan_2.stop_offset == timespan_1.stop_offset',
        ])

    time_relation = timespantools.TimespanTimespanTimeRelation(
        inequality,
        timespan_1=timespan_1,
        timespan_2=timespan_2,
        )

    if time_relation.is_fully_loaded and not hold:
        return time_relation()
    else:
        return time_relation
