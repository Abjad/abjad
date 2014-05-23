# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_DistributionFileWrangler_quit_01():
    
    input_ = 'red~example~score d q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert contents


def test_DistributionFileWrangler_quit_02():
    
    input_ = 'd q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert contents