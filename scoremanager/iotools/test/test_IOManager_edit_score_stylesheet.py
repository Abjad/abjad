# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_IOManager_edit_score_stylesheet_01():
    r'''From score menu.
    '''

    input_ = 'red~example~score ess q'
    score_manager._run(pending_input=input_)
    assert score_manager._session._attempted_to_open_file


def test_IOManager_edit_score_stylesheet_02():
    r'''From segments menu.
    '''

    input_ = 'red~example~score g ess q'
    score_manager._run(pending_input=input_)
    assert score_manager._session._attempted_to_open_file


def test_IOManager_edit_score_stylesheet_03():
    r'''From segment menu.
    '''

    input_ = 'red~example~score g 1 ess q'
    score_manager._run(pending_input=input_)
    assert score_manager._session._attempted_to_open_file