from experimental import *


def test_Session_command_repetition_01():

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager.run(user_input='next . . . q')
    assert score_manager.session.command_history == ['next', '.', '.', '.', 'q']
    assert score_manager.ts == (10, (1, 3, 5, 7))
