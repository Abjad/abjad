from experimental import selectortools
from experimental import settingtools
from experimental import specificationtools
from experimental import timespaninequalitytools


def test_SingleContextSetting___init___01():
    '''Initialize by hand.
    '''

    selector = selectortools.SingleSegmentSelector(identifier='red')
    setting = settingtools.SingleContextSetting(
        'time_signatures', [(4, 8), (3, 8)], selector, context_name='Voice 1')

    assert isinstance(setting, settingtools.SingleContextSetting)
