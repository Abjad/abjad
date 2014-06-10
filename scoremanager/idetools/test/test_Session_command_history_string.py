# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_Session_command_history_string_01():

    score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
    input_ = 'foo bar blah q'
    score_manager._run(input_=input_)
    assert score_manager._session.command_history_string == input_