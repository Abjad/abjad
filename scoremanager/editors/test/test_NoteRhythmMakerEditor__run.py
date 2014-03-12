# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_NoteRhythmMakerEditor__run_01():

    session = scoremanager.core.Session()
    editor = scoremanager.editors.NoteRhythmMakerEditor(session=session)
    editor._run(pending_user_input='q', is_autoadvancing=True)

    maker = rhythmmakertools.NoteRhythmMaker()

    assert editor.target == maker
