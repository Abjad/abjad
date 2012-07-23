from experimental.settingtools.MultipleContextSetting import MultipleContextSetting


def test_MultipleContextSetting___init___01():
    '''Init by hand.
    '''

    multiple_context_setting = MultipleContextSetting(None, 'time_signatures', [(4, 8), (3, 8)])
    assert isinstance(multiple_context_setting, MultipleContextSetting)


def test_MultipleContextSetting___init___02():
    '''Init from other multiple_context_setting.
    '''

    multiple_context_setting_1 = MultipleContextSetting(None, 'time_signatures', [(4, 8), (3, 8)], persistent=False, truncate=False)
    multiple_context_setting_2 = MultipleContextSetting(multiple_context_setting_1)

    assert isinstance(multiple_context_setting_1, MultipleContextSetting)
    assert isinstance(multiple_context_setting_2, MultipleContextSetting)
    assert not multiple_context_setting_1 is multiple_context_setting_2
    assert multiple_context_setting_1 == multiple_context_setting_2
