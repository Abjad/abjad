# -*- encoding: utf-8 -*-
import pytest
from abjad import *
import scoremanager

# is_test=True is ok when testing the creation of views
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_DistributionFileWrangler_make_view_01():
    r'''Makes sure view creation menu title is correct.
    '''

    input_ = 'd vnew _test q' 
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    string = 'Score Manager - distribution files - views - _test - edit:'
    assert string in contents


def test_DistributionFileWrangler_make_view_02():
    r'''Makes sure at least one distribution file appears in 
    view creation menu.
    '''

    input_ = 'd vnew _test q' 
    score_manager._run(input_=input_)
    transcript = score_manager._transcript

    string = 'red-example-score.pdf (Red Example Score)'
    assert string in transcript.contents


def test_DistributionFileWrangler_make_view_03():
    r'''Makes view in library. Removes view.

    Makes sure no extra new lines appear before or after 
    'written to disk' message.
    '''
    pytest.skip('port me forward.')

    input_ = 'd vnew _test rm all'
    input_ += ' add red-example-score.pdf~(Red~Example~Score) done <return> q' 
    score_manager._run(input_=input_)

    lines =['> done', '']
    assert score_manager._transcript[-5].lines == lines

    lines = ['View inventory written to disk.', '']
    assert score_manager._transcript[-4].lines == lines
        
    input_ = 'd vls vrm _test <return> q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents
    assert 'found' in contents or 'found' in contents
    assert '_test' in contents

    input_ = 'd vls q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents
    assert 'found' in contents or 'found' in contents
    assert '_test' not in contents