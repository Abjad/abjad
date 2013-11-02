# -*- encoding: utf-8 -*-


def offset_happens_during_timespan(timespan=None, offset=None, hold=False):
    r'''MakeS time relation indicating that `offset` happens during `timespan`.

    ::

        >>> relation = timerelationtools.offset_happens_during_timespan()
        >>> print relation.storage_format
        timerelationtools.OffsetTimespanTimeRelation(
            timerelationtools.CompoundInequality([
                timerelationtools.SimpleInequality('timespan.start <= offset'),
                timerelationtools.SimpleInequality('offset < timespan.stop'),
                ],
                logical_operator='and',
                )
            )

    Returns time relation or boolean.
    '''
    from abjad.tools import timerelationtools

    inequality = timerelationtools.CompoundInequality([
        'timespan.start <= offset',
        'offset < timespan.stop',
            ])

    time_relation = timerelationtools.OffsetTimespanTimeRelation(
        inequality,
        timespan=timespan,
        offset=offset)

    if time_relation.is_fully_loaded and not hold:
        return time_relation()
    else:
        return time_relation
