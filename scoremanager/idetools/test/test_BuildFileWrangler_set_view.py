# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
# must be is_test=False for view tests
score_manager = scoremanager.idetools.AbjadIDE(is_test=False)


def test_BuildFileWrangler_set_view_01():
    r'''Works in library.
    
    Makes sure only select build files are visible.
    '''
    
    views_file = os.path.join(
        score_manager._configuration.wrangler_views_directory,
        '__BuildFileWrangler_views__.py',
        )
    metadata_file = os.path.join(
        score_manager._configuration.wrangler_views_directory,
        '__metadata__.py',
        )
    with systemtools.FilesystemState(keep=[views_file, metadata_file]):
        os.remove(metadata_file)
        input_ = 'U vnew _test rm all'
        input_ += ' add segment-01.ly~(Red~Example~Score)'
        input_ += ' add segment-02.ly~(Red~Example~Score)'
        input_ += ' add segment-03.ly~(Red~Example~Score) done'
        input_ += ' vs _test vrm _test q'
        score_manager._run(input_=input_)
        transcript = score_manager._transcript
        lines = [
            'Abjad IDE - build files [_test]',
            '',
            '    Red Example Score:',
            '       1: segment-01.ly',
            '       2: segment-02.ly',
            '       3: segment-03.ly',
            '',
            '      files - copy (cp)',
            '      files - new (new)',
            '      files - remove (rm)',
            '      files - rename (ren)',
            '',
            ]
        assert any(_.lines == lines for _ in transcript)


def test_BuildFileWrangler_set_view_02():
    r'''Works in score package build directory.
    
    Makes sure only select build file is visible.
    '''
    
    views_file = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        'build',
        '__views__.py',
        )
    metadata_file = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        'build',
        '__metadata__.py',
        )
    with systemtools.FilesystemState(keep=[views_file, metadata_file]):
        os.remove(metadata_file)
        input_ = 'red~example~score u vnew _test rm all'
        input_ += ' add segment-01.ly done'
        input_ += ' vs _test vrm _test q'
        score_manager._run(input_=input_)
        transcript = score_manager._transcript
        lines = [
            'Red Example Score (2013) - build files [_test]',
            '',
            '   1: segment-01.ly',
            '',
            '      files - copy (cp)',
            '      files - new (new)',
            '      files - remove (rm)',
            '      files - rename (ren)',
            '',
            ]
        assert any(_.lines == lines for _ in transcript)