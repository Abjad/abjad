# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager

# must be is_test=False to test views
score_manager = scoremanager.core.ScoreManager(is_test=False)


def test_MaterialPackageWrangler_clear_view_01():
    r'''Works in library.
    
    Applies view and then clears view.

    Makes sure only one file is visible when view is applied.
    
    Then makes sure multiple files are visible once view is cleared.
    '''
    
    input_ = 'm vnew _test rm all'
    input_ += ' add instrumentation~(Red~Example~Score) done default'
    input_ += ' va _test vc vrm _test default q'
    score_manager._run(pending_input=input_)
    transcript = score_manager._transcript

    lines = [
        'Score manager - materials (_test)',
        '',
        '   1: instrumentation (Red Example Score)',
        '',
        '      materials - copy (cp)',
        '      materials - new (new)',
        '      materials - remove (rm)',
        '      materials - rename (ren)',
        '',
        ]
    assert any(_.lines for _ in transcript)


def test_MaterialPackageWrangler_clear_view_02():
    r'''Works in score.

    Applies view and then clears view.

    Makes sure only one material package is visible when view is applied.
    
    Then makes sure multiple material packages are visible once view is 
    cleared.
    '''
    
    input_ = 'red~example~score m vnew _test rm all'
    input_ += ' add instrumentation done default'
    input_ += ' va _test vc vrm _test default q'
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
    assert any(_.lines for _ in transcript)