# -*- encoding: utf-8 -*-
import pytest
from abjad import *
import scoremanager


def test_ScoreManager_01():
    r'''Main menu to mothballed scores.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='mb q')
    score_manager.session.io_transcript.signature == (4,)


def test_ScoreManager_02():
    r'''Main menu to score menu to tags menu.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='red~example~score tags q')
    assert score_manager.session.io_transcript.signature == (6,)


def test_ScoreManager_03():
    r'''Main menu to repository menu.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='rep q')
    assert score_manager.session.io_transcript.signature == (4,)


def test_ScoreManager_04():
    r'''Main menu header is the same even after state change to secondary menu.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='q')
    assert score_manager.session.io_transcript[-2][1][0] == \
        'Score manager - active scores'

    score_manager._run(pending_user_input='rep q')
    assert score_manager.session.io_transcript[-2][1][0] == \
        'Score manager - active scores - repository commands'

    score_manager._run(pending_user_input='rep b q')
    assert score_manager.session.io_transcript[-2][1][0] == \
        'Score manager - active scores'


def test_ScoreManager_05():
    r'''Junk works.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='foo q')
    assert score_manager.session.io_transcript.signature == (4, (0, 2))

    score_manager._run(pending_user_input='foo bar q')
    assert score_manager.session.io_transcript.signature == (6, (0, 2, 4))


def test_ScoreManager_06():
    r'''Back is handled correctly.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='b q')
    assert score_manager.session.io_transcript.signature == (4, (0, 2))


def test_ScoreManager_07():
    r'''Exec works.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='exec 2**30 q')

    assert score_manager.session.io_transcript[1][1] == ['> exec', '']
    assert score_manager.session.io_transcript[2][1] == ['XCF> 2**30']
    assert score_manager.session.io_transcript[3][1] == ['1073741824', '']
    assert score_manager.session.io_transcript[4][1] == ['> q', '']


def test_ScoreManager_08():
    r'''Exec protects against senseless input.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='exec foo q')

    assert score_manager.session.io_transcript[1][1] == ['> exec', '']
    assert score_manager.session.io_transcript[2][1] == ['XCF> foo']
    assert score_manager.session.io_transcript[3][1] == ['Expression not executable.', '']
    assert score_manager.session.io_transcript[4][1] == ['> q', '']


def test_ScoreManager_09():
    r'''Shared session.
    '''

    score_manager = scoremanager.core.ScoreManager()

    assert score_manager.session is score_manager.score_package_wrangler.session


def test_ScoreManager_10():
    r'''Backtracking stu* shortcut.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='Mon instrumentation home q')
    ts_1 = score_manager.session.io_transcript.signature

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='Mon instrumentation home q')
    ts_2 = score_manager.session.io_transcript.signature

    assert ts_1 == ts_2


def test_ScoreManager_11():
    r'''Backtracking sco* shortcut.
    '''
    pytest.skip('TODO: make sco shortcut work again.')

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='Mon score~setup score q')
    ts_1 = score_manager.session.io_transcript.signature

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='Mon score~setup sco q')
    ts_2 = score_manager.session.io_transcript.signature

    assert ts_1 == ts_2
