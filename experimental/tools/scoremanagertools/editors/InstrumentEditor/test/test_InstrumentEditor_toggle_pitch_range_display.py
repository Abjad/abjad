from experimental import *


def test_InstrumentEditor_toggle_pitch_range_display_01():

    editor = scoremanagertools.editors.InstrumentEditor()
    editor._run(pending_user_input='marimba q')
    assert not editor._session.display_pitch_ranges_with_numbered_pitches

    editor = scoremanagertools.editors.InstrumentEditor()
    editor._run(pending_user_input='marimba tprd q')
    assert editor._session.display_pitch_ranges_with_numbered_pitches

    editor = scoremanagertools.editors.InstrumentEditor()
    editor._run(pending_user_input='marimba tprd tprd q')
    assert not editor._session.display_pitch_ranges_with_numbered_pitches
