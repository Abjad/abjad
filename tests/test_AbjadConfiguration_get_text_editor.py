import abjad


def test_AbjadConfiguration_get_text_editor_01():
    assert isinstance(
        abjad.AbjadConfiguration.get_text_editor(),
        str,
        )
