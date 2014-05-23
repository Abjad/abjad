# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_BuildFileWrangler_remove_views_01():
    r'''Makes two views. Removes two views at one time.
    '''

    input_ = 'u vnew _test_100 rm all'
    input_ += ' add front-cover.pdf~(Red~Example~Score) done default' 
    input_ += ' u vnew _test_101 rm all'
    input_ += ' add back-cover.pdf~(Red~Example~Score) done default'
    input_ += ' q' 
    score_manager._run(input_=input_)

    input_ = 'u vls q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents
    assert 'views found' in contents
    assert '_test_100' in contents
    assert '_test_101' in contents

    input_ = 'u vrm _test_100-_test_101 default q'
    score_manager._run(input_=input_)

    input_ = 'u vls q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents
    assert 'view found' in contents or 'views found' in contents
    assert '_test_100' not in contents
    assert '_test_101' not in contents


def test_BuildFileWrangler_remove_views_02():
    r'''Makes sure selector backtracking works.
    '''

    input_ = 'u vrm b q'
    score_manager._run(input_=input_)

    titles = [
        'Score Manager - scores',
        'Score Manager - build files',
        'Score Manager - build files - select view(s) to remove:',
        'Score Manager - build files',
        ]
    assert score_manager._transcript.titles == titles