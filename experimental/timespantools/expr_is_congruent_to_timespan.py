def expr_is_congruent_to_timespan(timespan=None):
    r'''.. versionadded:: 1.0

    Make timespan inequality template indicating that expression is congruent to timespan::

        >>> from experimental import *

    ::

        >>> timespantools.expr_is_congruent_to_timespan()
        TimespanInequalityTemplate('expr_1.start == expr_2.start and expr_1.stop == expr_2.stop')

    Return timespan inequality or timespan inequality template.
    '''
    from experimental import timespantools

    template = timespantools.TimespanInequalityTemplate('expr_1.start == expr_2.start and expr_1.stop == expr_2.stop')

    if timespan is None:
        return template
    else:
        return timespantools.TimespanInequality(template, timespan)
