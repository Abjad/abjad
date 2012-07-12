from experimental.settingtools.MultipleContextSetting import MultipleContextSetting


def test_MultipleContextSetting___init___01():
    '''Init by hand.
    '''

    directive = MultipleContextSetting(None, 'time_signatures', [(4, 8), (3, 8)])
    assert isinstance(directive, MultipleContextSetting)


def test_MultipleContextSetting___init___02():
    '''Init from other directive.
    '''

    directive_1 = MultipleContextSetting(None, 'time_signatures', [(4, 8), (3, 8)], persistent=False, truncate=False)
    directive_2 = MultipleContextSetting(directive_1)

    assert isinstance(directive_1, MultipleContextSetting)
    assert isinstance(directive_2, MultipleContextSetting)
    assert not directive_1 is directive_2
    assert directive_1 == directive_2
