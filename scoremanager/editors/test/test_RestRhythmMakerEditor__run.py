# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_RestRhythmMakerEditor__run_01():

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.RestRhythmMakerEditor
    editor = editor(session=session, is_autoadvancing=True)
    input_ = 'q'
    editor._run(pending_user_input=input_)

    maker = rhythmmakertools.RestRhythmMaker()
    assert editor.target == maker