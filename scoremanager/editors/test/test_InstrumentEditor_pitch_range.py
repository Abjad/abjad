# -*- encoding: utf-8 -*-
from experimental import *


def test_InstrumentEditor_pitch_range_01():

    editor = scoremanager.editors.InstrumentEditor()
    editor._run(pending_user_input='marimba q')
    assert editor.target.pitch_range == pitchtools.PitchRange(-19, 36)

    editor = scoremanager.editors.InstrumentEditor()
    editor._run(pending_user_input='marimba rg [C2, C7] q')
    assert editor.target.pitch_range == pitchtools.PitchRange(-24, 36)
