# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
views_file = os.path.join(
    score_manager._configuration.wrangler_views_directory,
    '__DistributionFileWrangler_views__.py',
    )


def test_DistributionFileWrangler_remove_views_01():
    r'''Makes two views in library. Removes two views at one time.
    '''

    with systemtools.FilesystemState(keep=[views_file]):
        input_ = 'd vnew _test_100 rm all'
        input_ += ' add red-example-score.pdf~(Red~Example~Score) done'
        input_ += ' <return> d vnew _test_101 rm all'
        input_ += ' add'
        input_ += ' red-example-score-program-notes.pdf~(Red~Example~Score)'
        input_ += ' done <return>'
        input_ += ' q' 
        score_manager._run(input_=input_)

        input_ = 'd vae q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents
        assert '_test_100' in contents
        assert '_test_101' in contents

        input_ = 'd vrm _test_100-_test_101 <return> q'
        score_manager._run(input_=input_)

        input_ = 'd vae q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents
        assert '_test_100' not in contents
        assert '_test_101' not in contents


def test_DistributionFileWrangler_remove_views_02():
    r'''Makes sure selector backtracking works.
    '''

    with systemtools.FilesystemState(keep=[views_file]):
        input_ = 'd vrm b q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents

    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - distribution files',
        'Abjad IDE - distribution files',
        'Abjad IDE - distribution files',
        ]
    assert score_manager._transcript.titles == titles
    assert 'Select view(s) to remove:' in contents