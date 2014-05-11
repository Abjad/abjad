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
    score_manager._run(pending_input=input_)
    transcript = score_manager._transcript

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
    assert any(_.lines == lines for _ in transcript)


def test_MakerModuleWrangler_clear_view_02():
    r'''In single makers directory: applies view and then clears view.

    Makes sure only one maker module is visible when view is applied.
    
    Then makes sure multiple maker modules are visible once view is cleared.
    '''
    
    input_ = 'red~example~score k vnew _test rm all'
    input_ += ' add RedExampleScoreTemplate.py done default'
    input_ += ' va _test vc vrm _test default q'
    score_manager._run(pending_input=input_)
    transcript = score_manager._transcript

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
    assert any(_.lines == lines for _ in transcript)