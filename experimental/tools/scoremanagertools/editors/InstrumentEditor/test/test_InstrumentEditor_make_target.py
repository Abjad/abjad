# -*- encoding: utf-8 -*-
from experimental import *
from abjad import *


def test_InstrumentEditor_make_target_01():

    editor = scoremanagertools.editors.InstrumentEditor()
    editor._run(pending_user_input='cel q')
    assert editor.target == instrumenttools.Cello()
