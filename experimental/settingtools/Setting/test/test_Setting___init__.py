from experimental.settingtools.Setting import Setting


def test_Setting___init___01():
    '''Init by hand.
    '''

    directive = Setting(None, 'time_signatures', [(4, 8), (3, 8)])
    assert isinstance(directive, Setting)


def test_Setting___init___02():
    '''Init from other directive.
    '''

    directive_1 = Setting(None, 'time_signatures', [(4, 8), (3, 8)], persistent=False, truncate=False)
    directive_2 = Setting(directive_1)

    assert isinstance(directive_1, Setting)
    assert isinstance(directive_2, Setting)
    assert not directive_1 is directive_2
    assert directive_1 == directive_2
