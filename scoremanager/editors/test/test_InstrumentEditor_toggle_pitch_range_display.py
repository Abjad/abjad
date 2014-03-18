# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_InstrumentEditor_toggle_pitch_range_display_01():

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.InstrumentEditor(session=session)
    input_ = 'marimba q'
    editor._run(pending_user_input=input_)
    assert not editor._session.display_pitch_ranges_with_numbered_pitches

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.InstrumentEditor(session=session)
    input_ = 'marimba tprd q'
    editor._run(pending_user_input=input_)
    assert editor._session.display_pitch_ranges_with_numbered_pitches

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.InstrumentEditor(session=session)
    input_ = 'marimba tprd tprd q'
    editor._run(pending_user_input=input_)
    assert not editor._session.display_pitch_ranges_with_numbered_pitches
