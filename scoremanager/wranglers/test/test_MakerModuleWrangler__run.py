# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MakerModuleWrangler__run_01():

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score k q'
    score_manager._run(pending_input=input_)
    contents = score_manager._transcript.contents

    string = '1: RedExampleScoreRhythmMaker.py'
    assert string in contents

    string = '2: RedExampleScoreTemplate.py'
    assert string in contents