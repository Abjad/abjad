# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_InstrumentEditor_make_target_01():

    session = scoremanager.core.Session()
    editor = scoremanager.editors.InstrumentEditor(session=session)
    editor._run(pending_user_input='cel q')
    assert editor.target == instrumenttools.Cello()
