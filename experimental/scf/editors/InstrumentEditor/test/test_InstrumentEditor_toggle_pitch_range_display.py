import scf


def test_InstrumentEditor_toggle_pitch_range_display_01():

    editor = scf.editors.InstrumentEditor()
    editor.run(user_input='marimba q')
    assert not editor.session.display_pitch_ranges_with_numbered_pitches

    editor = scf.editors.InstrumentEditor()
    editor.run(user_input='marimba tprd q')
    assert editor.session.display_pitch_ranges_with_numbered_pitches

    editor = scf.editors.InstrumentEditor()
    editor.run(user_input='marimba tprd tprd q')
    assert not editor.session.display_pitch_ranges_with_numbered_pitches
