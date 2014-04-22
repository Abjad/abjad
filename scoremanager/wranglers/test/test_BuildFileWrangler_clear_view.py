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
    input_ += ' add segment-01.ly done default'
    input_ += ' va _test V vrm _test default q'
    score_manager._run(pending_user_input=input_)
    with_view = score_manager._transcript[-10]
    without_view = score_manager._transcript[-8]

    lines = [
        'Score manager - build files (_test view)',
        '',
        '    1: segment-01.ly (Red Example Score)',
        '',
        '    files - copy (cp)',
        '    files - new (new)',
        '    files - remove (rm)',
        '    files - rename (ren)',
        '',
        ]
    assert with_view.lines == lines

    title = 'Score manager - build files'
    assert without_view.title == title

    lines = [
        'segment-01.ly (Red Example Score)',
        'segment-02.ly (Red Example Score)',
        'segment-03.ly (Red Example Score)',
        'score.pdf (Red Example Score)',
        ]

    contents = without_view.contents
    for line in lines:
        assert line in contents


def test_BuildFileWrangler_clear_view_02():
    r'''In single build directory: applies view and then clears view.

    Makes sure only one file is visible when view is applied.
    
    Then makes sure multiple files are visible once view is cleared.
    '''
    
    input_ = 'red~example~score u vnew _test rm all'
    input_ += ' add segment-01.ly done default'
    input_ += ' va _test V vrm _test default q'
    score_manager._run(pending_user_input=input_)
    with_view = score_manager._transcript[-10]
    without_view = score_manager._transcript[-8]

    lines = [
        'Score manager - build files (_test view)',
        '',
        '    1: segment-01.ly (Red Example Score)',
        '',
        '    files - copy (cp)',
        '    files - new (new)',
        '    files - remove (rm)',
        '    files - rename (ren)',
        '',
        ]
    assert with_view.lines == lines

    title = 'Score manager - build files'
    assert without_view.title == title

    lines = [
        'segment-01.ly (Red Example Score)',
        'segment-02.ly (Red Example Score)',
        'segment-03.ly (Red Example Score)',
        'score.pdf (Red Example Score)',
        ]

    contents = without_view.contents
    for line in lines:
        assert line in contents