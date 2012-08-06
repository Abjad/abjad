from experimental import selectortools
from experimental import settingtools
from experimental import specificationtools
from experimental import timespantools


def test_SingleContextSetting___init___01():
    '''Initialize by hand.
    '''

    segment_selector = selectortools.SegmentItemSelector(identifier='red')
    timespan = timespantools.SingleSourceTimespan(selector=segment_selector)
    selector = selectortools.TimespanSelector(timespan)
    setting = settingtools.SingleContextSetting(
        'time_signatures', [(4, 8), (3, 8)], selector, context_name='Voice 1')

    assert isinstance(setting, settingtools.SingleContextSetting)
