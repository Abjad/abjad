from experimental import *


def test_UserInputGetterMenu_score_01():

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager._run(user_input='red~example~score setup performers move sco q')
    assert score_manager._session.transcript.signature == (11, (2, 9))
