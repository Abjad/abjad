from experimental import timespantools


def test_TimespanInequality_storage_format_01():

    timespan = timespantools.Timespan()
    timespan_inequality_class = timespantools.expr_starts_during_timespan()
    timespan_inequality = timespantools.TimespanInequality(timespan, timespan_inequality_class)

    r'''
    timespantools.TimespanInequality(
        timespantools.Timespan(),
        timespantools.TimespanInequalityClass(
            't.start <= expr.start < t.stop'
            )
        )
    '''

    assert timespan_inequality.storage_format == "timespantools.TimespanInequality(\n\ttimespantools.Timespan(),\n\ttimespantools.TimespanInequalityClass(\n\t\t't.start <= expr.start < t.stop'\n\t\t)\n\t)"
