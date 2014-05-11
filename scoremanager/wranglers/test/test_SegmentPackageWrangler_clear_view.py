# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager

# must be is_test=False to test view application
score_manager = scoremanager.core.ScoreManager(is_test=False)


def test_SegmentPackageWrangler_clear_view_01():
    r'''Makes sure more than one segment is visible without view.
    '''
    
    input_ = 'g vnew _test rm all'
    input_ += ' add segment~01~(Red~Example~Score) done default'
    input_ += ' va _test vc vrm _test default q'
    score_manager._run(pending_input=input_)
    transcript = score_manager._transcript

    lines = [
        'Score manager - segments (_test)',
        '',
        '   1: segment 01 (Red Example Score)',
        '',
        '      segments - copy (cp)',
        '      segments - new (new)',
        '      segments - remove (rm)',
        '      segments - rename (ren)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)