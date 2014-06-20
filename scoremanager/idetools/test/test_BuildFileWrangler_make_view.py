# -*- encoding: utf-8 -*-
import os
import pytest
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=False)
views_file = os.path.join(
    score_manager._configuration.wrangler_views_directory,
    '__BuildFileWrangler_views__.py',
    )
metadata_file = os.path.join(
    score_manager._configuration.wrangler_views_directory,
    '__metadata__.py',
    )


def test_BuildFileWrangler_make_view_01():
    r'''Makes sure view creation menu title is correct.
    '''

    input_ = 'U vnew _test q' 
    with systemtools.FilesystemState(keep=[views_file, metadata_file]):
        os.remove(metadata_file)
        score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    string = 'Abjad IDE - build files - views - _test (EDIT)'
    assert string in contents


def test_BuildFileWrangler_make_view_02():
    r'''Makes sure at least one build file appears in 
    view creation menu.
    '''

    input_ = 'U vnew _test q' 
    with systemtools.FilesystemState(keep=[views_file, metadata_file]):
        os.remove(metadata_file)
        score_manager._run(input_=input_)
    transcript = score_manager._transcript

    string = 'front-cover.pdf'
    assert string in transcript.contents


def test_BuildFileWrangler_make_view_03():
    r'''Makes view in library.
    '''

    input_ = 'U vnew _test rm all'
    input_ += ' add front-cover.pdf~(Red~Example~Score) done'
    input_ += ' vs _test q' 

    with systemtools.FilesystemState(keep=[views_file, metadata_file]):
        os.remove(metadata_file)
        score_manager._run(input_=input_)

    contents = score_manager._transcript.contents
    assert 'Abjad IDE - build files [_test]' in contents