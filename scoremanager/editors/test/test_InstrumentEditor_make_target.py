# -*- encoding: utf-8 -*-
from experimental import *


def test_InstrumentEditor_make_target_01():

    editor = scoremanager.editors.InstrumentEditor()
    editor._run(pending_user_input='cel q')
    assert editor.target == instrumenttools.Cello()
