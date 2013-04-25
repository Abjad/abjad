from experimental import *


def test_Session_command_history_string_01():

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager.run(user_input='foo bar blah q')
    assert score_manager.session.command_history_string == 'foo bar blah q'


def test_Session_command_history_string_02():

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager.run(user_input='example~score~i perf q')
    assert score_manager.session.command_history_string == 'example score i perf q'
