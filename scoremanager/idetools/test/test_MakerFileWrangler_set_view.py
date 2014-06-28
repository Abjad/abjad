# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
# must be is_test=False for view tests
ide = scoremanager.idetools.AbjadIDE(is_test=False)


def test_MakerFileWrangler_set_view_01():
    r'''Works in library.
    
    Makes sure only select maker file is visible.
    '''
    
    views_file = os.path.join(
        ide._configuration.wrangler_views_directory,
        '__MakerFileWrangler_views__.py',
        )
    metadata_file = os.path.join(
        ide._configuration.wrangler_views_directory,
        '__metadata__.py',
        )
    with systemtools.FilesystemState(keep=[views_file, metadata_file]):
        os.remove(views_file)
        os.remove(metadata_file)
        input_ = 'K va add _test'
        input_ += ' add RedExampleScoreTemplate.py~(Red~Example~Score)'
        input_ += ' done done'
        input_ += ' vs _test q'
        ide._run(input_=input_)
        transcript = ide._transcript

        lines = [
            'Abjad IDE - maker files [_test]',
            '',
            '    Red Example Score:',
            '       1: RedExampleScoreTemplate.py',
            '',
            '      files - copy (cp)',
            '      files - new (new)',
            '      files - remove (rm)',
            '      files - rename (ren)',
            '',
            ]
        assert any(_.lines == lines for _ in transcript)


def test_MakerFileWrangler_set_view_02():
    r'''Works in score package makers directory.
    
    Makes sure only select maker file is visible.
    '''
    
    views_file = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'makers',
        '__views__.py',
        )
    metadata_file = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'makers',
        '__metadata__.py',
        )
    with systemtools.FilesystemState(keep=[views_file, metadata_file]):
        os.remove(views_file)
        os.remove(metadata_file)
        input_ = 'red~example~score k va add _test'
        input_ += ' add RedExampleScoreTemplate.py done done'
        input_ += ' vs _test q'
        ide._run(input_=input_)
        transcript = ide._transcript

        lines = [
            'Red Example Score (2013) - maker files [_test]',
            '',
            '   1: RedExampleScoreTemplate.py',
            '',
            '      files - copy (cp)',
            '      files - new (new)',
            '      files - remove (rm)',
            '      files - rename (ren)',
            '',
            ]
        assert any(_.lines == lines for _ in transcript)