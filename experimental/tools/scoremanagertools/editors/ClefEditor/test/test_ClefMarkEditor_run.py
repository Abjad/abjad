# -*- encoding: utf-8 -*-
from abjad.tools import marktools
from experimental import *


def test_ClefEditor_run_01():

    editor = scoremanagertools.editors.ClefEditor()
    editor._run(pending_user_input='clef treble done')

    clef = marktools.Clef('treble')
    assert editor.target == clef
