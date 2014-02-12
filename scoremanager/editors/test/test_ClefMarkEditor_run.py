# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ClefMarkEditor_run_01():

    editor = scoremanager.editors.ClefEditor()
    editor._run(pending_user_input='clef treble done')

    clef = indicatortools.Clef('treble')
    assert editor.target == clef
