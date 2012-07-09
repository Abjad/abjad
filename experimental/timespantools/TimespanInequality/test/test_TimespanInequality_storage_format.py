from experimental import timespantools


def test_TimespanInequality_storage_format_01():

    timespan = timespantools.SingleSourceTimespan()
    timespan_inequality_template = timespantools.expr_starts_during_timespan()
    timespan_inequality = timespantools.TimespanInequality(timespan_inequality_template, timespan)

    r'''
    timespantools.TimespanInequality(
        timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
        timespantools.SingleSourceTimespan()
        )
    '''

    assert timespan_inequality.storage_format == "timespantools.TimespanInequality(\n\ttimespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),\n\ttimespantools.SingleSourceTimespan()\n\t)"
