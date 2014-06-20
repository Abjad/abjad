# -*- encoding: utf-8 -*-
import os
import pytest
from abjad import *
import scoremanager
# is_test=True is ok when testing the creation of views
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
views_file = os.path.join(
    score_manager._configuration.wrangler_views_directory,
    '__ScorePackageWrangler_views__.py',
    )
metadata_file = os.path.join(
    score_manager._configuration.wrangler_views_directory,
    '__metadata__.py',
    )


def test_ScorePackageWrangler_make_view_01():
    r'''Makes sure view creation menu title is correct.
    '''

    with systemtools.FilesystemState(keep=[views_file, metadata_file]):
        os.remove(metadata_file)
        input_ = 'vnew _test q' 
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents
        string = 'Abjad IDE - scores - views - _test (EDIT)'
        assert string in contents


def test_ScorePackageWrangler_make_view_02():
    r'''Makes sure at least one score appears in view creation menu.
    '''

    with systemtools.FilesystemState(keep=[views_file, metadata_file]):
        os.remove(metadata_file)
        input_ = 'vnew _test q' 
        score_manager._run(input_=input_)
        transcript = score_manager._transcript
        string = 'Red Example Score'
        assert string in transcript.contents


def test_ScorePackageWrangler_make_view_03():
    r'''Makes view. Removes view.

    Makes sure no extra new lines appear before or after 
    'written to disk' message.
    '''
    pytest.skip('port me forward.')

    with systemtools.FilesystemState(keep=[views_file, metadata_file]):
        os.remove(metadata_file)
        input_ = 'vnew _test rm all'
        input_ += ' add Red~Example~Score done q' 
        score_manager._run(input_=input_)

        lines =['> done', '']
        assert score_manager._transcript[-5].lines == lines

        lines = ['View inventory written to disk.', '']
        assert score_manager._transcript[-4].lines == lines
            
        input_ = 'va b vrm _test q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents
        assert 'found' in contents or 'found' in contents
        assert '_test' in contents

        input_ = 'va q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents
        assert 'found' in contents or 'found' in contents
        assert '_test' not in contents