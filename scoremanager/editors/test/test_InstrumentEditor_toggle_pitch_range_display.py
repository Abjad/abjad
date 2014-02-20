# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_InstrumentEditor_toggle_pitch_range_display_01():

    editor = scoremanager.editors.InstrumentEditor()
    editor._run(pending_user_input='marimba q')
    assert not editor._session.display_pitch_ranges_with_numbered_pitches

    editor = scoremanager.editors.InstrumentEditor()
    editor._run(pending_user_input='marimba tprd q')
    assert editor._session.display_pitch_ranges_with_numbered_pitches

    editor = scoremanager.editors.InstrumentEditor()
    editor._run(pending_user_input='marimba tprd tprd q')
    assert not editor._session.display_pitch_ranges_with_numbered_pitches
