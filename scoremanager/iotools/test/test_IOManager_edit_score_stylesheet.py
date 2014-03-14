# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager()


def test_IOManager_edit_score_stylesheet_01():
    r'''From score menu.
    '''

    input_ = 'red~example~score Y q'
    score_manager._run(pending_user_input=input_, is_test=True)
    assert score_manager._session.attempted_to_open_file


def test_IOManager_edit_score_stylesheet_02():
    r'''From segments menu.
    '''

    input_ = 'red~example~score g Y q'
    score_manager._run(pending_user_input=input_, is_test=True)
    assert score_manager._session.attempted_to_open_file


def test_IOManager_edit_score_stylesheet_03():
    r'''From segment menu.
    '''

    input_ = 'red~example~score g 1 Y q'
    score_manager._run(pending_user_input=input_, is_test=True)
    assert score_manager._session.attempted_to_open_file
