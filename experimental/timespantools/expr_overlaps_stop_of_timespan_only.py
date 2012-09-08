def expr_overlaps_stop_of_timespan_only(timespan=None):
    r'''.. versionadded:: 1.0

    Make timespan inequality template indicating that expression happens during timespan::

        >>> from experimental import *

    ::

        >>> timespantools.expr_overlaps_stop_of_timespan_only()
        TimespanInequalityTemplate('expr_1.start <= expr_2.start < expr_1.stop < expr_2.stop')

    Return timespan inequality or timespan inequality template.
    '''
    from experimental import timespantools

    template = timespantools.TimespanInequalityTemplate('expr_1.start <= expr_2.start < expr_1.stop < expr_2.stop')

    if timespan is None:
        return template
    else:
        return timespantools.TimespanInequality(template, timespan)
