# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager

# must be is_test=False to test views
score_manager = scoremanager.core.ScoreManager(is_test=False)


def test_BuildFileWrangler_clear_view_01():
    r'''In library: applies view and then clears view.

    Makes sure only one file is visible when view is applied.
    
    Then makes sure multiple files are visible once view is cleared.
    '''
    
    input_ = 'u vnew _test rm all'
    input_ += ' add segment-01.ly~(Red~Example~Score) done default'
    input_ += ' va _test vc vrm _test default q'
    score_manager._run(pending_input=input_)
    transcript = score_manager._transcript

    lines = [
        'Score manager - build files (_test)',
        '',
        '   1: segment-01.ly (Red Example Score)',
        '',
        '      files - copy (cp)',
        '      files - new (new)',
        '      files - remove (rm)',
        '      files - rename (ren)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)


def test_BuildFileWrangler_clear_view_02():
    r'''In single build directory: applies view and then clears view.

    Makes sure only one file is visible when view is applied.
    
    Then makes sure multiple files are visible once view is cleared.
    '''
    
    input_ = 'red~example~score u vnew _test rm all'
    input_ += ' add segment-01.ly done default'
    input_ += ' va _test vc vrm _test default q'
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