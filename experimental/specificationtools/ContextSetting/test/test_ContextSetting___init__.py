from experimental import timespantools
from experimental import specificationtools


def test_ContextSetting___init___01():
    '''Initialize by hand.
    '''

    anchor = specificationtools.ScoreElementSelector(segment='1')
    start = specificationtools.Timepoint(anchor=anchor)
    stop = specificationtools.Timepoint(anchor=anchor, edge=Right)
    timespan = timespantools.Timespan(start=start, stop=stop)
    target = specificationtools.ContextSelection('Voice 1', timespan=timespan)
    setting = specificationtools.ContextSetting(target, 'time_signatures', [(4, 8), (3, 8)])
    assert isinstance(setting, specificationtools.ContextSetting)


def test_ContextSetting___init___02():
    '''Initialize from other setting.
    '''

    anchor = specificationtools.ScoreElementSelector(segment='1')
    start = specificationtools.Timepoint(anchor=anchor)
    stop = specificationtools.Timepoint(anchor=anchor, edge=Right)
    timespan = timespantools.Timespan(start=start, stop=stop)
    target = specificationtools.ContextSelection('Voice 1', timespan=timespan)
    setting_1 = specificationtools.ContextSetting(target, 'time_signatures', [(4, 8), (3, 8)], fresh=False)

    setting_2 = specificationtools.ContextSetting(setting_1)
    
    assert isinstance(setting_1, specificationtools.ContextSetting)
    assert isinstance(setting_2, specificationtools.ContextSetting)
    assert not setting_1 is setting_2
    assert setting_1 == setting_2
