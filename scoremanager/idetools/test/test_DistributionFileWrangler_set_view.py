# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_DistributionFileWrangler_set_view_01():
    r'''Applies view to library.
    
    Makes sure only select distribution file is visible.
    '''

    views_file = os.path.join(
        ide._configuration.wrangler_views_directory,
        '__DistributionFileWrangler_views__.py',
        )
    with systemtools.FilesystemState(keep=[views_file]):
        os.remove(views_file)
        input_ = 'dd wa add _test'
        input_ += ' add red-example-score.pdf~(Red~Example~Score) done done'
        input_ += ' ws _test q'
        ide._run(input_=input_)
        transcript = ide._transcript
        lines = [
            'Abjad IDE - distribution depot [_test]',
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
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'distribution',
        '__views__.py',
        )
    metadata_file = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'distribution',
        '__metadata__.py',
        )
    with systemtools.FilesystemState(keep=[views_file, metadata_file]):
        os.remove(views_file)
        os.remove(metadata_file)
        input_ = 'red~example~score d wa add _test'
        input_ += ' add red-example-score.pdf done done'
        input_ += ' ws _test q'
        ide._run(input_=input_)
        transcript = ide._transcript
        lines = [
            'Red Example Score (2013) - distribution directory [_test]',
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