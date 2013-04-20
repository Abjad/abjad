from experimental import *


def test_Session_command_repetition_01():

    studio = scoremanagementtools.studio.ScoreManager()
    studio.run(user_input='next . . . q')
    assert studio.session.command_history == ['next', '.', '.', '.', 'q']
    assert studio.ts == (10, (1, 3, 5, 7))
