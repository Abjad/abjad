# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager

# must be is_test=False for view tests
score_manager = scoremanager.core.ScoreManager(is_test=False)


def test_MaterialPackageWrangler_apply_view_01():
    r'''Works in library.
    
    Makes sure only select material packages are visible.
    '''
    
    input_ = 'm vnew _test rm all'
    input_ += ' add instrumentation~(Red~Example~Score)'
    input_ += ' add tempo~inventory~(Red~Example~Score) done default'
    input_ += ' va _test vrm _test default q'
    score_manager._run(pending_input=input_)
    transcript = score_manager._transcript

    lines = [
        'Score manager - materials (_test)',
        '',
        '   1: instrumentation (Red Example Score)',
        '   2: tempo inventory (Red Example Score)',
        '',
        '      materials - copy (cp)',
        '      materials - new (new)',
        '      materials - remove (rm)',
        '      materials - rename (ren)',
        '',
        ]
    assert any(_.lines for _ in transcript)


def test_MaterialPackageWrangler_apply_view_02():
    r'''Works in score.
    
    Makes sure only select material package is visible.
    '''
    
    input_ = 'red~example~score m vnew _test rm all'
    input_ += ' add instrumentation done default'
    input_ += ' va _test vrm _test default q'
    score_manager._run(pending_input=input_)
    transcript = score_manager._transcript

    lines = [
        'Red Example Score (2013) - materials (_test)',
        '',
        '   1: instrumentation',
        '',
        '      materials - copy (cp)',
        '      materials - new (new)',
        '      materials - remove (rm)',
        '      materials - rename (ren)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)