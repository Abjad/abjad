# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_RestRhythmMakerEditor__run_01():

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.RestRhythmMakerEditor(session=session)
    input_ = 'q'
    editor._run(pending_user_input=input_, is_autoadvancing=True)

    maker = rhythmmakertools.RestRhythmMaker()
    assert editor.target == maker
