# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ScoreManager__run_01():
    r'''Quit, home & junk all work.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (2,)

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'h q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (4, (0, 2))

    input_ = 'foo q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (4, (0, 2))


def test_ScoreManager__run_02():
    r'''Score is handled correctly.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 's q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (4, (0, 2))


def test_ScoreManager__run_03():
    r'''Back is handled correctly.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'b q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (4, (0, 2))
