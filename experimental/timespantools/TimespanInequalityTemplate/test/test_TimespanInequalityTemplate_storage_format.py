from experimental import timespantools


def test_TimespanInequalityTemplate_storage_format_01():

    timespan_inequality_class = timespantools.expr_starts_during_timespan()

    r'''    
    timespantools.TimespanInequalityTemplate(
        't.start <= expr.start < t.stop'
        )
    '''

    assert timespan_inequality_class.storage_format == "timespantools.TimespanInequalityTemplate(\n\t't.start <= expr.start < t.stop'\n\t)"
