# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_NoteRhythmMakerEditor__run_01():

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.NoteRhythmMakerEditor(session=session)
    input_ = 'q'
    editor._run(pending_user_input=input_, is_autoadvancing=True)

    maker = rhythmmakertools.NoteRhythmMaker()

    assert editor.target == maker
