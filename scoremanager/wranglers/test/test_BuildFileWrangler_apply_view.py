# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager

# must be is_test=False for view tests
score_manager = scoremanager.core.ScoreManager(is_test=False)


def test_BuildFileWrangler_apply_view_01():
    r'''Applies view to library.
    
    Makes sure only select build files are visible.
    '''
    
    input_ = 'u vnew _test rm all'
    input_ += ' add segment-01.ly'
    input_ += ' add segment-02.ly'
    input_ += ' add segment-03.ly done default'
    input_ += ' va _test vrm _test default q'
    score_manager._run(pending_user_input=input_)
    applied_view = score_manager._transcript[-8]

    lines = [
        'Score manager - build file library (_test view)',
        '',
        '    1: segment-01.ly (Red Example Score)',
        '    2: segment-02.ly (Red Example Score)',
        '    3: segment-03.ly (Red Example Score)',
        '',
        '    files - copy (cp)',
        '    files - new (new)',
        '    files - remove (rm)',
        '    files - rename (ren)',
        '',
        ]
    assert applied_view.lines == lines


def test_BuildFileWrangler_apply_view_02():
    r'''Applies view to single view directory.
    
    Makes sure only select build files are visible.
    '''
    
    input_ = 'red~example~score u vnew _test rm all'
    input_ += ' add segment-01.ly done default'
    input_ += ' va _test vrm _test default q'
    score_manager._run(pending_user_input=input_)
    applied_view = score_manager._transcript[-8]

    lines = [
        'Score manager - build file library (_test view)',
        '',
        '    1: segment-01.ly (Red Example Score)',
        '',
        '    files - copy (cp)',
        '    files - new (new)',
        '    files - remove (rm)',
        '    files - rename (ren)',
        '',
        ]
    assert applied_view.lines == lines