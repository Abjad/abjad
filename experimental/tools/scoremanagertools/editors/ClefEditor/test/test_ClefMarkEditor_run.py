# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from experimental import *


def test_ClefMarkEditor_run_01():

    editor = scoremanagertools.editors.ClefEditor()
    editor._run(pending_user_input='clef treble done')

    clef = indicatortools.Clef('treble')
    assert editor.target == clef
