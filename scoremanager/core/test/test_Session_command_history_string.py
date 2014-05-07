# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_Session_command_history_string_01():

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'foo bar blah q'
    score_manager._run(pending_input=input_)
    assert score_manager._session.command_history_string == input_