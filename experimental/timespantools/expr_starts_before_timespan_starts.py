def expr_starts_before_timespan_starts(timespan=None):
    r'''.. versionadded:: 1.0

    Make timespan inequality template indicating that expression starts before timespan starts::

        >>> from experimental import *

    ::

        >>> timespantools.expr_starts_before_timespan_starts()
        TimespanInequalityTemplate('expr.start < t.start')

    Return timespan inequality or timespan inequality template.
    '''
    from experimental import timespantools

    template = timespantools.TimespanInequalityTemplate('expr.start < t.start')

    if timespan is None:
        return template
    else:
        return timespantools.TimespanInequality(template, timespan)
