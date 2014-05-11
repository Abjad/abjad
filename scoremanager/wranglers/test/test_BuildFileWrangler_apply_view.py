# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager

# must be is_test=False for view tests
score_manager = scoremanager.core.ScoreManager(is_test=False)


def test_BuildFileWrangler_apply_view_01():
    r'''Works in library.
    
    Makes sure only select build files are visible.
    '''
    
    input_ = 'u vnew _test rm all'
    input_ += ' add segment-01.ly~(Red~Example~Score)'
    input_ += ' add segment-02.ly~(Red~Example~Score)'
    input_ += ' add segment-03.ly~(Red~Example~Score) done default'
    input_ += ' va _test vrm _test default q'
    score_manager._run(pending_input=input_)
    transcript = score_manager._transcript

    lines = [
        'Score manager - build files (_test)',
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
    
    input_ = 'red~example~score u vnew _test rm all'
    input_ += ' add segment-01.ly done default'
    input_ += ' va _test vrm _test default q'
    score_manager._run(pending_input=input_)
    transcript = score_manager._transcript

    lines = [
        'Red Example Score (2013) - build files (_test)',
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