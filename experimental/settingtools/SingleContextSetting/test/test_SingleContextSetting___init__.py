from experimental import selectortools
from experimental import settingtools
from experimental import specificationtools
from experimental import timespantools


def test_SingleContextSetting___init___01():
    '''Initialize by hand.
    '''

    segment_selector = selectortools.SegmentItemSelector(index='red')
    timespan = timespantools.SingleSourceTimespan(selector=segment_selector)
    target = selectortools.SingleContextTimespanSelector('Voice 1', timespan=timespan)
    setting = settingtools.SingleContextSetting('time_signatures', [(4, 8), (3, 8)], target)
    assert isinstance(setting, settingtools.SingleContextSetting)


#def test_SingleContextSetting___init___02():
#    '''Initialize from other setting.
#    '''
#
#    segment_selector = selectortools.SegmentItemSelector(index='red')
#    timespan = timespantools.SingleSourceTimespan(selector=segment_selector)
#    target = selectortools.SingleContextTimespanSelector('Voice 1', timespan=timespan)
#    setting_1 = settingtools.SingleContextSetting('time_signatures', [(4, 8), (3, 8)], target, fresh=False)
#
#    setting_2 = settingtools.SingleContextSetting(setting_1)
#    
#    assert isinstance(setting_1, settingtools.SingleContextSetting)
#    assert isinstance(setting_2, settingtools.SingleContextSetting)
#    assert not setting_1 is setting_2
#    assert setting_1 == setting_2
