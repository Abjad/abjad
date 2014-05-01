# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager

# must be is_test=False to test views
score_manager = scoremanager.core.ScoreManager(is_test=False)


def test_MakerModuleWrangler_clear_view_01():
    r'''In library: applies view and then clears view.

    Makes sure only one maker module is visible when view is applied.
    
    Then makes sure multiple files are visible once view is cleared.
    '''
    
    input_ = 'k vnew _test rm all'
    input_ += ' add RedExampleScoreTemplate.py~(Red~Example~Score)'
    input_ += ' done default'
    input_ += ' va _test vc vrm _test default q'
    score_manager._run(pending_user_input=input_)
    with_view = score_manager._transcript[-10]
    without_view = score_manager._transcript[-8]

    lines = [
        'Score manager - maker modules (_test)',
        '',
        '   1: RedExampleScoreTemplate.py (Red Example Score)',
        '',
        '      maker modules - copy (cp)',
        '      maker modules - new (new)',
        '      maker modules - remove (rm)',
        '      maker modules - rename (ren)',
        '',
        ]
    assert with_view.lines == lines

    title = 'Score manager - maker modules'
    assert without_view.title == title

    lines = [
        'RedExampleScoreTemplate.py (Red Example Score)',
        'RedExampleScoreRhythmMaker.py (Red Example Score)',
        ]

    contents = without_view.contents
    for line in lines:
        assert line in contents


def test_MakerModuleWrangler_clear_view_02():
    r'''In single makers directory: applies view and then clears view.

    Makes sure only one maker module is visible when view is applied.
    
    Then makes sure multiple maker modules are visible once view is cleared.

    Use explicit (ssx) to manage example scores when is_test=False.
    '''
    
    input_ = 'ssx red~example~score k vnew _test rm all'
    input_ += ' add RedExampleScoreTemplate.py done default'
    input_ += ' va _test vc vrm _test default q'
    score_manager._run(pending_user_input=input_)
    with_view = score_manager._transcript[-10]
    without_view = score_manager._transcript[-8]

    lines = [
        'Red Example Score (2013) - maker modules (_test)',
        '',
        '   1: RedExampleScoreTemplate.py',
        '',
        '      maker modules - copy (cp)',
        '      maker modules - new (new)',
        '      maker modules - remove (rm)',
        '      maker modules - rename (ren)',
        '',
        ]
    assert with_view.lines == lines

    title = 'Red Example Score (2013) - maker modules'
    assert without_view.title == title

    lines = [
        'RedExampleScoreRhythmMaker.py',
        'RedExampleScoreTemplate.py',
        ]

    contents = without_view.contents
    for line in lines:
        assert line in contents