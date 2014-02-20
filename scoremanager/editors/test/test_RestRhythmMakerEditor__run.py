# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_RestRhythmMakerEditor__run_01():

    editor = scoremanager.editors.RestRhythmMakerEditor()
    editor._run(pending_user_input='q', is_autoadvancing=True)

    maker = rhythmmakertools.RestRhythmMaker()

    assert editor.target == maker
