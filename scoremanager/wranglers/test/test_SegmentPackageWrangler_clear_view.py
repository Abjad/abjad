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
    with_view = score_manager._transcript[-10]
    without_view = score_manager._transcript[-8]

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
    assert with_view.lines == lines

    title = 'Score manager - segments'
    assert without_view.title == title

    string = 'segment 01 (Red Example Score)'
    assert string in without_view.contents

    string = 'segment 02 (Red Example Score)'
    assert string in without_view.contents