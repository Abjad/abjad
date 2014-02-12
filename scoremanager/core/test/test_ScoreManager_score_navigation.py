# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ScoreManager_score_navigation_01():
    r'''Score does nothing.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='score q')
    score_manager.session.io_transcript.signature == (4, (0, 2))


def test_ScoreManager_score_navigation_02():
    r'''Session-initial next and prev both work.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='next q')
    score_manager.session.io_transcript.signature == (4,)
    isinstance(score_manager.session.snake_case_current_score_name, str)

    score_manager._run(pending_user_input='prev q')
    score_manager.session.io_transcript.signature == (4,)
    isinstance(score_manager.session.snake_case_current_score_name, str)


def test_ScoreManager_score_navigation_03():
    r'''Successive next.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='next next next q')
    score_manager.session.io_transcript.signature == (8, (1, 3, 5))
    isinstance(score_manager.session.snake_case_current_score_name, str)


def test_ScoreManager_score_navigation_04():
    r'''Successive prev.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='prev prev prev q')
    score_manager.session.io_transcript.signature == (8, (1, 3, 5))
    isinstance(score_manager.session.snake_case_current_score_name, str)
