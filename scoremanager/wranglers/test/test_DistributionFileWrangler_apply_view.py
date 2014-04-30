# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager

# must be is_test=False for view tests
score_manager = scoremanager.core.ScoreManager(is_test=False)


def test_DistributionFileWrangler_apply_view_01():
    r'''Applies view to library.
    
    Makes sure only select distribution file is visible.
    '''
    
    input_ = 'd vnew _test rm all'
    input_ += ' add red-example-score.pdf~(Red~Example~Score) done default'
    input_ += ' va _test vrm _test default q'
    score_manager._run(pending_user_input=input_)
    applied_view = score_manager._transcript[-8]

    lines = [
        'Score manager - distribution files (_test)',
        '',
        '   1: red-example-score.pdf (Red Example Score)',
        '',
        '      files - copy (cp)',
        '      files - new (new)',
        '      files - remove (rm)',
        '      files - rename (ren)',
        '',
        ]
    assert applied_view.lines == lines


def test_DistributionFileWrangler_apply_view_02():
    r'''Applies view to single view directory.
    
    Makes sure only select distribution file are visible.

    Must use explicit (ssx) to manage example score when
    is_test=False.
    '''
    
    input_ = 'ssx red~example~score d vnew _test rm all'
    input_ += ' add red-example-score.pdf done default'
    input_ += ' va _test vrm _test default q'
    score_manager._run(pending_user_input=input_)
    applied_view = score_manager._transcript[-8]

    lines = [
        'Red Example Score (2013) - distribution files (_test)',
        '',
        '   1: red-example-score.pdf',
        '',
        '      files - copy (cp)',
        '      files - new (new)',
        '      files - remove (rm)',
        '      files - rename (ren)',
        '',
        ]
    assert applied_view.lines == lines