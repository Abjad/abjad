# -*- encoding: utf-8 -*-
from experimental import *


def test_RhythmMakerClassNameSelector_run_01():

    selector = scoremanagertools.selectors.RhythmMakerClassNameSelector()

    assert selector._run(pending_user_input='note') == 'NoteRhythmMaker'
