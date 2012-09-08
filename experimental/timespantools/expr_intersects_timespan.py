def expr_intersects_timespan(expr_1=None, expr_2=None, hold=False):
    r'''.. versionadded:: 1.0

    Make timespan inequality template indicating that expression intersects timespan::

        >>> from experimental import *

    ::

        >>> timespantools.expr_intersects_timespan()
        TimespanInequalityTemplate('expr_1.start <= expr_2.start < expr_2.stop or expr_1.start < expr_2.stop <= expr_2.stop or expr_1.start < expr_2.start < expr_1.stop < expr_2.stop')

    Return timespan inequality or timespan inequality template.
    '''
    from experimental import timespantools

    template = timespantools.TimespanInequalityTemplate(
        'expr_1.start <= expr_2.start < expr_2.stop or '
        'expr_1.start < expr_2.stop <= expr_2.stop or '
        'expr_1.start < expr_2.start < expr_1.stop < expr_2.stop')

    if timespan is None:
        return template
    else:
        return timespantools.TimespanInequality(template, timespan)
