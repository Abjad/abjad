# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_SegmentPackageWrangler_apply_view_01():
    
    input_ = 'red~example~score g q'
    score_manager._run(pending_user_input=input_)
    contents = score_manager._transcript.contents
    
    assert 'segment 01' in contents
    assert 'segment 02' in contents
    assert 'segment 03' in contents