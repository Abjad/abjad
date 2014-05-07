# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager

# must be is_test=False for view tests
score_manager = scoremanager.core.ScoreManager(is_test=False)


def test_MakerModuleWrangler_apply_view_01():
    r'''Works in library.
    
    Makes sure only select maker module is visible.
    '''
    
    input_ = 'k vnew _test rm all'
    input_ += ' add RedExampleScoreTemplate.py~(Red~Example~Score)'
    input_ += ' done default'
    input_ += ' va _test vrm _test default q'
    score_manager._run(pending_input=input_)
    applied_view = score_manager._transcript[-8]

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
    assert applied_view.lines == lines


def test_MakerModuleWrangler_apply_view_02():
    r'''Works in score package makers directory.
    
    Makes sure only select maker module is visible.
    '''
    
    input_ = 'red~example~score k vnew _test rm all'
    input_ += ' add RedExampleScoreTemplate.py done default'
    input_ += ' va _test vrm _test default q'
    score_manager._run(pending_input=input_)
    applied_view = score_manager._transcript[-8]

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
    assert applied_view.lines == lines