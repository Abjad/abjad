# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MakerFileWrangler_quit_01():
    
    input_ = 'red~example~score k q'
    score_manager._run(pending_input=input_)
    contents = score_manager._transcript.contents

    assert contents


def test_MakerFileWrangler_quit_02():
    
    input_ = 'k q'
    score_manager._run(pending_input=input_)
    contents = score_manager._transcript.contents

    assert contents