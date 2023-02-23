import abjad


def test_ly_environment_01():
    assert abjad.lyenv.contexts is not None
    print(abjad.lyenv.contexts)

    assert abjad.lyenv.current_module is not None
    print(abjad.lyenv.current_module)

    assert abjad.lyenv.engravers is not None
    print(abjad.lyenv.engravers)

    assert abjad.lyenv.grob_interfaces is not None
    print(abjad.lyenv.grob_interfaces)

    assert abjad.lyenv.interface_properties is not None
    print(abjad.lyenv.interface_properties)

    assert abjad.lyenv.language_pitch_names is not None
    print(abjad.lyenv.language_pitch_names)

    assert abjad.lyenv.markup_functions is not None
    print(abjad.lyenv.markup_functions)

    assert abjad.lyenv.markup_list_functions is not None
    print(abjad.lyenv.markup_list_functions)

    assert abjad.lyenv.music_glyphs is not None
    print(abjad.lyenv.music_glyphs)
