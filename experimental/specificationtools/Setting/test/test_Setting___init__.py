from experimental import specificationtools


def test_Setting___init___01():
    '''Initialize by hand.
    '''

    anchor = specificationtools.ScoreObjectIndicator(segment='1')
    start = specificationtools.TemporalCursor(anchor=anchor)
    stop = specificationtools.TemporalCursor(anchor=anchor, edge=Right)
    scope = specificationtools.TemporalScope(start=start, stop=stop)
    target = specificationtools.ContextSelection('Voice 1', scope=scope)
    setting = specificationtools.Setting(target, 'time_signatures', [(4, 8), (3, 8)], True, True)
    assert isinstance(setting, specificationtools.Setting)


def test_Setting___init___02():
    '''Initialize from other setting.
    '''

    anchor = specificationtools.ScoreObjectIndicator(segment='1')
    start = specificationtools.TemporalCursor(anchor=anchor)
    stop = specificationtools.TemporalCursor(anchor=anchor, edge=Right)
    scope = specificationtools.TemporalScope(start=start, stop=stop)
    target = specificationtools.ContextSelection('Voice 1', scope=scope)
    setting_1 = specificationtools.Setting(target, 'time_signatures', [(4, 8), (3, 8)], True, True, fresh=False)

    setting_2 = specificationtools.Setting(setting_1)
    
    assert isinstance(setting_1, specificationtools.Setting)
    assert isinstance(setting_2, specificationtools.Setting)
    assert not setting_1 is setting_2
    assert setting_1 == setting_2
