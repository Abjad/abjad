# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager

# must be is_test=False to test views
score_manager = scoremanager.core.ScoreManager(is_test=False)


def test_DistributionFileWrangler_clear_view_01():
    r'''In library: applies view and then clears view.

    Makes sure only one file is visible when view is applied.
    
    Then makes sure multiple files are visible once view is cleared.
    '''
    
    input_ = 'd vnew _test rm all'
    input_ += ' add red-example-score.pdf~(Red~Example~Score) done default'
    input_ += ' va _test vc vrm _test default q'
    score_manager._run(pending_user_input=input_)
    with_view = score_manager._transcript[-10]
    without_view = score_manager._transcript[-8]

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
    assert with_view.lines == lines

    title = 'Score manager - distribution files'
    assert without_view.title == title

    lines = [
        'red-example-score.pdf (Red Example Score)',
        'temporary-red-example-score.txt (Red Example Score)',
        ]

    contents = without_view.contents
    for line in lines:
        assert line in contents


def test_DistributionFileWrangler_clear_view_02():
    r'''In score package distribution directory: 
    applies view and then clears view.

    Makes sure only one file is visible when view is applied.
    
    Then makes sure multiple files are visible once view is cleared.

    Use explicit (ssx) to manage example scores when is_test=False.
    '''
    
    input_ = 'ssx red~example~score d vnew _test rm all'
    input_ += ' add red-example-score.pdf done default'
    input_ += ' va _test vc vrm _test default q'
    score_manager._run(pending_user_input=input_)
    with_view = score_manager._transcript[-10]
    without_view = score_manager._transcript[-8]

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
    assert with_view.lines == lines

    title = 'Red Example Score (2013) - distribution files'
    assert without_view.title == title

    lines = [
        'red-example-score.pdf',
        'temporary-red-example-score.txt',
        ]

    contents = without_view.contents
    for line in lines:
        assert line in contents