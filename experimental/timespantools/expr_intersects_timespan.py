def expr_intersects_timespan(timespan=None):
    r'''.. versionadded:: 1.0

    Make timespan inequality template indicating that expression intersects timespan::

        >>> from experimental import *

    ::

        >>> timespantools.expr_intersects_timespan()
        TimespanInequalityTemplate('t.start <= expr.start < expr.stop or t.start < expr.stop <= expr.stop or t.start < expr.start < t.stop < expr.stop')

    Return timespan inequality or timespan inequality template.
    '''
    from experimental import timespantools

    template = timespantools.TimespanInequalityTemplate(
        't.start <= expr.start < expr.stop or '
        't.start < expr.stop <= expr.stop or '
        't.start < expr.start < t.stop < expr.stop')

    if timespan is None:
        return template
    else:
        return timespantools.TimespanInequality(template, timespan)
