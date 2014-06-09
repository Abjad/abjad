# -*- encoding: utf-8 -*-
import os
import pytest
from abjad import *
import scoremanager
# is_test=True is ok when testing the creation of views
score_manager = scoremanager.core.AbjadIDE(is_test=True)
views_file = os.path.join(
    score_manager._configuration.wrangler_views_directory,
    '__BuildFileWrangler_views__.py',
    )


def test_BuildFileWrangler_make_view_01():
    r'''Makes sure view creation menu title is correct.
    '''

    input_ = 'u vnew _test q' 
    with systemtools.FilesystemState(keep=[views_file]):
        score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    string = 'Abjad IDE - build files - views - _test (EDIT)'
    assert string in contents


def test_BuildFileWrangler_make_view_02():
    r'''Makes sure at least one build file appears in 
    view creation menu.
    '''

    input_ = 'u vnew _test q' 
    with systemtools.FilesystemState(keep=[views_file]):
        score_manager._run(input_=input_)
    transcript = score_manager._transcript

    string = 'front-cover.pdf (Red Example Score)'
    assert string in transcript.contents


def test_BuildFileWrangler_make_view_03():
    r'''Makes view in library. Removes view.

    Makes sure no extra new lines appear before or after 
    'written to disk' message.
    '''
    pytest.skip('fix me')

    input_ = 'u vnew _test rm all'
    input_ += ' add front-cover.pdf~(Red~Example~Score) done q' 
    with systemtools.FilesystemState(keep=[views_file]):
        score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert 'Abjad IDE - build files [_test]' in contents

    input_ = 'u vae b vrm _test <return> q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents
    assert 'found' in contents or 'found' in contents
    assert '_test' in contents

    input_ = 'u vae q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents
    assert 'found' in contents or 'found' in contents
    assert '_test' not in contents