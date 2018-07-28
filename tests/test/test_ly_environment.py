def test_ly_environment_01():

    from abjad import ly

    assert ly.contexts is not None
    print(ly.contexts)

    assert ly.current_module is not None
    print(ly.current_module)

    assert ly.engravers is not None
    print(ly.engravers)

    assert ly.grob_interfaces is not None
    print(ly.grob_interfaces)

    assert ly.interface_properties is not None
    print(ly.interface_properties)

    assert ly.language_pitch_names is not None
    print(ly.language_pitch_names)

    assert ly.markup_functions is not None
    print(ly.markup_functions)

    assert ly.markup_list_functions is not None
    print(ly.markup_list_functions)

    assert ly.music_glyphs is not None
    print(ly.music_glyphs)
