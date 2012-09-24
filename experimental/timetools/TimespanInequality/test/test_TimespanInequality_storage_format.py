from experimental import *


def test_TimespanInequality_storage_format_01():

    selector = selectortools.SingleSegmentSelector(identifier='red')
    timespan_inequality = timetools.timespan_2_happens_during_timespan_1(timespan_1=selector)

    r'''
    timetools.TimespanInequality(
        'timespan_1.start <= timespan_2.start <= timespan_2.stop <= timespan_1.stop',
        timespan_1=selectortools.SingleSegmentSelector(
            identifier='red'
            )
        )
    '''

    assert timespan_inequality.storage_format == "timetools.TimespanInequality(\n\t'timespan_1.start <= timespan_2.start <= timespan_2.stop <= timespan_1.stop',\n\ttimespan_1=selectortools.SingleSegmentSelector(\n\t\tidentifier='red'\n\t\t)\n\t)"
