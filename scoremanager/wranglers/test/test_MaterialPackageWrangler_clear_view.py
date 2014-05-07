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
    with_view = score_manager._transcript[-10]
    without_view = score_manager._transcript[-8]

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
    assert with_view.lines == lines

    title = 'Score manager - materials'
    assert without_view.title == title

    lines = [
        'instrumentation (Red Example Score)',
        'magic numbers (Red Example Score)',
        'pitch range inventory (Red Example Score)',
        'tempo inventory (Red Example Score)',
        ]

    contents = without_view.contents
    for line in lines:
        assert line in contents


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
    with_view = score_manager._transcript[-10]
    without_view = score_manager._transcript[-8]

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
    assert with_view.lines == lines

    title = 'Red Example Score (2013) - materials'
    assert without_view.title == title

    lines = [
        'instrumentation',
        'magic numbers',
        'pitch range inventory',
        'tempo inventory',
        ]

    contents = without_view.contents
    for line in lines:
        assert line in contents