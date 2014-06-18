# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
# must be is_test=False for view tests
score_manager = scoremanager.idetools.AbjadIDE(is_test=False)


def test_DistributionFileWrangler_set_view_01():
    r'''Applies view to library.
    
    Makes sure only select distribution file is visible.
    '''

    views_file = os.path.join(
        score_manager._configuration.wrangler_views_directory,
        '__DistributionFileWrangler_views__.py',
        )
    metadata_file = os.path.join(
        score_manager._configuration.wrangler_views_directory,
        '__metadata__.py',
        )
    with systemtools.FilesystemState(keep=[views_file, metadata_file]):
        input_ = 'D vnew _test rm all'
        input_ += ' add red-example-score.pdf~(Red~Example~Score) done'
        input_ += ' <return> vs _test vrm _test <return> q'
        score_manager._run(input_=input_)
        transcript = score_manager._transcript
        lines = [
            'Abjad IDE - distribution files [_test]',
            '',
            '    Red Example Score:',
            '       1: red-example-score.pdf',
            '',
            '      files - copy (cp)',
            '      files - new (new)',
            '      files - remove (rm)',
            '      files - rename (ren)',
            '',
            ]
        assert any(_.lines == lines for _ in transcript)


def test_DistributionFileWrangler_set_view_02():
    r'''Applies view to single view directory.
    
    Makes sure only select distribution file are visible.
    '''
    
    views_file = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        'distribution',
        '__views__.py',
        )
    metadata_file = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        'distribution',
        '__metadata__.py',
        )
    with systemtools.FilesystemState(keep=[views_file, metadata_file]):
        input_ = 'red~example~score d vnew _test rm all'
        input_ += ' add red-example-score.pdf done <return>'
        input_ += ' vs _test vrm _test <return> q'
        score_manager._run(input_=input_)
        transcript = score_manager._transcript
        lines = [
            'Red Example Score (2013) - distribution files [_test]',
            '',
            '   1: red-example-score.pdf',
            '',
            '      files - copy (cp)',
            '      files - new (new)',
            '      files - remove (rm)',
            '      files - rename (ren)',
            '',
            ]
        assert any(_.lines == lines for _ in transcript)