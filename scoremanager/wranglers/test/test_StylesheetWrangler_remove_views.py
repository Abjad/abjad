# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_StylesheetWrangler_remove_views_01():
    r'''Makes two views. Removes two views at one time.
    '''

    input_ = 'y vnew _test_100 rm all add clean-letter-14.ily done default' 
    input_ += ' y vnew _test_101 rm all add clean-letter-16.ily done default'
    input_ += ' q' 
    score_manager._run(pending_user_input=input_)

    input_ = 'y vls q'
    score_manager._run(pending_user_input=input_)
    contents = score_manager._transcript.contents
    assert 'views found' in contents
    assert '_test_100' in contents
    assert '_test_101' in contents

    input_ = 'y vrm _test_100-_test_101 default q'
    score_manager._run(pending_user_input=input_)

    input_ = 'y vls q'
    score_manager._run(pending_user_input=input_)
    contents = score_manager._transcript.contents
    assert 'view found' in contents or 'views found' in contents
    assert '_test_100' not in contents
    assert '_test_101' not in contents


def test_StylesheetWrangler_remove_views_02():
    r'''Makes sure selector backtracking works.
    '''

    input_ = 'y vrm b q'
    score_manager._run(pending_user_input=input_)

    titles = [
        'Score manager - example scores',
        'Score manager - stylesheet library',
        'Score manager - stylesheet library - select view(s) to remove:',
        'Score manager - stylesheet library',
        ]
    assert score_manager._transcript.titles == titles