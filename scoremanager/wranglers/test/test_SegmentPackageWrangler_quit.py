# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_SegmentPackageWrangler_quit_01():
    
    input_ = 'red~example~score g q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert contents


def test_SegmentPackageWrangler_quit_02():
    
    input_ = 'g q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert contents