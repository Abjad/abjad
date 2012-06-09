from experimental.specificationtools.Setting import Setting


def test_Setting___repr___01():
    '''Repr is evaluable.
    '''

    setting_1 = Setting('1', 'Voice 1', None, 'time_signatures', [(4, 8), (3, 8)], True, True)
    setting_2 = eval(repr(setting_1))

    assert isinstance(setting_1, Setting)
    assert isinstance(setting_2, Setting)
    assert not setting_1 is setting_2
    assert setting_1 == setting_2
