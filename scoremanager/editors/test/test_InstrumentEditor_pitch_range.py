# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_InstrumentEditor_pitch_range_01():

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.InstrumentEditor(session=session)
    input_ = 'marimba q'
    editor._run(pending_user_input=input_)
    assert editor.target.pitch_range == pitchtools.PitchRange(-19, 36)

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.InstrumentEditor(session=session)
    input_ = 'marimba rg [C2, C7] q'
    editor._run(pending_user_input=input_)
    assert editor.target.pitch_range == pitchtools.PitchRange(-24, 36)
