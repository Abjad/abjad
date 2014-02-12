# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_NoteRhythmMakerEditor_01():

    editor = scoremanager.editors.NoteRhythmMakerEditor()
    editor._run(pending_user_input='q', is_autoadvancing=True)

    maker = rhythmmakertools.NoteRhythmMaker()

    assert editor.target == maker
