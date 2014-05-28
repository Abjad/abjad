# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_DistributionFileWrangler_remove_views_01():
    r'''Makes two views in library. Removes two views at one time.
    '''

    input_ = 'd vnew _test_100 rm all'
    input_ += ' add red-example-score.pdf~(Red~Example~Score) done <return>' 
    input_ += ' d vnew _test_101 rm all'
    input_ += ' add red-example-score-program-notes.pdf~(Red~Example~Score)'
    input_ += ' done <return>'
    input_ += ' q' 
    score_manager._run(input_=input_)

    input_ = 'd vls q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents
    assert 'found' in contents
    assert '_test_100' in contents
    assert '_test_101' in contents

    input_ = 'd vrm _test_100-_test_101 <return> q'
    score_manager._run(input_=input_)

    input_ = 'd vls q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents
    assert 'found' in contents or 'found' in contents
    assert '_test_100' not in contents
    assert '_test_101' not in contents


def test_DistributionFileWrangler_remove_views_02():
    r'''Makes sure selector backtracking works.
    '''

    input_ = 'd vrm b q'
    score_manager._run(input_=input_)

    titles = [
        'Score Manager - scores',
        'Score Manager - distribution files',
        'Score Manager - distribution files - select view(s) to remove:',
        'Score Manager - distribution files',
        ]
    assert score_manager._transcript.titles == titles