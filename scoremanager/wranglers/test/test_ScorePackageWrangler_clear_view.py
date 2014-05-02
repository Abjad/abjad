# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager

# must be is_test=False to test views
score_manager = scoremanager.core.ScoreManager(is_test=False)


def test_ScorePackageWrangler_clear_view_01():
    r'''Applies view and then clears view.

    Makes sure only one score is visible when view is applied.
    
    Then makes sure multiple scores are visible once view is cleared.
    '''
    
    input_ = 'vnew _test rm all'
    input_ += ' add Red~Example~Score done default'
    input_ += ' va _test vc vrm _test default q'
    score_manager._run(pending_user_input=input_)
    with_view = score_manager._transcript[-10]
    without_view = score_manager._transcript[-8]

    lines = [
        'Score manager - scores (_test)',
        '',
        '   1: Red Example Score (2013)',
        '',
        '      scores - copy (cp)',
        '      scores - new (new)',
        '      scores - remove (rm)',
        '      scores - rename (ren)',
        '',
        ]
    assert with_view.lines == lines

    title = 'Score manager - scores'
    assert without_view.title == title

    lines = [
        'Red Example Score (2013)',
        'Blue Example Score (2013)',
        'Étude Example Score (2013)',
        ]

    contents = without_view.contents
    for line in lines:
        assert line in contents