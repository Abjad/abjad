# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_NoteRhythmMakerEditor__run_01():

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.NoteRhythmMakerEditor
    editor = editor(session=session, is_autoadvancing=True)
    input_ = 'q'
    editor._run(pending_user_input=input_)

    maker = rhythmmakertools.NoteRhythmMaker()

    assert editor.target == maker