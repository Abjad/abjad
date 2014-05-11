# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager

# is_test=True is ok when testing the creation of views
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MaterialPackageWrangler_make_view_01():
    r'''Makes sure view creation menu title is correct.
    '''

    input_ = 'm vnew _test q' 
    score_manager._run(pending_input=input_)
    transcript = score_manager._transcript

    string = 'Score manager - materials - views - _test - edit:'
    assert transcript.last_title == string


def test_MaterialPackageWrangler_make_view_02():
    r'''Makes sure at least one package appears in 
    view creation menu.
    '''

    input_ = 'm vnew _test q' 
    score_manager._run(pending_input=input_)
    transcript = score_manager._transcript

    string = 'instrumentation (Red Example Score)'
    assert string in transcript.contents


def test_MaterialPackageWrangler_make_view_03():
    r'''Makes sure numeric entry during view creation does not
    raise an exception.
    '''

    input_ = 'red~example~score m vnew _test 1 q' 
    score_manager._run(pending_input=input_)

    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials',
        'Red Example Score (2013) - materials - views - _test - edit:',
        'Red Example Score (2013) - materials - views - _test - edit:',
        ]
    assert score_manager._transcript.titles == titles


def test_MaterialPackageWrangler_make_view_04():
    r'''Makes view in library. Removes view.

    Makes sure no extra new lines appear before or after 
    'written to disk' message.
    '''

    input_ = 'm vnew _test rm all'
    input_ += ' add instrumentation~(Red~Example~Score) done default q' 
    score_manager._run(pending_input=input_)

    lines =['> done', '']
    assert score_manager._transcript[-5].lines == lines

    lines = ['View inventory written to disk.', '']
    assert score_manager._transcript[-4].lines == lines
        
    input_ = 'm vls vrm _test default q'
    score_manager._run(pending_input=input_)
    contents = score_manager._transcript.contents
    assert 'view found' in contents or 'views found' in contents
    assert '_test' in contents

    input_ = 'm vls q'
    score_manager._run(pending_input=input_)
    contents = score_manager._transcript.contents
    assert 'view found' in contents or 'views found' in contents
    assert '_test' not in contents