from experimental import timespantools
import py


def test_TimespanInequalityTemplate_storage_format_01():
    py.test.skip('deprecated.')

    timespan_inequality_template = timespantools.expr_starts_during_timespan()

    r'''    
    timespantools.TimespanInequalityTemplate('expr_1.start <= expr_2.start < expr_1.stop')
    '''

    assert timespan_inequality_template.storage_format == "timespantools.TimespanInequalityTemplate('expr_1.start <= expr_2.start < expr_1.stop')"
