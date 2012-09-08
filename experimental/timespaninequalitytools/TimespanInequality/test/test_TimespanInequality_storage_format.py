from experimental import *


def test_TimespanInequality_storage_format_01():

    selector = selectortools.SingleSegmentSelector(identifier='red')
    timespan_inequality = timespaninequalitytools.expr_2_happens_during_expr_1(expr_1=selector)

    r'''
    timespaninequalitytools.TimespanInequality(
        'expr_1.start <= expr_2.start <= expr_2.stop <= expr_1.stop',
        expr_1=selectortools.SingleSegmentSelector(
            identifier='red'
            )
        )
    '''

    assert timespan_inequality.storage_format == "timespaninequalitytools.TimespanInequality(\n\t'expr_1.start <= expr_2.start <= expr_2.stop <= expr_1.stop',\n\texpr_1=selectortools.SingleSegmentSelector(\n\t\tidentifier='red'\n\t\t)\n\t)"
