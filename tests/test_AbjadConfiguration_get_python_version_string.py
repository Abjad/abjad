import abjad


def test_AbjadConfiguration_get_python_version_string_01():
    python_version_string = abjad.AbjadConfiguration.get_python_version_string()
    assert isinstance(python_version_string, str)
    assert python_version_string.count(".") == 2
