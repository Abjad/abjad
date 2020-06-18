import abjad


def test_ly_environment_01():

    assert abjad.ly.contexts is not None
    print(abjad.ly.contexts)

    assert abjad.ly.current_module is not None
    print(abjad.ly.current_module)

    assert abjad.ly.engravers is not None
    print(abjad.ly.engravers)

    assert abjad.ly.grob_interfaces is not None
    print(abjad.ly.grob_interfaces)

    assert abjad.ly.interface_properties is not None
    print(abjad.ly.interface_properties)

    assert abjad.ly.language_pitch_names is not None
    print(abjad.ly.language_pitch_names)

    assert abjad.ly.markup_functions is not None
    print(abjad.ly.markup_functions)

    assert abjad.ly.markup_functions.markup_list_functions is not None
    print(abjad.ly.markup_functions.markup_list_functions)

    assert abjad.ly.music_glyphs is not None
    print(abjad.ly.music_glyphs)
