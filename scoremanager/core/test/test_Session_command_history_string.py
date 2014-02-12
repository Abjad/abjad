# -*- encoding: utf-8 -*-
from experimental import *


def test_Session_command_history_string_01():

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='foo bar blah q')
    assert score_manager.session.command_history_string == 'foo bar blah q'


def test_Session_command_history_string_02():

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='red~example~score instrumentation q')
    assert score_manager.session.command_history_string == 'red example score instrumentation q'
