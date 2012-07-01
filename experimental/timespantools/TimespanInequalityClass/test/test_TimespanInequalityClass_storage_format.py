from experimental import timespantools


def test_TimespanInequalityClass_storage_format_01():

    timespan_inequality_class = timespantools.expr_starts_during_timespan()

    r'''    
    timespantools.TimespanInequalityClass(
        't.start <= expr.start < t.stop'
        )
    '''

    assert timespan_inequality_class.storage_format == "timespantools.TimespanInequalityClass(\n\t't.start <= expr.start < t.stop'\n\t)"
