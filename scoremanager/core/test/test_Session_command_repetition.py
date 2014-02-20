# -*- encoding: utf-8 -*-
import pytest
from abjad import *
import scoremanager


def test_Session_command_repetition_01():
    pytest.skip('TODO: command repetition is currently broken.')

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='next . . . q')

    command_history = ['next', '.', '.', '.', 'q']
    assert score_manager._session.command_history == command_history
    assert score_manager._session.io_transcript.signature == (10, (1, 3, 5, 7))
