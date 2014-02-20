# -*- encoding: utf-8 -*-
import pytest
from abjad import *
import scoremanager


def test_ScoreManager_score_navigation_02():
    r'''Session-initial next and prev both work.
    '''
    pytest.skip('FIXME')

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='next q')
    assert score_manager._session.io_transcript.signature == (4,)
    assert isinstance(score_manager._session.current_score_snake_case_name, str)

    score_manager._run(pending_user_input='prev q')
    assert score_manager._session.io_transcript.signature == (4,)
    assert isinstance(score_manager._session.current_score_snake_case_name, str)


def test_ScoreManager_score_navigation_03():
    r'''Successive next.
    '''
    pytest.skip('FIXME')

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='next next next q')

    assert score_manager._session.io_transcript.signature == (8, (1, 3, 5))
    assert isinstance(score_manager._session.current_score_snake_case_name, str)


def test_ScoreManager_score_navigation_04():
    r'''Successive prev.
    '''
    pytest.skip('FIXME')

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='prev prev prev q')
    assert score_manager._session.io_transcript.signature == (8, (1, 3, 5))
    assert isinstance(score_manager._session.current_score_snake_case_name, str)
