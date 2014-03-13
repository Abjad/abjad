# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ClefEditor__run_01():

    session = scoremanager.core.Session()
    editor = scoremanager.editors.ClefEditor(session=session)
    editor._run(pending_user_input='clef treble done')

    clef = indicatortools.Clef('treble')
    assert editor.target == clef
