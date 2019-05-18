import abjad


def test_AbjadConfiguration_get_abjad_version_string_01():
    assert isinstance(abjad.AbjadConfiguration.get_abjad_version_string(), str)
