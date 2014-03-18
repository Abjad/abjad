# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_InstrumentEditor_make_target_01():

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.InstrumentEditor(session=session)
    input_ = 'cel q'
    editor._run(pending_user_input=input_)
    assert editor.target == instrumenttools.Cello()
