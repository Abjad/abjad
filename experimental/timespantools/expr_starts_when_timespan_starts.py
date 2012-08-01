def expr_starts_when_timespan_starts(timespan=None):
    r'''.. versionadded:: 1.0

    Make timespan inequality template indicating that expression starts when timespan starts::

        >>> from experimental import *

    ::

        >>> timespantools.expr_starts_when_timespan_starts()
        TimespanInequalityTemplate('t.start == expr.start')

    Return timespan inequality or timespan inequality template.
    '''
    from experimental import timespantools

    template = timespantools.TimespanInequalityTemplate('t.start == expr.start')

    if timespan is None:
        return template
    else:
        return timespantools.TimespanInequality(template, timespan)
