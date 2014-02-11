# -*- encoding: utf-8 -*-
from experimental import *


def test_NoteRhythmMakerEditor_01():

    editor = scoremanagertools.editors.NoteRhythmMakerEditor()
    editor._run(pending_user_input='q', is_autoadvancing=True)

    maker = rhythmmakertools.NoteRhythmMaker()

    assert editor.target == maker
