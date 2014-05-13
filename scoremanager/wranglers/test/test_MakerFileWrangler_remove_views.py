# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MakerFileWrangler_remove_views_01():
    r'''Makes two views. Removes two views at one time.
    '''

    input_ = 'k vnew _test_100 rm all'
    input_ += ' add RedExampleScoreTemplate.py~(Red~Example~Score)'
    input_ += ' done default' 
    input_ += ' k vnew _test_101 rm all'
    input_ += ' add RedExampleScoreRhythmMaker.py~(Red~Example~Score)'
    input_ += ' done default'
    input_ += ' q' 
    score_manager._run(pending_input=input_)

    input_ = 'k vls q'
    score_manager._run(pending_input=input_)
    contents = score_manager._transcript.contents
    assert 'views found' in contents
    assert '_test_100' in contents
    assert '_test_101' in contents

    input_ = 'k vrm _test_100-_test_101 default q'
    score_manager._run(pending_input=input_)

    input_ = 'k vls q'
    score_manager._run(pending_input=input_)
    contents = score_manager._transcript.contents
    assert 'view found' in contents or 'views found' in contents
    assert '_test_100' not in contents
    assert '_test_101' not in contents


def test_MakerFileWrangler_remove_views_02():
    r'''Makes sure selector backtracking works.
    '''

    input_ = 'k vrm b q'
    score_manager._run(pending_input=input_)

    titles = [
        'Score manager - example scores',
        'Score manager - maker files',
        'Score manager - maker files - select view(s) to remove:',
        'Score manager - maker files',
        ]
    assert score_manager._transcript.titles == titles