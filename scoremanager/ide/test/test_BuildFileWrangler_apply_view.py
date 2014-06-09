# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
# must be is_test=False for view tests
score_manager = scoremanager.ide.AbjadIDE(is_test=False)
views_file = os.path.join(
    score_manager._configuration.wrangler_views_directory,
    '__BuildFileWrangler_views__.py',
    )


def test_BuildFileWrangler_apply_view_01():
    r'''Works in library.
    
    Makes sure only select build files are visible.
    '''
    
    with systemtools.FilesystemState(keep=[views_file]):
        input_ = 'u vnew _test rm all'
        input_ += ' add segment-01.ly~(Red~Example~Score)'
        input_ += ' add segment-02.ly~(Red~Example~Score)'
        input_ += ' add segment-03.ly~(Red~Example~Score) done <return>'
        input_ += ' vap _test vrm _test <return> q'
        score_manager._run(input_=input_)
        transcript = score_manager._transcript
        lines = [
            'Abjad IDE - build files [_test]',
            '',
            '   1: segment-01.ly (Red Example Score)',
            '   2: segment-02.ly (Red Example Score)',
            '   3: segment-03.ly (Red Example Score)',
            '',
            '      files - copy (cp)',
            '      files - new (new)',
            '      files - remove (rm)',
            '      files - rename (ren)',
            '',
            ]
        assert any(_.lines == lines for _ in transcript)


def test_BuildFileWrangler_apply_view_02():
    r'''Works in score package build directory.
    
    Makes sure only select build file is visible.
    '''
    
    with systemtools.FilesystemState(keep=[views_file]):
        input_ = 'red~example~score u vnew _test rm all'
        input_ += ' add segment-01.ly done <return>'
        input_ += ' vap _test vrm _test <return> q'
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