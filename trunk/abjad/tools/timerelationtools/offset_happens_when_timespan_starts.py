# -*- encoding: utf-8 -*-


def offset_happens_when_timespan_starts(
    timespan=None, 
    offset=None, 
    hold=False,
    ):
    r'''Makes time relation indicating that `offset` happens 
    when `timespan` starts.

    ::

        >>> relation = timerelationtools.offset_happens_when_timespan_starts()
        >>> print relation.storage_format
        timerelationtools.OffsetTimespanTimeRelation(
            timerelationtools.CompoundInequality([
                timerelationtools.SimpleInequality('offset == timespan.start')
                ],
                logical_operator='and'
                )
            )

    Returns time relation or boolean.
    '''
    from abjad.tools import timerelationtools

    inequality = timerelationtools.CompoundInequality([
        'offset == timespan.start',
        ])

    time_relation = timerelationtools.OffsetTimespanTimeRelation(
        inequality,
        timespan=timespan,
        offset=offset)

    if time_relation.is_fully_loaded and not hold:
        return time_relation()
    else:
        return time_relation
