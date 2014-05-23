# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager

# must be is_test=False for view tests
score_manager = scoremanager.core.ScoreManager(is_test=False)


def test_ScorePackageWrangler_apply_view_01():
    r'''Makes sure only select scores are visible.
    '''
    
    input_ = 'vnew _test rm all'
    input_ += ' add Red~Example~Score done <return>'
    input_ += ' vap _test vrm _test <return> q'
    score_manager._run(input_=input_)
    transcript = score_manager._transcript

    lines = [
        'Score Manager - scores (_test)',
        '',
        '   1: Red Example Score (2013)',
        '',
        '      scores - copy (cp)',
        '      scores - new (new)',
        '      scores - remove (rm)',
        '      scores - rename (ren)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)