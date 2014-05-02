# -*- encoding: utf-8 -*-
import pytest
pytest.skip('make me work')
from abjad import *
import scoremanager

# must be is_test=False for view tests
score_manager = scoremanager.core.ScoreManager(is_test=False)


def test_ScorePackageWrangler_apply_view_01():
    r'''Makes sure only select scores are visible.
    '''
    
    input_ = 'vnew _test rm all'
    input_ += ' add Red~Example~Score done default'
    input_ += ' va _test vrm _test default q'
    score_manager._run(pending_user_input=input_)
    applied_view = score_manager._transcript[-8]

    lines = [
        'Score manager - example scores (_test)',
        '',
        '   1: Red Example Score (2013)',
        '',
        '      scores - copy (cp)',
        '      scores - new (new)',
        '      scores - remove (rm)',
        '      scores - rename (ren)',
        '',
        ]
    assert applied_view.lines == lines