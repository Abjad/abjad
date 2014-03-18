# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ClefEditor__run_01():

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.ClefEditor(session=session)
    input_ = 'clef treble done'
    editor._run(pending_user_input=input_)

    clef = indicatortools.Clef('treble')
    assert editor.target == clef
