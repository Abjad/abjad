import abjad


def test_AbjadConfiguration_get_tab_width_01():
    assert abjad.AbjadConfiguration.get_tab_width() == 4
