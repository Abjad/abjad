from experimental import selectortools
from experimental import settingtools
from experimental import specificationtools
from experimental import timespantools


def test_ContextSetting___init___01():
    '''Initialize by hand.
    '''

    segment_selector = selectortools.SegmentSelector(index='red')
    timespan = timespantools.SingleSourceTimespan(selector=segment_selector)
    target = selectortools.SingleContextTimespanSelector('Voice 1', timespan=timespan)
    setting = settingtools.ContextSetting(target, 'time_signatures', [(4, 8), (3, 8)])
    assert isinstance(setting, settingtools.ContextSetting)


def test_ContextSetting___init___02():
    '''Initialize from other setting.
    '''

    segment_selector = selectortools.SegmentSelector(index='red')
    timespan = timespantools.SingleSourceTimespan(selector=segment_selector)
    target = selectortools.SingleContextTimespanSelector('Voice 1', timespan=timespan)
    setting_1 = settingtools.ContextSetting(target, 'time_signatures', [(4, 8), (3, 8)], fresh=False)

    setting_2 = settingtools.ContextSetting(setting_1)
    
    assert isinstance(setting_1, settingtools.ContextSetting)
    assert isinstance(setting_2, settingtools.ContextSetting)
    assert not setting_1 is setting_2
    assert setting_1 == setting_2
